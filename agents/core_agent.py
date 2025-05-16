from agents.tool_registry import ToolRegistry
from agents.prompt_templates import SYSTEM_PROMPT, RESERVATION_PROMPT, RECOMMENDATION_PROMPT, ERROR_PROMPT

class FoodieSpotAgent:
    def __init__(self, llm, data_service):
        self.llm = llm
        self.data_service = data_service
        self.tool_registry = self._initialize_tools()
        self.conversation_history = []
        self.current_context = None
        self.pending_reservation = None

    def _initialize_tools(self):
        """Register all available tools"""
        from tools.reservation_tools import ReservationTools
        from tools.query_tools import QueryTools
        from tools.recommendation_tools import RecommendationTools
        from services.validation_service import ValidationService

        validation = ValidationService()
        tool_registry = ToolRegistry()

        # Register reservation tools
        reservation_tools = ReservationTools(self.data_service, validation)
        tool_registry.register_tool(
            "check_availability",
            reservation_tools.check_availability,
            "Check if a restaurant has availability for a given time and party size",
            {
                "restaurant_id": {"type": "string", "required": True},
                "date": {"type": "string", "format": "YYYY-MM-DD", "required": True},
                "party_size": {"type": "integer", "required": True},
                "time_slot": {"type": "string", "format": "HH:MM", "required": True}
            }
        )

        # Register query tools
        query_tools = QueryTools(self.data_service)
        tool_registry.register_tool(
            "list_restaurants",
            query_tools.list_restaurants,
            "List restaurants matching given criteria",
            {
                "cuisine": {"type": "list", "required": False},
                "location": {"type": "string", "required": False},
                "features": {"type": "list", "required": False}
            }
        )

        # Register recommendation tools
        recommendation_tools = RecommendationTools(self.data_service)
        tool_registry.register_tool(
            "get_recommendations",
            recommendation_tools.get_recommendations,
            "Get restaurant recommendations based on occasion and preferences",
            {
                "occasion": {"type": "string", "required": False},
                "preferences": {"type": "string", "required": False}
            }
        )

        return tool_registry

    def _format_tool_response(self, tool_name, tool_result):
        """Format tool output with proper error handling"""
        if tool_name == "check_availability":
            if not tool_result.get("restaurant_name"):
                return "Sorry, I encountered an error checking availability. Please try again."
            if tool_result.get("available", False):
                return f"Great news! {tool_result['restaurant_name']} has availability. Would you like to proceed?"
            else:
                alternatives = tool_result.get("alternative_times", [])
                alt_msg = f" Alternative times: {', '.join(alternatives)}" if alternatives else ""
                return f"Sorry, {tool_result['restaurant_name']} is booked at that time.{alt_msg}"
        elif tool_name == "list_restaurants":
            if tool_result.get('count', 0) == 0:
                return "No matching restaurants found."
            names = [r['name'] for r in tool_result['restaurants']]
            return f"Found {tool_result['count']} restaurants: {', '.join(names)}"
        elif tool_name == "get_recommendations":
            names = [r['name'] for r in tool_result]
            return f"I recommend: {', '.join(names)}"
        return str(tool_result)

    def process_message(self, user_input):
        """Main agent loop with improved conversation flow"""
        self.conversation_history.append({"role": "user", "content": user_input})

        if self.pending_reservation:
            # Collect missing reservation info if needed
            missing = [p for p in ["restaurant_id", "date", "party_size", "time_slot"] if p not in self.pending_reservation]
            if missing:
                questions = {
                    "restaurant_id": "Which location would you prefer? (Downtown or Riverside)",
                    "date": "What date would you like to book for?",
                    "party_size": "How many people will be dining?",
                    "time_slot": "What time would you like to reserve?"
                }
                response = questions[missing[0]]
                self.conversation_history.append({"role": "assistant", "content": response})
                return response
            try:
                tool_result = self.tool_registry.execute_tool(
                    "check_availability",
                    self.pending_reservation
                )
                self.pending_reservation = None
                response = self._format_tool_response("check_availability", tool_result)
            except Exception as e:
                response = self.llm.generate("error") + f"\nError: {str(e)}"
        else:
            # New reservation flow or general query
            tool_decision = self.llm.generate("tool_decision", user_input)
            if tool_decision.get("requires_tool"):
                self.pending_reservation = tool_decision["arguments"]
                missing = [p for p in ["restaurant_id", "date", "party_size", "time_slot"] if p not in self.pending_reservation]
                if missing:
                    questions = {
                        "restaurant_id": "Which location would you prefer? (Downtown or Riverside)",
                        "date": "What date would you like to book for?",
                        "party_size": "How many people will be dining?",
                        "time_slot": "What time would you like to reserve?"
                    }
                    response = f"To make your reservation, I need to know:\n" + "\n".join(f"- {questions[m]}" for m in missing)
                else:
                    try:
                        tool_result = self.tool_registry.execute_tool(
                            tool_decision["tool_name"],
                            self.pending_reservation
                        )
                        self.pending_reservation = None
                        response = self._format_tool_response(tool_decision["tool_name"], tool_result)
                    except Exception as e:
                        response = self.llm.generate("error") + f"\nError: {str(e)}"
            else:
                response = self.llm.generate("general_response", user_input)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

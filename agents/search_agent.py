from google.adk.agents import Agent
from google.adk.tools import google_search
from config.settings import MODEL_GEMINI

def create_search_agent():
    """
    Creates and configures the Google ADK greeting agent.
    This agent is designed to provide personalized greetings and engage in general conversation.
    """
    root_agent = Agent(
        name="search_agent", # A unique name for this specific agent.
        model=MODEL_GEMINI,    # Specifies the Gemini model to power this agent's language understanding and generation.
        description="An agent that searches the web for user-related activities.", # A brief, human-readable description of the agent's role.
        instruction=""" # The core instructions that dictate the agent's behavior and how it should use its tools.
        You are a helpful assistant that searches the web for the user for activities to do near them that day.
        
        You will utilize the provided interests and hobbies by the user to guide your search for the day's events.

        You will use the 'google_search' tool to collect your information.
        """,
        tools = [google_search]
    )
    return root_agent
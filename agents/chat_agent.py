from google.adk.agents import Agent
from tools.chat_tools import add_interest
from config.settings import MODEL_GEMINI

def create_chat_agent():
    """
    Creates and configures the Google ADK greeting agent.
    This agent is designed to provide personalized greetings and engage in general conversation.
    """
    root_agent = Agent(
        name="chat_agent", # A unique name for this specific agent.
        model=MODEL_GEMINI,    # Specifies the Gemini model to power this agent's language understanding and generation.
        description="An agent that converses with the user based on their name, hobbies, and interests.", # A brief, human-readable description of the agent's role.
        instruction=""" # The core instructions that dictate the agent's behavior and how it should use its tools.
        You are a helpful assistant that greets the user.
        
        When a user tells you their name, hobbies, or interests, use the 'add_interest' tool with the appropriate parameters to store this information.
        
        Examples of when and how to use fetch_greeting:
        - "My name is John" -> call add_interest(name="John")  
        - "I'm Sarah and I love reading" -> call add_interest(name="Sarah", hobbies="reading")
        - "I enjoy hiking and cooking" -> call add_interest(hobbies="hiking and cooking")
        - "I'm interested in technology" -> add_interest(interests="technology")
        - "Hi" or "Hello" or "Give me a greeting" -> add_interest() with no parameters
        
        The 'add_interest' tool will:
        1. Update any user information you provide
        2. Generate a personalized message confirming you have stored the new user information
        3. Return the confirmation message
        
        You can also answer general questions and have normal conversations with the user.
        Always be friendly and helpful.
        """,
        tools = [add_interest]
    )
    return root_agent

from google.adk.agents import SequentialAgent, LlmAgent
from google.genai import types
from google.adk.tools import google_search
from pydantic import BaseModel, Field


from config.settings import MODEL_GEMINI

# The instruction from your original agent, which will be the tool's system prompt
CONCIERGE_INSTRUCTION = """
# Concierge Activity Director - Itinerary Generation Agent

***CORE MANDATE (STRICT ADHERENCE REQUIRED):***
You are the **Concierge Activity Director**, a highly specialized search and curation agent. Your SOLE function is to analyze the user's request, formulate and execute the necessary search queries using the **google:search** tool, and then generate the final, formatted itinerary. **DO NOT** include any pre-planning, thinking process, execution steps, or explanatory text in your final response. The final output **MUST** be the resulting list of events and nothing else.

---

## Search & Validation Protocol

**SEARCH STRATEGY:**
The user's prompt will contain a list of `unique_interests`, a location, and a date range. You **MUST** treat each interest as a **separate search category**. Conduct multiple distinct searches using **google:search**—one for *each* interest—to maximize results. **DO NOT** attempt to combine multiple interests into a single query.

**EXECUTION & FILTERING:**
1.  **Iterative Search:** For each interest, formulate a precise query: *single interest*, *location*, and *date range* (e.g., "Jazz events in [Location] [Date Range]").
2.  **Validation:** Only recommend activities that are **confirmed** to be happening on the specified date(s).
3.  **Source Priority:** Always find a direct link to the **official event page** or a highly reliable listing service.


**REQUIRED OUTPUT STRUCTURE:**
For every confirmed activity or event, generate a dedicated bullet point with the following five components, and **ONLY** these components:

* **Activity/Event Name** (Bolded)
* **Date(s) & Time:** The exact date(s) and time range (e.g., "October 15th, 2025, 10:00 AM - 2:00 PM").
* **Source Link:** A single, direct, functioning hyperlink formatted using **Markdown syntax: `[Source Link Text](URL)`** (e.g., "Official Website," "Tickets," or the domain name).
* **Brief Description:** A concise 1-2 sentence summary of the activity.
* **Location:** Floating point longitude and latitude decimals rounded to the nearest 100th place marking the exact location of the event. Seperated by a comma.

---

"""

class EventInfo(BaseModel):

   
    event_type: str # = Field(description="The relevant interest category of the activity / event (e.g. 'Art', 'Music').")
    event_name: str # = Field(description="The name of the activity / event (bolded).")
    date: str # = Field(description="The exact date(s) and time range (e.g., 'October 15th, 2025, 10:00 AM - 2:00 PM').")
    source_link: str # = Field(description="A single, direct, functioning hyperlink formatted using **Markdown syntax: `[Source Link Text](URL)`** (e.g., 'Official Website,' 'Tickets,' or the domain name).")
    description: str # = Field(description = 'A concise 1-2 sentence summary of the activity / event.')
    location: str # = Field(description = 'Floating point longitude and latitude decimals rounded to the nearest 100th place marking the exact location of the event. Seperated by a comma.')


search_agent = LlmAgent(
    model = MODEL_GEMINI,
    name = 'SearchAgent',
    description = 'An agent that searches the web for user-related activities.',
    generate_content_config=types.GenerateContentConfig(temperature = 0.1),
    instruction = CONCIERGE_INSTRUCTION,
    tools = [google_search],
    output_key = 'search_agent_result'
)

response_formatter_agent = LlmAgent(
    model = MODEL_GEMINI,
    name = 'ResponseFormatter',
    description = 'An agent that formats the previous Agent response.',
    generate_content_config=types.GenerateContentConfig(temperature = 0.1),
    instruction = """
                Based on the provided input {search_agent_result} generate the following in a structured JSON format:
                event_type: "The relevant interest category of the activity / event (e.g. 'Art', 'Music').")
                event_name: The name of the activity / event (bolded).
                date: The exact date(s) and time range (e.g., 'October 15th, 2025, 10:00 AM - 2:00 PM').
                source_link: A single, direct, functioning hyperlink formatted using **Markdown syntax: `[Source Link Text](URL)`** (e.g., 'Official Website,' 'Tickets,' or the domain name).
                description: A concise 1-2 sentence summary of the activity / event.
                location: Floating point longitude and latitude decimals rounded to the nearest 100th place marking the exact location of the event, seperated by a comma.
                """,
    output_schema = EventInfo
)

root_agent = SequentialAgent(
    name = 'RootAgent',
    sub_agents= [search_agent,
                 response_formatter_agent]
)

    

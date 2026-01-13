import os
import sys
sys.path.append("..")
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import AgentTool
from google.adk.tools import VertexAiSearchTool

from .tools import get_date
from .send_email_tool import send_email
from .state_tool import save_attribute_to_state

from .guradrail_agents import guardrail_agent
from summarizer_agent import summarizer_agent





# Create your vertexai_search_tool and update its path below
vertexai_search_tool = VertexAiSearchTool(
    search_engine_id="projects/data-discovery-306320/locations/global/collections/default_collection/engines/jira-tickets_1768222530040"
)

vertexai_search_agent = Agent(
    name="vertexai_search_agent",
    model=os.getenv("MODEL"),
    instruction="Use your search tool to look up jira tickets. save output result to state with key = 'vertexai_search_result'.",
    tools=[vertexai_search_tool]
)

# jira_agent = Agent(
#     name="jira_agent",
#     model="gemini-2.5-flash",
#     instruction="Search Jira tickets and return raw results.",
#     tools=[AgentTool(vertexai_search_agent)]
# )

jira_agent = Agent(
    name="jira_agent",
    model="gemini-2.5-flash",
    instruction="Search Jira tickets and return raw results, save them in state with key = 'jira_ticket_<id>'.",
    tools=[AgentTool(vertexai_search_agent), save_attribute_to_state] #When it's used as an agent, we need to remove mulitple tools
)

send_email_agent = Agent(
    name="send_email_agent",
    model="gemini-2.5-flash",
    instruction="""
    Send email ONLY if approved.
    """,
    tools=[send_email]
)

load_dotenv()
root_agent = Agent(
    name="cx_911_agent",
    description="Summarize the provided jira ticket information.",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    instruction="""
    You are an agent to try to help customer resolve production support issues.

    1. Provide summarize the provided jira ticket information. 
    2. Use 'jira_agent' tool to check if there are duplicated / similar tickets. output a message to show that.
    3. Provide solution suggestion.
    4. Save the suggestions to state as key = Jira-ticket id, value = solution suggestion.

    5. If customer asks questions about Jira tickets for example number of tickets, use 'jira_agent' to check them.

    6. Write a email reply to the customer, including summary, issue suggestion. store the reply to state 'output_result_candidate'
    
    7. Use guardrail_agent to calculate guardrail scores for the 'output_result_candidate' reply. The guardrail_agent will store result in state with key = 'QulityGate'
    
    8. When 'QulityGate' passed, then use 'send_email_agent' to send the 'output_result_candidate' to 'farrah.tsai@onetrust.com' and 'thsinfang@gmail.com'
    """,
   
    # instruction="Summarize the provided jira ticket information. Then give an SLA as 3 days from now using 'get_date' tool",
    tools=[save_attribute_to_state, AgentTool(jira_agent)],

    sub_agents=[
        # jira_agent,
        send_email_agent,
        guardrail_agent,
    ]

    

    # film_concept_team = SequentialAgent(
    # name="film_concept_team",
    # description="Write a film plot outline and save it as a text file.",
    # sub_agents=[
    #     writers_room,
    #     file_writer
    # ],
    # )
)
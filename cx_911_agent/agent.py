import os
import sys
sys.path.append("..")
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import AgentTool

from .tools import get_date
from .send_email_tool import send_email
from .state_tool import save_attribute_to_state

from .guradrail_agents import guardrail_agent
from .summarizer_agent import summarizer_agent
from .solution_provider_agent import solution_proivder_agent



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

    1. Use 'summarizer_agent' to summarize the provided jira ticket information. 
    2. Use 'solution_provider_agent' to provide suggested solution.

    3. Save the suggestions to state as key = Jira-ticket id, value = solution suggestion.

    4. If customer asks questions about Jira tickets for example number of tickets, use 'jira_agent' to check them.

    5. Write a email reply to the customer, including summary, issue suggestion. store the reply to state 'output_result_candidate'
    
    6. Use guardrail_agent to calculate guardrail scores for the 'output_result_candidate' reply. The guardrail_agent will store result in state with key = 'QulityGate'
    
    7. Check state with 'QulityGate' key. If passed, then use 'send_email_agent' to send the 'output_result_candidate' to 'farrah.tsai@onetrust.com' and 'thsinfang@gmail.com'
    """,
   
    # instruction="Summarize the provided jira ticket information. Then give an SLA as 3 days from now using 'get_date' tool",
    tools=[save_attribute_to_state],

    sub_agents=[
        summarizer_agent,
        solution_proivder_agent,
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
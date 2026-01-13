import os
import sys
sys.path.append("..")
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import AgentTool
from google.adk.agents import SequentialAgent

from .tools import get_date
from .send_email_tool import send_email_tool
from .state_tool import save_attribute_to_state

from .guradrail_agents import guardrail_agent
from .summarizer_agent import summarizer_agent
from .solution_provider_agent import solution_proivder_agent



send_email_agent = Agent(
    name="send_email_agent",
    model="gemini-2.5-flash",
    instruction="""
    Send email ONLY if {QualityGate? = PASS}. The subject and body can be reached from {output_result_candidate ?}
    """,
    tools=[send_email_tool]
)

response_proivder_agent=Agent(
    name="response_proivder_agent",
    model="gemini-2.5-flash",
    instruction="""
    Get {jira_ticket_summary ?}, {solution_suggestion ?} and write an email reply to customer.
    Store the email reply to state with key = 'output_result_candidate'
    """,
    tools=[save_attribute_to_state]
)


load_dotenv()

cx_911_sequential_agent=SequentialAgent(
    name="cx_911_sequential_agent",
    description="Summarize the provided jira ticket information and provide solution suggestion",
    sub_agents=[
        summarizer_agent,
        solution_proivder_agent,
        response_proivder_agent,
        guardrail_agent,
        send_email_agent,
    
    ],
)


root_agent = Agent(
    name="cx_911_agent",
    description="Summarize the provided jira ticket information.",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    instruction="""
    You are an agent to try to help customer resolve production support issues.
    Store the user input into state with key = 'new_jira_ticket' and use cx_911_sequential_agent subagent to resolve it.

    """,
   
    # instruction="Summarize the provided jira ticket information. Then give an SLA as 3 days from now using 'get_date' tool",
    tools=[save_attribute_to_state],
    sub_agents=[
        cx_911_sequential_agent
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
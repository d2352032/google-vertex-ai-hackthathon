import os
from google.adk import Agent
from google.adk.tools import AgentTool
from google.adk.agents import SequentialAgent
# from .jira_agent import jira_agent
from .jira_agent import vertexai_search_agent

from .state_tool import save_attribute_to_state




compare_existing_tickets_agent=Agent(
    name="compare_existing_tickets_agent",
    description="Take in jira ticket summary, provide if there's similar / duplicate existing jira tickets using 'jira_agent' ",
    instruction="""
    Take in jira ticket summary, check if there's similar / duplicate existing jira tickets using 'jira_agent'.
    Store the result to state with key =  'compare_existing_tickets' 
    """,
    tools=[save_attribute_to_state, AgentTool(vertexai_search_agent)],
    # sub_agents=[jira_agent]
)

suggest_solution_agent=Agent(
    name="suggest_solution_agent",
    description="provide suggested solution by considering 'jira_ticket_summary' and 'compare_existing_tickets' ",
    instruction="""
    Get {new_jira_ticket?}, {jira_ticket_summary ?} and {compare_existing_tickets?}, and provide suggested solution. 
    Store the provided solution in state with key = 'solution_suggestion' 
    """,
    tools=[save_attribute_to_state],
)

solution_proivder_agent=SequentialAgent(
    name="solution_proivder_agent",
    description="Take in jira ticket summary, check similar jira tickets and provide solution suggestion",
    sub_agents=[
        compare_existing_tickets_agent,
        suggest_solution_agent,
    ]
)
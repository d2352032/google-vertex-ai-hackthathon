import os
from google.adk import Agent
from google.adk.tools import AgentTool
from google.adk.tools import VertexAiSearchTool


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

jira_agent = Agent(
    name="jira_agent",
    model="gemini-2.5-flash",
    instruction="Search Jira tickets and return raw results.",
    tools=[AgentTool(vertexai_search_agent)]
)
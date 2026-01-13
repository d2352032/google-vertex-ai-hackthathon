import os
from google.adk import Agent
from google.adk.tools import AgentTool
from .jira_agent import vertexai_search_agent
from .state_tool import save_attribute_to_state

customer_360_info_agent=Agent(
    name="customer_360_info_agent",
    model="gemini-2.5-flash",
    instruction = """
        Step 1: From {new_jira_ticket?}, retrieve the customer account name and store it in state with:
        - key: "account_name"
        - value: the extracted account name

        Step 2: Use "vertexai_search_agent" to fetch additional Jira tickets associated with this account.

        Step 3: Using the account name and related tickets, retrieve and ground information from the Customer 360 personal data store.

        Customer 360 data may include:
        - Contacts (matched by account name)
        - Tenant ID
        - Roles
        - Consent status
        - Communication preferences
        - Interaction and activity history

        Step 4: Extract all relevant personal data and store it in state with:
        - key: "customer_360_info"
        - value: a structured object in the following format:

        {
        "contact": "...",
        "tenant_id": "...",
        "roles": "...",
        "consent": "...",
        "communication_preferences": "...",
        "history": "..."
        }

        Constraints:
        - Each field must be a concise summary, maximum 200 words.
        - Use only information explicitly supported by Customer 360 data.
        - Do not infer, enrich, or fabricate missing data.
        - If a field is unavailable, set its value to null.
    """,

    tools=[save_attribute_to_state, AgentTool(vertexai_search_agent)]
)
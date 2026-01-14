import os
from google.adk import Agent
from google.adk.tools import AgentTool
from .jira_agent import vertexai_search_agent
from .state_tool import save_attribute_to_state

customer_360_info_agent=Agent(
    name="customer_360_info_agent",
    model="gemini-2.5-flash",
    instruction = """
        Step 1: Identify the customer account name.
        - Source the account name from the provided context or input (e.g., Jira custom field "Account Name").
        - If the account name cannot be determined, set it to null and continue.

        Step 2: Use the tool "vertexai_search_agent" to retrieve all Jira tickets associated with the identified account name.
        - Match tickets by account name.
        - Include tickets across all statuses.
        - If no related tickets are found, proceed using only the current ticket.

        Step 3: Using the account name and all related Jira tickets, retrieve and ground information to construct:
        A) Customer Account data
        B) Tenant Information data

        Customer Account fields:
        | Field                         | Description |
        |------------------------------|-------------|
        | Account Name                 | Customer legal or business name |
        | Engagement Type              | e.g., POC, Evaluation, Production |
        | Customer Identified Issue    | Yes / No |
        | Customer Temperature         | Hot / Warm / Cold |
        | Reported By Region           | Geographic region |
        | Reported By Team             | Internal reporting team |

        Tenant Information fields:
        | Field                      | Description |
        |---------------------------|-------------|
        | Tenant GUID               | Unique tenant identifier |
        | Environment Context       | Trial, production, internal, etc. |
        | Database Type             | SQL, Oracle, etc. |
        | Product Area              | Product and sub-product |
        | Engine Version Context    | Platform version, migration, or release context |

        Step 4: Store the extracted and grounded data in agent state:
        - key: "customer_360_datastore"
        - value: an object containing:
        - customer_account
        - tenant_information

        Constraints:
        - Each field must be a concise grounded summary (maximum 200 words).
        - Use only information explicitly supported by Jira ticket data.
        - Do not infer or hallucinate values.
        - If a field is unavailable or unsupported, set its value to null.
    """,

    tools=[save_attribute_to_state, AgentTool(vertexai_search_agent)]
)
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
from .safe_setting import generate_content_config
from .customer_360_agents import customer_360_info_agent


send_email_agent = Agent(
    name="send_email_agent",
    model="gemini-2.5-flash",
    instruction = """
        Condition:
        - Check whether {QualityGate?} == "PASS".

        Actions:
        - If {QualityGate?} == "PASS":
            1. Use the email subject and email body from {output_result_candidate?}.
            2. Set the email recipient to:
                receiver = "customer@example.com"
            3. Send the email.

        - If {QualityGate?} != "PASS":
            - Do not send an email.
            - Take no further action.
    """,
    tools=[send_email_tool]
)

response_proivder_agent=Agent(
    name="response_proivder_agent",
    model="gemini-2.5-flash",
    generate_content_config=generate_content_config,
    instruction = """
    Using the available inputs:
    - {jira_ticket_summary ?}
    - {solution_suggestion ?}

    Draft a professional email reply to the customer that addresses the ticket and incorporates the solution where appropriate.

    Save the generated email reply to the state using the key:
    - output_result_candidate

    Constraints:
    - The email must end with the following signature (exact text):

    "Sincerely,
        OneTrust – Your Trusted AI Partner"
    """,

    tools=[save_attribute_to_state]
)




load_dotenv()

cx_911_sequential_agent=SequentialAgent(
    name="cx_911_sequential_agent",
    description="Summarize the provided jira ticket information and provide solution suggestion",
    sub_agents=[
        customer_360_info_agent,
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

    1. Get customer account name and store it in state with key = 'account_name'
    2. Summarize the ticket and store it to state with key = 'jira_ticket_summary'
    3. Run 'cx_911_sequential_agent' for next steps.

    """,
   
    # instruction="Summarize the provided jira ticket information. Then give an SLA as 3 days from now using 'get_date' tool",
    tools=[save_attribute_to_state],
    sub_agents=[
        cx_911_sequential_agent
    ]

)
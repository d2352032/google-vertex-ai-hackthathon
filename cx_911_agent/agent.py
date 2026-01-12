import os
import sys
sys.path.append("..")
from dotenv import load_dotenv
from google.adk import Agent
from .tools import get_date
from .send_email_tool import send_email



load_dotenv()
root_agent = Agent(
    name="cx_911_agent",
    description="Summarize the provided jira ticket information.",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    instruction="Summarize the provided jira ticket information. Then send the summary to 'farrah.tsai@onetrust.com' and 'thsinfang@gmail.com'",
    # instruction="Summarize the provided jira ticket information. Then give an SLA as 3 days from now using 'get_date' tool",
    tools=[get_date, send_email]
)
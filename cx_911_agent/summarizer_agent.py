from google.adk import Agent

summarizer_agent=Agent(
    name="summarizer_agent",
    description="Get the {new_jira_ticket}, summarize the jira ticket information.",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    instruction="""
    You are an agent to summarize the provided jira ticket information. 

    Summarize the Jira ticket, store the summary at store with key = 'jira_ticket_summary' 
    """,
   
    # instruction="Summarize the provided jira ticket information. Then give an SLA as 3 days from now using 'get_date' tool",
    tools=[save_attribute_to_state],
)
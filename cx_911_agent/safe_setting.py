import re
import vertexai
from google.auth import default
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

# Import safety config types
from google.genai import types

# =========================
# CONFIGURATION
# =========================
PROJECT_ID = "data-discovery-306320"
REGION = "us-central1"
STAGING_BUCKET = "gs://ai-agent-vertex-mks"

EXISTING_AGENT_RESOURCE = None

# =========================
# MODEL SAFETY SETTINGS
# (Gemini Recommended Safety Filters)
# =========================
safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
]

generate_content_config = types.GenerateContentConfig(
    safety_settings=safety_settings,
    temperature=0.2,
    max_output_tokens=1000,
    top_p=0.9,
)

# =========================
# GUARDRAILS (Optional)
# =========================
PII_PATTERNS = [
    r"\b\d{12}\b",
    r"\b\d{10}\b",
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
]

BANNED_TOPICS = [
    "terrorism",
    "bomb",
    "drug trafficking",
    "credit card fraud",
    "money laundering",
]

def run_guardrails(prompt: str):
    for p in PII_PATTERNS:
        if re.search(p, prompt):
            raise ValueError("❌ PII detected. Blocked.")
    for topic in BANNED_TOPICS:
        if topic.lower() in prompt.lower():
            raise ValueError("❌ Banned topic. Blocked.")

# =========================
# INIT VERTEX
# =========================
def init_vertex():
    creds, _ = default()
    vertexai.init(
        project=PROJECT_ID,
        location=REGION,
        credentials=creds,
    )

# =========================
# TOOL
# =========================
def get_exchange_rate(currency_from: str="USD", currency_to: str="INR"):
    import requests
    r = requests.get(
        "https://api.frankfurter.app/latest",
        params={"from": currency_from, "to": currency_to},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()

# # =========================
# # DEPLOY AGENT
# # =========================
# def deploy_agent_once():
#     # Create the Agent with safety config
#     agent = Agent(
#         name="currency_safe_agent",
#         model="gemini-2.0-flash",
#         generate_content_config=generate_content_config,
#         tools=[get_exchange_rate],
#     )

#     app = AdkApp(agent=agent)
#     client = vertexai.Client(project=PROJECT_ID, location=REGION)

#     print("Deploying agent with safety filters…")

#     remote_agent = client.agent_engines.create(
#         agent=app,
#         config={
#             "staging_bucket": STAGING_BUCKET,
#             "requirements": [
#                 "google-cloud-aiplatform[agent_engines,adk]",
#                 "requests",
#                 "google-genai",
#                 "pydantic",
#                 "cloudpickle",
#             ],
#         },
#     )

#     print("Deployed Agent:")
#     print(remote_agent.api_resource.name)
#     return remote_agent.api_resource.name

# # =========================
# # MAIN
# # =========================
# if __name__ == "__main__":
#     init_vertex()

#     if EXISTING_AGENT_RESOURCE:
#         agent_name = EXISTING_AGENT_RESOURCE
#         print("Existing agent:", agent_name)
#     else:
#         agent_name = deploy_agent_once()
#         print("Save this ID for reuse:", agent_name)

#     # Try guarded prompt
#     prompt = "Convert USD to INR"
#     try:
#         run_guardrails(prompt)
#         print("Prompt is safe to send.")
#     except Exception as e:
#         print(str(e))
 
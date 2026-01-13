from google.adk import Agent
from google.adk.agents import SequentialAgent

from .state_tool import save_attribute_to_state

policy_guard_agent = Agent(
    name="policy_guard_agent",
    model="gemini-2.5-pro",
    description="Provide policy_guard_result - policy score and consent value",
    instruction="""
    You are a policy compliance agent.

    Get {output_result_candidate ?},
    Check the following:
    - Customer data is used only for support purposes
    - Customer consent exists for outbound email
    - No unnecessary PII is included

    Output STRICT JSON:
    {
      "consent_ok": true|false,
      "policy_score": 0.0-1.0,
      "violations": []
    }

    Use the 'save_attribute_to_state' Store the output strict JSON to state with key = 'policy_guard_result'
    """,
    tools=[save_attribute_to_state]
)

groundedness_agent = Agent(

    name="groundedness_agent",
    description="Provide groundedness_result",
    instruction="""
    Get {output_result_candidate ?},
    Check whether all factual claims are supported by sources.

    Output JSON:
    {
      "groundedness_score": 0.0-1.0,
      "unsupported_claims": []
    }

    Use the 'save_attribute_to_state' Store the output strict JSON to state with key = 'groundedness_result'
    """,
    tools=[save_attribute_to_state]
)

pii_risk_agent = Agent(
    name="pii_risk_agent",
    description="Provide pii_risk_result",
    instruction="""
    Get {output_result_candidate ?}, Identify unnecessary or excessive PII in the draft.

    Output JSON:
    {
      "pii_risk": 0.0-1.0,
      "issues": []
    }

    Use the 'save_attribute_to_state' Store the output strict JSON to state with key = 'pii_risk_result'
    """,
    tools=[save_attribute_to_state]
)


quality_gate_agent = Agent(
    name="quality_gate_agent",
    instruction="""
    
    Combine   { policy_guard_result? }, { groundedness_result? }, { pii_risk_result? } evaluation results.

    PASS only if:
    - consent_ok = true
    - policy_score ≥ 0.95
    - groundedness_score ≥ 0.9
    - pii_risk ≤ 0.1

    Output:
    { "decision": "PASS" | "FAIL", "reason": "" }

    Use the 'save_attribute_to_state' Store the output decision to state with key = 'quality_gate_result'
    """,
    tools=[save_attribute_to_state]
)

# Instructions and tools are not permitted for SequentialAgent
guardrail_agent = SequentialAgent(
  name="guardrail_agent",
  description="""
  Get {output_result_candidate ?}, check the content by iterating through subagents to get policy_guard_result, groundedness_result and pii_risk_result then use quality_gate_agent to make guardrail decision
  """,
  # instruction="""
  # Iterates through subagents to get policy_guard_result, groundedness_result and pii_risk_result then use quality_gate_agent to make guardrail decision.
  # Store the guradrail result (PASS/FAIL)to to state with key = 'QulityGate'
  # """,
  sub_agents=[
    policy_guard_agent,
    groundedness_agent,
    pii_risk_agent,
    quality_gate_agent
  ],
  # tools=[save_attribute_to_state]

)




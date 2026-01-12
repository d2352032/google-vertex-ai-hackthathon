from google.adk import Agent

policy_guard_agent = Agent(
    name="policy_guard_agent",
    model="gemini-2.5-pro",
    instruction="""
    You are a policy compliance agent.

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
    """
)

groundedness_agent = Agent(
    name="groundedness_agent",
    instruction="""
    Check whether all factual claims are supported by sources.

    Output JSON:
    {
      "groundedness_score": 0.0-1.0,
      "unsupported_claims": []
    }
    """
)

quality_gate_agent = Agent(
    name="quality_gate_agent",
    instruction="""
    Combine evaluation results.

    PASS only if:
    - policy_score ≥ 0.95
    - groundedness_score ≥ 0.9
    - pii_risk ≤ 0.1

    Output:
    { "decision": "PASS" | "FAIL", "reason": "" }
    """
)

pii_agent = Agent(
    name="pii_agent",
    instruction="""
    Identify unnecessary or excessive PII in the draft.

    Output JSON:
    {
      "pii_risk": 0.0-1.0,
      "issues": []
    }
    """
)



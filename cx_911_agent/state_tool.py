from typing import List
from google.adk.tools import ToolContext

def save_attribute_to_state(
    tool_context: ToolContext,
    key: str,
    value: str
) -> dict[str, str]:
    """Saves the values to state[key].

    Returns: message about state storing
    """
    # Load existing attractions from state. If none exist, start an empty map
    existing_attractions = tool_context.state.get(key, "")

    tool_context.state[key] = value

    # A best practice for tools is to return a status message in a return dict
    return {"status": "{key}:{value} saved to state success}"}
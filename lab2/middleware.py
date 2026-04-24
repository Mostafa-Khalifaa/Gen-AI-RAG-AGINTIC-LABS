from langchain.agents.middleware import before_agent
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langchain.messages import ToolMessage, RemoveMessage
 
@before_agent
def trim_messages(state:AgentState, runtime:Runtime)->AgentState:
    """ remove all tool messages from the state """
    messages = state['messages']
    trimmed_messages = [msg for msg in messages if not isinstance(msg, ToolMessage)]
    return {'messages': trimmed_messages}
 
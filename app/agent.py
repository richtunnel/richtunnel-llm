from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.llm import get_llm
from app.tools import tools

llm = get_llm(temperature=0)

# In-memory checkpointer — swap for SqliteSaver/PostgresSaver to persist across restarts.
checkpointer = MemorySaver()

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer,
)


def run_agent(message: str, session_id: str) -> str:
    """Run one turn of the agent for a given session, with memory keyed on session_id."""
    config = {"configurable": {"thread_id": session_id}, "recursion_limit": 15}
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config,
    )
    return result["messages"][-1].content

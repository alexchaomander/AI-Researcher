from litellm.types.utils import ChatCompletionMessageToolCall, Function

from research_agent.inno.core import MetaChain
from research_agent.inno.types import Result


def echo_tool(text: str):
    return Result(value=f"echo:{text}")


def test_metachain_handles_tool_calls():
    mc = MetaChain(log_path=None)
    tool_call = ChatCompletionMessageToolCall(
        id="toolcall-1",
        type="function",
        function=Function(name="echo_tool", arguments='{"text": "hello"}'),
    )

    response = mc.handle_tool_calls(
        tool_calls=[tool_call],
        functions=[echo_tool],
        context_variables={},
        debug=False,
    )

    assert response.messages, "Expected a tool response message"
    tool_message = response.messages[0]
    assert tool_message["role"] == "tool"
    assert tool_message["content"] == "echo:hello"

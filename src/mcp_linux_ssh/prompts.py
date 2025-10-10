from mcp.server.fastmcp.prompts import base

from .server import mcp


@mcp.prompt(title="System error")
def system_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error or my RHEL system:"),
        base.UserMessage(error),
        base.UserMessage("Please help me troubleshoot the problem."),
    ]

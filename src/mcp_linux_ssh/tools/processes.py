from mcp.types import ToolAnnotations

from ..server import mcp
from ..utils import SSH

@mcp.tool(
    title="Get running process",
    description="List all processes on a system sorted in descending order by CPU",
    annotations=ToolAnnotations(readOnlyHint=True),
)
def get_processes(host: str):
    command = "ps -ef --sort=-%cpu"
    return SSH.run(host, command)

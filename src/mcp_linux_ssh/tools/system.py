from mcp.types import ToolAnnotations

from ..server import mcp
from ..utils import SSH


@mcp.tool(
    title="Service status",
    description="Get details on a systemd unit",
    annotations=ToolAnnotations(readOnlyHint=True),
)
def get_service_status(host: str, unit: str):
    command = f"systemctl --no-pager status {unit}"
    return SSH.run(host, command)


@mcp.tool(
    title="CPU information",
    description="Get detailed information about system CPUs",
    annotations=ToolAnnotations(readOnlyHint=True),
)
def get_cpu_info(host: str):
    command = "lscpu; cat /proc/cpuinfo"
    return SSH.run(host, command)


@mcp.tool(
    title="Disk information",
    description="Get details about the system filesystems and free space",
    annotations=ToolAnnotations(readOnlyHint=True),
)
def get_disk_info(host: str):
    command = "findmnt -l; findmnt --df"
    return SSH.run(host, command)

import shlex
import sys
import typing as t

from mcp.server.fastmcp import FastMCP

from mcp_linux_ssh.logging import setup_logging_to_file
from mcp_linux_ssh.utils import SSH

logger = setup_logging_to_file()
mcp = FastMCP(
    name="Linux SSH",
    instructions="",
)


class MCPError(Exception):
    def __init__(self, msg: str = ""):
        self.msg = msg


@mcp.tool(
    title="Run SSH read only",
    description="""
    Only run commands that would not make changes to the system.
    sudo is not allowed.

    When using systemctl, make sure to add --no-pager to prevent the command
    from hanging.
    """,
)
async def run_ssh_read_only(
    host: str,
    command: str,
) -> dict[str, t.Any]:
    """Run an SSH command on a remote host."""

    if "sudo" in shlex.split(command):
        logger.error(f"Refusing to run command with sudo: {command}")
        raise MCPError(
            "Found sudo in command. Running commands with sudo is not allowed."
        )

    return SSH.run(host, command)


@mcp.tool(
    title="Run SSH",
    description="""
    This command could make changes to the system. Care should be taken
    to not disable ssh or modify files such as /etc/sudoers, etc/password,
    or /etc/shadow so as to render tho system inaccessible.

    It can use sudo but should not prompt for password input. The sudo settings
    shoould allow passwordless sudo on the remote machine.

    When using systemctl, make sure to add --no-pager to prevent the command
    from hanging.
    """,
)
async def run_ssh(
    host: str,
    command: str,
) -> dict[str, t.Any]:
    """Run an ssh command on a remote host with elevated priviliges."""
    return SSH.run(host, command)


def main():
    logger.info("Starting Linux MCP Server")
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Shutting down Linux MCP server")
        sys.exit()


if __name__ == "__main__":
    main()

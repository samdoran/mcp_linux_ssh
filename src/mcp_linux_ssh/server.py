import dataclasses
import shutil
import subprocess
import sys
import typing as t

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context

from mcp_linux_ssh.logging import setup_logging_to_file

mcp = FastMCP("Linux SSH")
file_logger = setup_logging_to_file()


class MCPError(Exception):
    def __init__(self, msg: str = ""):
        self.msg = msg


@dataclasses.dataclass
class SSHCommand:
    bin: str | None = None

    def build_ssh_options(self) -> list[str]:
        ssh_options = {
            "ControlPersist": "yes",
            "StrictHostKeyChecking": "no",
            "UserKnownHostsFile": "/dev/null",
        }

        return [
            arg
            for key, value in ssh_options.items()
            for arg in ("-o", f"{key}={value}")
        ]  # fmt: skip

    def build_ssh_command(self, host: str, command: str) -> list[str]:
        opts = self.build_ssh_options()
        ssh_command = [self.bin, "-tt", *opts, host, command, "; sleep 0"]

        return ssh_command

    def __post_init__(self):
        if self.bin is None:
            self.bin = shutil.which("ssh") or "/usr/bin/ssh"


SSH = SSHCommand()


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
    context: Context,
) -> dict[str, t.Any]:
    """Run an SSH command on a remote host."""
    if command.casefold().startswith("sudo"):
        raise MCPError(
            "Found sudo in command. Running commands with sudo is not allowed."
        )

    ssh_command = SSH.build_ssh_command(host, command)

    file_logger.info(f"Running {command} on {host}")

    result = subprocess.run(ssh_command, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


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
    context: Context,
) -> dict[str, t.Any]:
    """Run an ssh command on a remote host with elevated priviliges."""
    ssh_command = SSH.build_ssh_command(host, command)
    file_logger.info(f"Running {command} on {host}")
    file_logger.debug(ssh_command)

    result = subprocess.run(ssh_command, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    logger.info("Starting Linux MCP Server")
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Shutting down Linux MCP server")
        sys.exit()


if __name__ == "__main__":
    main()

import shutil
import subprocess
import typing as t

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Linux SSH")


class MCPError(Exception):
    def __init__(self, msg: str = ""):
        self.msg = msg


def build_ssh_options() -> list[str]:
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


def build_ssh_command(host: str, command: str) -> list[str]:
    opts = build_ssh_options()
    ssh_command = [shutil.which("ssh"), "-tt", *opts, host, command, "; sleep 0"]

    return ssh_command


@mcp.tool(title="Run SSH read only")
def run_ssh_read_only(host: str, command: str) -> dict[str, t.Any]:
    """Run an SSH command on a remote host.

    Only run commands that would not make changes to the system.
    sudo is not allowed.
    """
    if command.casefold().startswith("sudo"):
        raise MCPError(
            "Found sudo in command. Running commands with sudo is not allowed."
        )

    ssh_command = build_ssh_command(host, command)

    result = subprocess.run(ssh_command, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@mcp.tool(title="Run SSH")
def run_ssh(host: str, command: str) -> dict[str, t.Any]:
    """Run an ssh command on a remote host with elevated priviliges.

    This command could make changes to the system. Care should be taken
    to not disable ssh or modify files such as /etc/sudoers, etc/password,
    or /etc/shadow so as to render tho system inaccessible.

    It can use sudo but should not prompt for password input. The sudo settings
    shoould allow passwordless sudo on the remote machine.
    """
    ssh_command = build_ssh_command(host, command)

    result = subprocess.run(ssh_command, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

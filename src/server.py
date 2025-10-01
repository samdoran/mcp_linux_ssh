import json
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
@mcp.tool()
def run_ssh(host: str, command: str) -> dict[str, t.Any]:
    """Run an SSH command on a remote host"""
    ssh_command = [shutil.which("ssh"), "-tt", host, command]

    result = subprocess.run(ssh_command, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    print("Running server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

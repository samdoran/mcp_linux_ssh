import dataclasses
import shlex
import shutil
import subprocess
import typing as t

from .logging import setup_logging_to_file

logger = setup_logging_to_file()


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
        ssh_command = [self.bin, "-tt", *opts, host, *shlex.split(command), "; sleep 0"]

        return ssh_command

    def run(self, host: str, command: str) -> dict[str, t.Any]:
        logger.info(f"Running {command} on {host}")
        ssh_command = self.build_ssh_command(host, command)
        result = subprocess.run(ssh_command, capture_output=True, text=True)

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def __post_init__(self):
        if self.bin is None:
            self.bin = shutil.which("ssh") or "/usr/bin/ssh"


SSH = SSHCommand()

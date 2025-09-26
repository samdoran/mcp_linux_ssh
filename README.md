# MCP Server to run commands over SSH #

⚠️ This is an early prototype. Use at your own risk. ⚠️

## Getting started ###

```
python -m venv .venvs/mcp
.venvs/mcp/bin/python -m pip install -e .
```

Run the MCP server with `.venvs/mcp/bin/mcp-linux-ssh`

To have an MCP client run the application, point it at `realpath .venvs/mcp/bin/mcp-linux-ssh`.

Here's an example configuration for Claude Desktop:

```json
{
    "mcpServers": {
        "linux_ssh": {
            "command": "/Users/sdoran/Developer/mcp_linux_ssh/.venvs/mcp/bin/mcp-linux-ssh",
            "env": {
                "TMPDIR": "/tmp"
            }
        }
    }
}
```

### Create a standalone executable ###

Use [`shiv`][] to create portable executable.

```
mkdir build
shiv -o build/mcp_linux_ssh --console-script mcp-linux-ssh .
```


[`shiv`]: https://shiv.readthedocs.io/en/latest/

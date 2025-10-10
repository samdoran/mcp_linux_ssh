import sys

from mcp.server.fastmcp import FastMCP

from mcp_linux_ssh.logging import setup_logging_to_file

logger = setup_logging_to_file()
mcp = FastMCP(
    name="Linux SSH",
    instructions="",
)

from mcp_linux_ssh.tools import *  # noqa: E402, F403


def main():
    logger.info("Starting Linux MCP Server")
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Shutting down Linux MCP server")
        sys.exit()


if __name__ == "__main__":
    main()

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import smartrent
import os

# loads env variable
load_dotenv()

# naming our mcp server and init
mcp = FastMCP("smartrent-mcp-server")

# registers functions as an MCP tool
@mcp.tool()
def ping() -> str:
    """Test that the server is alive"""
    return "ARIA MCP server is running"

@mcp.tool()
async def get_api():
    return await smartrent.async_login(os.getenv("SMARTRENT_EMAIL"),
                                      os.getenv("SMARTRENT_PASSWORD"))



if __name__ == "__main__":
    mcp.run(transport="sse")
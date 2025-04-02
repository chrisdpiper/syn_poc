
import virtualenv
import os

from mcp.server.fastmcp import FastMCP

async def get_science_response(input: str) -> str:
    """Get response from a question
    Args:
        input: a string to ask
    """
    data = get_science(input)
    return data

# Initialize FastMCP server
mcp = FastMCP("dac_science")

# Attach tools
# mcp.add_tool(get_alerts, name="Get-Weather-Alerts", description="TOOL DESC")
mcp.add_tool(get_science_response)

if __name__ == "__main__":
    #Run the server
    venv_dir = os.path.join(os.path.expanduser("~"), ".venv")
    virtualenv.create_environment(venv_dir)
    from mcp_science import get_science
    mcp.run(transport='stdio')
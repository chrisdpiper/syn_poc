from mcp.server.fastmcp import FastMCP #pip indstall mcp

from mcp.server.fastmcp import FastMCP

async def get_dac_response(input: str) -> str:
    """Get response from a question
    Args:
        input: a string to ask
    """
    data = "input string:" +  input + "  response: this is a sample return string of my data prepared from a vector database" \
    "huge blob of text about science Science is a systematic discipline that builds and organises knowledge in the form of testable hypotheses and predictions about the universe.[1][2] Modern science is typically divided into two or three major branches:[3] the natural sciences (e.g., physics, chemistry, and biology), which study the physical world; and the social sciences (e.g., economics, psychology, and sociology), which study individuals and societies.[4][5] Applied sciences are disciplines that use scientific knowledge for practical purposes, such as engineering and medicine.[6][7][8] While sometimes referred to as the formal sciences, the study of logic, mathematics, and theoretical computer science (which study formal systems governed by axioms and rules)[9][10] are typically regarded as separate because they rely on deductive reasoning instead of the scientific method or empirical evidence as their main methodology."
    return data

# Initialize FastMCP server
mcp = FastMCP("dac")

# Attach tools
# mcp.add_tool(get_alerts, name="Get-Weather-Alerts", description="TOOL DESC")
mcp.add_tool(get_dac_response)

if __name__ == "__main__":
    #Run the server
    mcp.run(transport='stdio')
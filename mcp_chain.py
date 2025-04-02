from textwrap import dedent
import httpx
from typing import Any
import logging
import time
import requests
import hashlib
import json
import os

from mcp_chain_tools import get_dac_events, get_dacs_owned


from mcp.server.fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("synovient")

# Attach tools
# mcp.add_tool(get_alerts, name="Get-Weather-Alerts", description="TOOL DESC")
mcp.add_tool(get_dacs_owned)
# mcp.add_tool(get_forecast, name="Get-Forecast", description="TOOL DESC")
mcp.add_tool(get_dac_events)

if __name__ == "__main__":
    #Run the server
    mcp.run(transport='stdio')
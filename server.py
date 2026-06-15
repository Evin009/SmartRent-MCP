from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from dotenv import load_dotenv
from tools.devices import fetch_devices_status, control_switch, control_lock, control_temperature
import os

# loads env variable
load_dotenv()

# naming our mcp server and init
mcp = FastMCP("smartrent-mcp-server", 
              host='0.0.0.0',
              port=(os.environ.get("PORT", 8000)),
              transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))

# registers functions as an MCP tool
@mcp.tool()
def ping() -> str:
    """Test that the server is alive"""
    return "ARIA MCP server is running"

# adding tool: getting device status
@mcp.tool()
async def get_device_status() -> str:
    """Get the current status of all SmartRent devices (locks, thermostat, switches, sensors)"""
    return await fetch_devices_status()

# adding tool: making switch control
@mcp.tool()
async def switch_control(name: str, action: str) -> str:
    """
    Turn a light switch on or off.
    name: partial or full name of the switch (e.g. 'bedroom', 'living room')
    action: 'on' or 'off'
    """
    return await control_switch(name, action)

# adding tool: making switch control
@mcp.tool()
async def lock_door(action: str) -> str:
    """
    Lock or unlock the front door.
    action: 'lock' or 'unlock'
    """
    return await control_lock(action)

# adding tool: temp control
@mcp.tool()
async def set_temperature(temperature: int, mode: str = "cool", unit: str = "F") -> str:
    """
    Set thermostat temperature and mode.
    temperature: the temperature value
    mode: 'cool', 'heat', 'auto', or 'off'
    unit: 'F' for farenheit (default) or 'C' for celcius
    """
    return await control_temperature(temperature, mode, unit)
    



if __name__ == "__main__":
    mcp.run(transport="sse")
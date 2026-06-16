# SmartRent MCP

An MCP (Model Context Protocol) server that lets Claude control your SmartRent smart home devices — locks, thermostat, switches, and sensors.

## Requirements

- A SmartRent account with devices set up (this only works if your building uses SmartRent hardware)
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) installed

## Setup

### 1. Add to Claude Desktop config

Open your `claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "smartrent-mcp": {
      "command": "uvx",
      "args": ["smartrent-mcp"],
      "env": {
        "SMARTRENT_EMAIL": "your_smartrent_email",
        "SMARTRENT_PASSWORD": "your_smartrent_password"
      }
    }
  }
}
```

### 2. Restart Claude Desktop

Fully quit (Cmd+Q on Mac) and reopen.

### 3. Try it

Ask Claude: *"What's the status of my home?"*

## Available Tools

- `ping` — test the server is alive
- `get_device_status` — read all devices (locks, thermostat, switches, sensors)
- `switch_control` — turn lights on/off by name
- `lock_door` — lock or unlock your front door
- `set_temperature` — set thermostat temperature, mode, and unit (F/C)

## Built With

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [smartrent-py](https://github.com/ZacheryThomas/smartrent-py)

## License

MIT

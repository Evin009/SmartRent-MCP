# SmartRent MCP

[![PyPI version](https://img.shields.io/pypi/v/smartrent-mcp.svg)](https://pypi.org/project/smartrent-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/smartrent-mcp.svg)](https://pypi.org/project/smartrent-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An [MCP](https://modelcontextprotocol.io) (Model Context Protocol) server that lets Claude control your [SmartRent](https://smartrent.com) smart home devices — locks, thermostat, light switches, and sensors — through natural conversation.

```
You: "Turn off the kitchen lights and lock the front door"
Claude: "Kitchen turned off. Front Door - Lock is now locked."
```

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup — Claude Desktop](#setup--claude-desktop)
- [Setup — Claude Web](#setup--claude-web)
- [Available Tools](#available-tools)
- [Self-Hosting (Remote / SSE mode)](#self-hosting-remote--sse-mode)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Built With](#built-with)
- [License](#license)

---

## Requirements

- A SmartRent account with devices already set up in the SmartRent app (this only works if your building/home uses SmartRent hardware — front door locks, thermostats, switches, or sensors)
- Python 3.10+
- Either [`uv`](https://docs.astral.sh/uv/) **or** `pip` — you likely already have one of these

---

## Installation

**Option A — using `uv` (recommended, no separate install step)**

If you don't have `uv` yet, install it once:

```bash
# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

That's it — `uvx` will download and run the package automatically the first time Claude needs it. No manual `install` command required.

**Option B — using plain `pip`**

```bash
pip install smartrent-mcp
```

---

## Setup — Claude Desktop

### 1. Open your Claude Desktop config file

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### 2. Add the server entry

**If you installed via `uv` (Option A):**

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

**If you installed via `pip` (Option B):**

```json
{
  "mcpServers": {
    "smartrent-mcp": {
      "command": "smartrent-mcp",
      "env": {
        "SMARTRENT_EMAIL": "your_smartrent_email",
        "SMARTRENT_PASSWORD": "your_smartrent_password"
      }
    }
  }
}
```

If you already have other servers under `"mcpServers"`, just add `"smartrent-mcp"` as another entry — don't replace the existing ones.

### 3. Restart Claude Desktop

Fully quit the app (Cmd+Q on Mac, or right-click the tray icon and Quit on Windows) and reopen it. Closing the window alone is not enough.

### 4. Try it

Ask Claude:

- *"What's the status of my home?"*
- *"Turn on the kitchen lights"*
- *"Lock the front door"*
- *"Set temperature to 72 cool mode"*

---

## Setup — Claude Web

Claude Web only connects to **remote** MCP servers over a URL — it cannot run local commands like `uvx`. To use this server with Claude Web, you need to self-host a remote instance. See [Self-Hosting](#self-hosting-remote--sse-mode) below, then add your deployed URL in Claude Web → Settings → MCP Servers.

---

## Available Tools

| Tool | Description | Parameters |
|---|---|---|
| `ping` | Test that the server is alive | none |
| `get_device_status` | Read the status of all devices — locks, thermostat, switches, sensors | none |
| `switch_control` | Turn a light switch on or off | `name` (e.g. `"kitchen"`), `action` (`"on"` / `"off"`) |
| `lock_door` | Lock or unlock the front door | `action` (`"lock"` / `"unlock"`) |
| `set_temperature` | Set thermostat temperature, mode, and unit | `temperature` (int), `mode` (`"cool"` / `"heat"` / `"auto"` / `"off"`, default `"cool"`), `unit` (`"F"` / `"C"`, default `"F"`) |

Device matching is partial and case-insensitive — `"dining"` will match a switch named `"Dining Room"`.

---

## Self-Hosting (Remote / SSE mode)

By default this package runs in **stdio mode** for local use with Claude Desktop. To run it as a remote, always-on server (for Claude Web or shared use), set the `TRANSPORT` environment variable:

```bash
TRANSPORT=sse SMARTRENT_EMAIL=you@example.com SMARTRENT_PASSWORD=yourpassword smartrent-mcp
```

This starts an HTTP/SSE server (default port `8000`, override with `PORT`). Deploy it anywhere that runs Python — Railway, Render, Fly.io, etc. — with these environment variables set:

| Variable | Required | Description |
|---|---|---|
| `SMARTRENT_EMAIL` | Yes | Your SmartRent account email |
| `SMARTRENT_PASSWORD` | Yes | Your SmartRent account password |
| `TRANSPORT` | No | `stdio` (default) or `sse` |
| `PORT` | No | Port to listen on in `sse` mode (default `8000`) |

Once deployed, connect to it at `https://your-deployment-url/sse`.

---

## Troubleshooting

**"Invalid Host header" or connection refused on a remote deployment**
The server disables DNS rebinding protection by default to support remote access. If you've changed this, make sure `TransportSecuritySettings(enable_dns_rebinding_protection=False)` is set in `server.py`.

**Claude Desktop doesn't show any tools**
Make sure you fully quit and restarted the app (not just closed the window). Check the MCP logs:
- Mac: `~/Library/Logs/Claude/mcp-server-smartrent-mcp.log`
- Windows: `%APPDATA%\Claude\logs\mcp-server-smartrent-mcp.log`

**"Username or password was wrong"**
Verify your SmartRent credentials work by logging into the SmartRent mobile app with the same email/password.

**"No switch/lock/thermostat found on this account"**
Your SmartRent account needs the corresponding device type already set up in the SmartRent app.

---

## Security

Your SmartRent credentials are passed as environment variables directly to the server process and are never sent anywhere except SmartRent's own login API. They are not logged or stored by this package.

If you're self-hosting in `sse` mode, anyone with your server's URL can control your home — there is currently no authentication layer on remote mode. Keep your deployment URL private, or restrict network access to it.

---

## Built With

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [smartrent-py](https://github.com/ZacheryThomas/smartrent-py)
- [uv](https://docs.astral.sh/uv/)

## License

MIT

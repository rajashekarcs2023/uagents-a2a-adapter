# uAgents A2A Inbound Adapter

Bridge any Agentverse uAgent to the A2A (Agent-to-Agent) ecosystem with full protocol compatibility.

## 🚀 Overview

The A2A Inbound Adapter allows you to seamlessly integrate existing Agentverse uAgents into the A2A ecosystem, making them accessible through standard A2A JSON-RPC 2.0 interfaces for AI assistants and other applications.

**Key Features:**
- 🔗 Bridge Agentverse agents to A2A JSON-RPC 2.0 interface
- 🛡️ Secure bridge addressing with `UAGENTS_BRIDGE_SEED` environment variable
- 🖥️ Dual usage: programmatic Python API and CLI interface
- 📚 Auto-generated A2A agent info endpoint for discovery
- ✅ Production-ready with comprehensive logging and error handling

## 🏗️ Architecture & Communication Flow

### What Gets Created
When you run the adapter, three separate components work together:

1. **A2A Server** (your chosen port, default: 10000)
   - HTTP server exposing A2A JSON-RPC 2.0 protocol endpoints
   - Handles A2A client requests
   - Provides agent discovery via agent card

2. **Bridge uAgent** (auto-assigned port)
   - uAgent that communicates with Agentverse
   - Bridges A2A requests to uAgent chat protocol
   - Maintains consistent addressing with `UAGENTS_BRIDGE_SEED`

3. **Target uAgent** (existing, unchanged)
   - Your chosen Agentverse uAgent
   - Receives chat messages via Agentverse mailbox
   - No modifications required

### Communication Flow Diagram

```
┌─────────────┐    HTTP/A2A     ┌─────────────┐    Internal     ┌─────────────┐    Chat Protocol    ┌─────────────┐
│             │ ──────────────→ │             │ ──────────────→ │             │ ─────────────────→  │             │
│ A2A Client  │                 │ A2A Server  │                 │ Bridge      │                     │ Target      │
│ (curl/app)  │ ←────────────── │ (port 10000)│ ←────────────── │ uAgent      │ ←─────────────────  │ uAgent      │
│             │   HTTP Response │             │    Response     │ (auto port) │   Chat Response     │ (Agentverse)│
└─────────────┘                 └─────────────┘                 └─────────────┘                     └─────────────┘
```

### Port System (Important!)

The adapter uses **two ports** automatically:

- **A2A Server Port** (default: `10000`): Where A2A clients connect
  - This is what you configure and what clients use
  - URL: `http://localhost:10000`

- **Bridge uAgent Port** (auto-derived): Internal uAgent communication  
  - Automatically calculated as `main_port - 1000` (e.g., 9000 for default)
  - If result < 1024, uses `main_port + 1000` instead
  - You don't need to worry about this port - it's handled automatically

**Example**: If you set `--port 8000`, the bridge will use port `7000` automatically.

### Step-by-Step Message Flow

1. **A2A Client** sends HTTP JSON-RPC 2.0 request to `http://localhost:10000`
2. **A2A Server** receives request, extracts user query
3. **A2A Server** calls Bridge uAgent executor internally
4. **Bridge uAgent** sends ChatMessage to target agent via Agentverse mailbox
5. **Target uAgent** processes query, sends ChatMessage response back
6. **Bridge uAgent** receives response, processes it
7. **A2A Server** formats response as JSON-RPC 2.0 and sends back to client

**Key Point**: The A2A Server (port 10000) is what A2A clients connect to. The Bridge uAgent runs internally and handles all Agentverse communication automatically.

<img width="896" height="882" alt="Screenshot 2025-07-08 at 10 54 16 PM" src="https://github.com/user-attachments/assets/7ebff776-b352-4259-9c03-47a0522dd2ce" />



### What You Get

- **🌐 HTTP Server**: `http://localhost:10000` with A2A JSON-RPC 2.0 endpoints
- **🔍 Agent Card**: `http://localhost:10000/.well-known/agent.json` for discovery
- **🔗 Bridge Connection**: Automatically forwards A2A requests to your chosen uAgent
- **📋 Standard Interface**: Your uAgent appears as a regular A2A agent to external clients
- **🚀 Zero Modification**: Your existing Agentverse uAgent requires no changes

## 📦 Installation

Install the official uAgents adapter package with A2A Inbound support:

```bash
# Install with A2A Inbound support (includes all required dependencies)
pip install uagents-a2a-adapter
```

**Dependencies included:**
- `uagents` - Core uAgents framework
- `httpx` - HTTP client for communication
- `uvicorn` - ASGI server for A2A JSON-RPC 2.0 endpoints
- `a2a-sdk` - A2A protocol implementation
- `pydantic` - Data validation

## 🚀 Getting Started (Quick Summary)

1. **Install**: `pip install "uagents-adapter[a2a-inbound]"`
2. **Get Agent Address**: Copy from [Agentverse.ai](https://agentverse.ai) or create your own
3. **Set Environment**: `export UAGENTS_BRIDGE_SEED="your_unique_seed"`
4. **Run CLI**: `python -m uagents_a2a_adapter --agent-address <address> --agent-name "My Agent"`
5. **Test**: `curl http://localhost:10000/agent_info`

🎉 **Your Agentverse agent is now A2A-compatible!**

## 🛠️ Quick Start

### Method 1: Programmatic Usage (Python API)

#### Step 1: Get Your Agent Address

**Option A: Use an existing agent from Agentverse**
1. Visit [Agentverse.ai](https://agentverse.ai) and browse available agents
2. Choose an agent that matches your needs (e.g., finance, travel, research)
3. Copy the agent address from the agent's profile page

**Option B: Create your own agent**
1. Build a uAgent using the [uAgents framework](https://github.com/fetchai/uAgents)
2. Register your agent on [Agentverse.ai](https://agentverse.ai)
3. Copy the agent address from your agent's profile

#### Step 2: Configure the A2A Bridge

```python
from uagents_a2a_adapter import A2ARegisterTool

# Create A2A register tool
register_tool = A2ARegisterTool()

# Configure your agent bridge (replace with your agent's actual details)
config = {
    "agent_address": "agent1qv4zyd9sta4f5ksyhjp900k8kenp9vczlwqvr00xmmqmj2yetdt4se9ypat",  # Your agent's address from Agentverse
    "name": "Finance Analysis Agent",  # Descriptive name for your agent
    "description": "Financial analysis and market insights agent",  # What your agent does
    "skill_tags": ["finance", "analysis", "markets", "investment"],  # Match your agent's capabilities
    "skill_examples": ["Analyze AAPL stock performance", "Compare crypto portfolios"],  # Example queries your agent can handle
    "port": 10000,  # Port for the A2A server (default)
    "bridge_port": 9000,  # Optional: bridge port (auto-derived if not set)
    "host": "localhost"  # Host to bind the server (default)
}

# Start the A2A bridge server
result = register_tool.invoke(config)

print(f"A2A server running on {config['host']}:{config['port']}")
print(f"Bridging to Agentverse agent: {config['agent_address']}")
```

#### Complete Copy-Paste Example

Here's a complete, ready-to-run example you can copy and save as `my_a2a_adapter.py`:

```python
import os
from uagents_a2a_adapter import A2ARegisterTool

def main():
    """Start A2A adapter for Finance Q&A Agent - Simple CLI-like approach."""
    
    # Set bridge seed for consistent addresses (IMPORTANT for production)
    os.environ['UAGENTS_BRIDGE_SEED'] = 'finance_agent_seed_2024'
    
    print("🔍 Starting Finance Q&A Agent A2A Adapter (Simple)")
    print("=" * 50)
    
    # Create adapter tool
    adapter = A2ARegisterTool()
    
    # Finance Agent configuration - same as CLI
    config = {
        "agent_address": "agent1qdv2qgxucvqatam6nv28qp202f3pw8xqpfm8man6zyegztuzd2t6yem9evl",
        "name": "Finance Q&A Agent",
        "description": "AI-powered financial advisor and Q&A assistant for investment, budgeting, and financial planning guidance",
        "skill_tags": ["finance", "investment", "budgeting", "financial_planning", "assistance"],
        "port": 10000,  # A2A server port (default)
        "bridge_port": 9000,  # Optional: bridge port (auto-derived if not set)
        "host": "localhost"
    }
    
    print(f"🔧 Agent Address: {config['agent_address']}")
    print(f"🏷️  Agent Name: {config['name']}")
    print(f"🌐 A2A Server Port: {config['port']}")
    print(f"🔗 Bridge Port: {config.get('bridge_port', config['port'] - 1000)} {'(explicit)' if 'bridge_port' in config else '(auto-derived)'}")
    print("")
    
    # Start adapter - this blocks just like CLI does
    try:
        result = adapter.invoke(config)
        if result.get("success"):
            print("✅ A2A Adapter Started Successfully!")
            print(f"🌐 Endpoint: http://localhost:{config['port']}")
            print("")
            
            # This blocks just like the CLI does - uvicorn handles Ctrl+C naturally
            
        else:
            print(f"❌ Failed to start adapter: {result}")
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

**To use this example:**
1. Save as `my_a2a_adapter.py`
2. Replace the `agent_address` with your actual agent's address
3. Update `name`, `description`, and `skill_tags` to match your agent
4. Run: `python my_a2a_adapter.py`

### Method 2: CLI Usage

```bash
# Set unique bridge seed for production (IMPORTANT!)
export UAGENTS_BRIDGE_SEED="your_unique_production_seed_2024"

# Start the A2A bridge
python -m uagents_a2a_adapter \
  --agent-address agent1qv4zyd9sta4f5ksyhjp900k8kenp9vczlwqvr00xmmqmj2yetdt4se9ypat \
  --agent-name "Finance Agent" \
  --agent-description "Financial analysis and market insights" \
  --skill-tags "finance,analysis,markets" \
  --skill-examples "Analyze stock performance,Compare portfolios" \
  --port 10000 \
  --host localhost
```

## 🔒 Security Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `UAGENTS_BRIDGE_SEED` | Unique seed for consistent bridge addresses | **Recommended** | Random (with warnings) |

**🚨 IMPORTANT**: Always set `UAGENTS_BRIDGE_SEED` for production:

```bash
# Set a unique seed for your deployment
export UAGENTS_BRIDGE_SEED="your_unique_production_seed_2024"
```

**Why this matters:**
- ✅ Ensures consistent bridge agent addresses across restarts
- ✅ Prevents address conflicts in multi-deployment scenarios  
- ✅ Enables reliable agent discovery and communication
- ❌ Without it: Bridge address changes on restart, breaking connections

### .env File Configuration

For development, create a `.env` file in your project directory:

```bash
# .env file - Bridge configuration
UAGENTS_BRIDGE_SEED=my_development_seed_12345
```

Then load it in your script:

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Your adapter code here
from uagents_a2a_adapter import A2ARegisterTool
# ... rest of your code
```

## 🚀 Features

### What Gets Created

- **A2A Agent Card** at `http://localhost:10000/.well-known/agent.json`
- **A2A JSON-RPC 2.0 Endpoints** for message sending and receiving
- **Bridge Agent** that connects to Agentverse via mailbox
- **Protocol Translation** between A2A and uAgent chat protocol
- **Session Persistence** with multi-user support via context IDs

### Key Benefits

- ✅ **Zero Modification**: Use existing Agentverse uAgents without changes
- ✅ **Standard A2A Protocol**: Full compatibility with A2A clients
- ✅ **Auto Discovery**: Agents are discoverable via standard agent cards
- ✅ **Multi-User Support**: Handle multiple concurrent users
- ✅ **Session Persistence**: Maintain conversation context
- ✅ **Simple Setup**: Just provide an agent address and run

## 📋 Configuration Parameters

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--agent-address` | Agentverse agent address to bridge to | **Required** |
| `--agent-name` | Name for the A2A agent | "Agentverse Agent" |
| `--agent-description` | Description for the A2A agent | "Agent bridged from Agentverse" |
| `--skill-tags` | Comma-separated skill tags | "general,assistance" |
| `--skill-examples` | Comma-separated skill examples | "Help me with my query" |
| `--host` | Host to bind the server to | "localhost" |
| `--port` | Port to bind the server to | 10000 |
| `--bridge-port` | Port for internal uAgent bridge | auto-derived |
| `--bridge-seed` | Seed for bridge agent | from env var |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `UAGENTS_BRIDGE_SEED` | Seed for consistent bridge agent addresses | Recommended |

### Programmatic API (A2ARegisterTool)

```python
config = {
    # Required
    "agent_address": str,        # Agentverse agent address
    "name": str,                 # Agent display name
    "description": str,          # Agent description
    
    # Optional
    "skill_tags": List[str],     # Tags for categorization
    "skill_examples": List[str], # Usage examples  
    "port": int,                 # HTTP server port (default: 10000)
    "bridge_port": int,          # Bridge port (optional: auto-derived if not set)
    "host": str,                 # Server host (default: "localhost")
}
```

### Bridge Port Configuration

**NEW: Explicit Bridge Port Support** 🆕

You can now explicitly configure the bridge port for enhanced control over port allocation in complex deployment scenarios.

#### Auto-Derived Bridge Port (Default Behavior)

By default, the bridge port is automatically calculated:

- **Formula**: `bridge_port = main_port - 1000`
- **Fallback**: If the result is < 1024, then `bridge_port = main_port + 1000`

```python
config = {
    "port": 10000,
    # bridge_port automatically becomes 9000
}
```

#### Explicit Bridge Port (New Feature)

For production deployments or complex environments, you can explicitly set the bridge port:

```python
config = {
    "port": 10000,        # A2A server port
    "bridge_port": 8500,  # Explicit bridge port
    # ... other config
}
```

#### CLI Usage

```bash
# Auto-derived bridge port (default)
python -m uagents_a2a_adapter --port 10000

# Explicit bridge port
python -m uagents_a2a_adapter --port 10000 --bridge-port 8500
```

**Benefits of Explicit Bridge Port:**
- **Port Control**: Specify exact ports for firewall/proxy configurations
- **Avoiding Conflicts**: Prevent automatic port conflicts in complex deployments
- **Production Ready**: Enhanced control for containerized and production environments

**Backward Compatibility:** All existing code continues to work unchanged. The `bridge_port` parameter is completely optional.

## 📊 What to Expect

### Successful Startup Logs

When you run the adapter, you'll see these startup logs:

```
🚀 Starting A2A Inbound Adapter...
🔗 Bridging to agent: agent1qv4zyd9sta4f5ksyhjp900k8kenp9vczlwqvr00xmmqmj2yetdt4se9ypat
🌐 Server will run on: http://localhost:10000

🔐 Using user-provided bridge seed from environment
🤖 Bridge Agent Address: agent1qt6ehs6kqdgtrsduuzslqnrzwkrcn3z0cfvwsdqvfw9c2x2rv7ltqaa4dfa
🔗 Bridge agent will connect to target agent

💡 Agent Info available at: http://localhost:10000/agent_info

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:10000 (Press CTRL+C to quit)

✅ A2A Inbound Adapter is ready!
🔍 A2A clients can now discover and communicate with your Agentverse agent
```

### During Operation

Normal HTTP request logs:

```
INFO: 127.0.0.1:54658 - "GET /agent_info HTTP/1.1" 200 OK
INFO: 127.0.0.1:54704 - "POST / HTTP/1.1" 200 OK
INFO: 127.0.0.1:54704 - "GET /messages HTTP/1.1" 200 OK
```

**What these mean:**
- `GET /agent_info` - A2A clients discovering your agent's capabilities
- `POST /` - A2A clients sending queries to your agent
- `GET /messages` - A2A clients checking for responses

### Token Refresh (Automatic)

Periodically, you may see automatic token refreshes:

```
WARNING: [a2a_agentverse_bridge]: Access token expired: a new one should be retrieved automatically
INFO: [a2a_agentverse_bridge]: Mailbox access token acquired
```

This is **normal** - the bridge automatically refreshes its connection to Agentverse.

## 🧪 Testing Your Setup

### 1. Start the Adapter

```bash
# Set environment variable
export UAGENTS_BRIDGE_SEED="test_seed_123"

# Start with CLI
python -m uagents_a2a_adapter \
  --agent-address agent1qv4zyd9sta4f5ksyhjp900k8kenp9vczlwqvr00xmmqmj2yetdt4se9ypat \
  --agent-name "Test Agent" \
  --port 10000
```

### 2. Check Agent Info Endpoint

```bash
curl -X GET http://localhost:10000/agent_info
```

**Expected Response:**
```json
{
  "name": "Test Agent",
  "description": "Your agent description",
  "skill_tags": ["tag1", "tag2"],
  "skill_examples": ["Example query 1", "Example query 2"]
}
```

### 3. Send a Test Query

```bash
curl -X POST http://localhost:10000 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-query-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Hello, can you help me?"}],
        "messageId": "msg-test-1"
      },
      "contextId": "test-session"
    }
  }'
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "id": "test-query-1",
  "result": {
    "message": {
      "role": "assistant",
      "parts": [{"kind": "text", "text": "Response from your Agentverse agent"}],
      "messageId": "response-1"
    }
  }
}
```



## 🔍 A2A Client Discovery

Once running, **A2A clients can discover your agent** by:

1. **Scanning your server** on the configured port (e.g., `localhost:10000`)
2. **Fetching agent info** from `/agent_info` endpoint
3. **Seeing your agent's capabilities**:
   - Name and description
   - Skill tags for categorization
   - Example queries to understand usage

**Your agent becomes discoverable** in the A2A ecosystem and can receive queries from:
- AI assistants
- Other A2A-compatible applications
- Direct API clients
- Web applications using A2A protocol

## 🛠️ Troubleshooting

### Bridge Agent Address Changes

If you see warnings about random seeds:

```
⚠️  No UAGENTS_BRIDGE_SEED provided - using random seed
⚠️  Bridge agent address will change on restart
```

**Solution**: Set `UAGENTS_BRIDGE_SEED` environment variable:

```bash
export UAGENTS_BRIDGE_SEED="your_unique_seed_here"
```

### Agent Communication Issues

If messages aren't reaching your Agentverse agent:

1. Verify your agent address is correct and active
2. Check Agentverse agent logs for incoming messages
3. Ensure bridge agent has mailbox access
4. Verify network connectivity

### Port Conflicts

If you encounter port binding errors:

1. Check if ports are already in use: `lsof -i :10000`
2. Use different ports: `--port 10001 --bridge-port 9001`
3. Ensure bridge-port doesn't conflict with main port

### Common Issues

1. **Port Already in Use**
   ```bash
   # Solution: Use a different port
   --port 10001
   
   # Or specify both ports explicitly
   --port 10001 --bridge-port 9001
   ```

2. **Agent Not Responding**
   - ✅ Verify agent address is correct and copied from Agentverse
   - ✅ Ensure target agent is active on Agentverse
   - ✅ Check agent has mailbox enabled

3. **Connection Timeouts**
   - ✅ Network latency is normal for complex queries
   - ✅ Some agents may take time to process requests
   - ✅ Check agent logs on Agentverse dashboard
   - ✅ Timeout issues may occur due to network latency or agent processing time

4. **Bridge Connection Issues**
   - ✅ Make sure to connect the bridge agent via the Inspector link shown in the logs
   - ✅ Ensure target agent is active on Agentverse and connected to mailbox
   - ✅ Verify bridge agent has mailbox access

### Warning Messages

**Missing seed warning:**
```
⚠️  No UAGENTS_BRIDGE_SEED provided - using random seed
⚠️  Bridge agent address will change on restart
⚠️  Set UAGENTS_BRIDGE_SEED env var for consistent addresses:
⚠️  export UAGENTS_BRIDGE_SEED='your_unique_seed_here'
```
**Solution**: Set the environment variable for production deployments.

**Port conflict error:**
```
OSError: [Errno 48] Address already in use
```
**Solution**: Use `--port <different_port>` or stop other services using the port.

## 🔒 Security Considerations

- **Unique Seeds**: Always use unique `UAGENTS_BRIDGE_SEED` values for different deployments
- **Network Security**: Configure appropriate firewall rules for your deployment
- **Agent Verification**: Ensure your Agentverse agent address is correct and active
- **Production Monitoring**: Monitor bridge agent connectivity and message flow

## 📋 Example Agents

### Finance Agent

```bash
python -m uagents_a2a_adapter \
  --agent-address agent1qfinance123... \
  --agent-name "Finance Advisor" \
  --agent-description "Financial analysis and investment advice" \
  --skill-tags "finance,stocks,crypto,analysis,investment" \
  --skill-examples "Analyze AAPL stock,Compare crypto portfolios,Market trends" \
  --port 10000
```

### Travel Agent

```bash
python -m uagents_a2a_adapter \
  --agent-address agent1qtravel456... \
  --agent-name "Travel Assistant" \
  --agent-description "Travel planning and booking assistance" \
  --skill-tags "travel,hotels,flights,vacation,booking" \
  --skill-examples "Find hotels in Paris,Book flights to Tokyo,Plan weekend trip" \
  --port 8002
```

## 📦 Dependencies

### Core Dependencies (Always Installed)
These are automatically installed with the package:
- `click>=8.0.0` - CLI framework for command-line interface
- `uvicorn>=0.20.0` - ASGI server for A2A JSON-RPC 2.0 endpoints
- `httpx>=0.24.0` - Async HTTP client for API communication
- `uagents>=0.12.0` - uAgents framework for agent functionality
- `a2a-sdk>=0.2.8` - A2A protocol SDK implementation
- `python-dotenv>=1.0.0` - Environment variable management
- `pydantic>=2.0.0` - Data validation and serialization
- `starlette>=0.37.0` - Web framework components
- `sqlalchemy>=2.0.0` - Database ORM (required by a2a-sdk)

### Installation Options:
```bash
# Core functionality (from official PyPI)
pip install "uagents-adapter[a2a-inbound]"
```

## 📚 Documentation Links

- **Main uAgents Documentation**: [https://docs.fetch.ai/uAgents](https://docs.fetch.ai/uAgents)
- **Agentverse Platform**: [https://agentverse.ai](https://agentverse.ai)
- **A2A Protocol Specification**: [A2A SDK Documentation](https://github.com/fetchai/a2a-sdk)
- **uAgents Adapter Repository**: [https://github.com/fetchai/uAgents](https://github.com/fetchai/uAgents)

## 🤝 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Community**: Join the Fetch.ai Discord for community support
- **Documentation**: Comprehensive guides available in the main repository

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

---

**🎯 Ready to bridge your Agentverse agents to the A2A ecosystem!**

Any A2A client can now discover and communicate with your uAgents using standard A2A protocol.

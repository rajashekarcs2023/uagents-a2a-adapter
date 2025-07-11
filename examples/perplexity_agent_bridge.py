#!/usr/bin/env python3
"""
Example: Bridge a Perplexity Search Agent from Agentverse to A2A Protocol

This example shows how to take a Perplexity-powered search agent from Agentverse
and make it available via Google's Agent-to-Agent protocol.
"""

import os
from uagents_a2a_adapter import A2ARegisterTool

def main():
    """Start A2A bridge for Perplexity Search Agent."""
    
    # Set bridge seed for consistent agent identity (required in production)
    os.environ["UAGENTS_BRIDGE_SEED"] = "perplexity_bridge_seed_2024"
    
    # Configure the bridge
    config = {
        "agent_address": "agent1qgzd0c60d4c5n37m4pzuclv5p9vwsftmfkznksec3drux8qnhmvuymsmshp",
        "name": "Perplexity Search Agent",
        "description": "AI-powered web search and research assistant with real-time information access",
        "skill_tags": ["search", "research", "web", "ai", "information", "news"],
        "skill_examples": ["Search for latest AI news", "Research quantum computing trends", "Find information about climate change"],
        "port": 9002,
        "bridge_port": 8002,  # Explicit bridge port for uAgent communication
        "host": "localhost"
    }
    
    print(f"🚀 Starting A2A bridge for {config['name']}...")
    print(f"🌐 Available at: http://localhost:{config['port']}")
    print(f"🔗 Bridging to agent: {config['agent_address']}")
    print("")
    
    # Start the A2A bridge
    adapter = A2ARegisterTool()
    
    try:
        result = adapter.invoke(config)
        if result.get("success"):
            print("✅ A2A Bridge Started Successfully!")
            print("🧪 Test with: curl -X POST http://localhost:9002 -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"query\",\"params\":{\"query\":\"What are the latest developments in AI?\"},\"id\":1}'")
        else:
            print(f"❌ Failed to start bridge: {result}")
    except KeyboardInterrupt:
        print("\n👋 Shutting down bridge...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

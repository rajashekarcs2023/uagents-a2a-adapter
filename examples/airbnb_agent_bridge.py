#!/usr/bin/env python3
"""
Example: Bridge an Airbnb Search Agent from Agentverse to A2A Protocol

This example shows how to take an Airbnb property search agent from Agentverse
and make it available via Google's Agent-to-Agent protocol.
"""

import os
from uagents_a2a_adapter import A2ARegisterTool

def main():
    """Start A2A bridge for Airbnb Search Agent."""
    
    # Set bridge seed for consistent agent identity (required in production)
    os.environ["UAGENTS_BRIDGE_SEED"] = "airbnb_bridge_seed_2024"
    
    # Configure the bridge
    config = {
        "agent_address": "agent1qv4zyd9sta4f5ksyhjp900k8kenp9vczlwqvr00xmmqmj2yetdt4se9ypat",
        "name": "Airbnb Search Agent",
        "description": "AI-powered vacation rental search and property details assistant",
        "skill_tags": ["airbnb", "vacation", "rental", "travel", "accommodation", "booking"],
        "skill_examples": ["Find Airbnb rentals in Paris", "Search for vacation homes in Palo Alto", "Find pet-friendly rentals near the beach"],
        "port": 9001,
        "bridge_port": 8001,  # Explicit bridge port for uAgent communication
        "host": "localhost"
    }
    
    print(f"🚀 Starting A2A bridge for {config['name']}...")
    print(f"🌐 Available at: http://localhost:{config['port']}")
    print(f"🔗 Bridge Port: {config['bridge_port']} (explicit)")
    print(f"🏠 Bridging to agent: {config['agent_address']}")
    print("")
    
    # Start the A2A bridge
    adapter = A2ARegisterTool()
    
    try:
        result = adapter.invoke(config)
        if result.get("success"):
            print("✅ A2A Bridge Started Successfully!")
            print("🧪 Test with: curl -X POST http://localhost:9001 -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"query\",\"params\":{\"query\":\"Find Airbnb rentals near Palo Alto for 2 nights starting tomorrow\"},\"id\":1}'")
        else:
            print(f"❌ Failed to start bridge: {result}")
    except KeyboardInterrupt:
        print("\n🛑 Bridge stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Example: Bridge a Financial Analysis Agent from Agentverse to A2A Protocol

This example shows how to take a financial analysis agent from Agentverse
and make it available via Google's Agent-to-Agent protocol.
"""

import os
from uagents_a2a_adapter import A2ARegisterTool

def main():
    """Start A2A bridge for Financial Analysis Agent."""
    
    # Set bridge seed for consistent agent identity (required in production)
    os.environ["UAGENTS_BRIDGE_SEED"] = "finance_bridge_seed_2024"
    
    # Configure the bridge
    config = {
        "agent_address": "agent1qdv2qgxucvqatam6nv28qp202f3pw8xqpfm8man6zyegztuzd2t6yem9evl",
        "name": "Financial Analysis Expert",
        "description": "AI-powered financial analysis, stock insights, and investment recommendations",
        "skill_tags": ["finance", "stocks", "investment", "analysis", "portfolio"],
        "skill_examples": ["Analyze Apple stock performance", "Recommend portfolio allocation", "Compare tech stocks"],
        "port": 9004,
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
            print("🧪 Test with: curl -X POST http://localhost:10000 -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"query\",\"params\":{\"query\":\"Analyze Tesla stock\"},\"id\":1}'")
        else:
            print(f"❌ Failed to start bridge: {result}")
    except KeyboardInterrupt:
        print("\n👋 Shutting down bridge...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

"""
uAgents A2A Adapter - Bridge Fetch.ai uAgents with Google's Agent-to-Agent Protocol

This package provides adapters to make Fetch.ai uAgents compatible with Google's
Agent-to-Agent (A2A) protocol, enabling seamless integration between the two ecosystems.
"""

from .adapter import A2ARegisterTool

__version__ = "0.1.0"
__author__ = "Rajashekar Vennavelli"
__email__ = "rajashekar.vennavelli@fetch.ai"

__all__ = ["A2ARegisterTool"]

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-07-11

### Added
- Initial release of uAgents A2A Adapter
- A2ARegisterTool for bridging Fetch.ai uAgents with Google's Agent-to-Agent protocol
- CLI interface for easy deployment: `python -m uagents_a2a_adapter`
- Programmatic API for integration with existing Python applications
- Support for configurable bridge ports (auto-derived or explicit)
- Environment variable support for secure bridge seeds
- Comprehensive documentation with examples and troubleshooting
- Example scripts for Finance and Travel agents
- Production-ready packaging for PyPI distribution

### Features
- **Protocol Bridge**: Seamlessly connect Agentverse agents to A2A HTTP endpoints
- **Security**: Bridge seed management for consistent agent identities
- **Flexibility**: Both CLI and programmatic interfaces
- **Robustness**: Error handling, logging, and graceful shutdown
- **Documentation**: Complete setup guides and real-world examples

### Security
- Secure bridge seed handling via environment variables
- Best practices documentation for production deployments
- No hardcoded secrets or sensitive information

### Dependencies
- uagents >= 0.13.0
- uagents-core
- pydantic >= 2.0.0
- uvicorn >= 0.20.0
- a2a-python-sdk
- google-generativeai
- Plus standard web framework dependencies (FastAPI, Starlette, etc.)

### Examples
- Finance agent bridge with stock analysis capabilities
- Travel agent bridge with booking and planning features
- Complete JSON-RPC 2.0 test commands
- Environment setup and configuration examples

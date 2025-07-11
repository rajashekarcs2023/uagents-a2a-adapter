# Development Guide

This guide covers development setup, testing, and contributing to the uAgents A2A Adapter.

## Development Installation

### 1. Clone the Repository

```bash
git clone https://github.com/radhikadanda/uagents-a2a-adapter.git
cd uagents-a2a-adapter
```

### 2. Install in Development Mode

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 3. Verify Installation

```bash
# Test CLI access
python -m uagents_a2a_adapter --help

# Test programmatic access
python -c "from uagents_a2a_adapter import A2ARegisterTool; print('✅ Import successful')"
```

## Running Examples

### Finance Agent Example

```bash
cd examples
python finance_agent_bridge.py
```

### Travel Agent Example

```bash
cd examples
python travel_agent_bridge.py
```

## Testing

### Run Basic Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Manual Testing

```bash
# Set bridge seed
export UAGENTS_BRIDGE_SEED="dev_test_seed_123"

# Start a test bridge
python -m uagents_a2a_adapter \
  --agent-address agent1qtest123... \
  --agent-name "Test Agent" \
  --port 10000

# Test with curl (in another terminal)
curl -X POST http://localhost:10000 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"query","params":{"query":"Hello"},"id":1}'
```

## Code Quality

### Formatting

```bash
# Install formatting tools
pip install black isort

# Format code
black src/ tests/ examples/
isort src/ tests/ examples/
```

### Type Checking

```bash
# Install mypy
pip install mypy

# Run type checking
mypy src/uagents_a2a_adapter/
```

## Building and Distribution

### Build Package

```bash
# Install build tools
pip install build

# Build distribution packages
python -m build
```

### Local Installation from Build

```bash
# Install from local build
pip install dist/uagents_a2a_adapter-0.1.0-py3-none-any.whl
```

## Publishing to PyPI

### Test PyPI (Recommended First)

```bash
# Install twine
pip install twine

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ uagents-a2a-adapter
```

### Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

## Project Structure

```
uagents-a2a-adapter/
├── src/uagents_a2a_adapter/     # Main package source
│   ├── __init__.py              # Package exports
│   ├── adapter.py               # A2ARegisterTool implementation
│   ├── agentverse_executor.py   # Bridge executor logic
│   ├── cli.py                   # Command-line interface
│   └── __main__.py              # CLI entry point
├── tests/                       # Test files
├── examples/                    # Usage examples
├── pyproject.toml              # Modern Python packaging config
├── requirements.txt            # Dependency list
├── README.md                   # User documentation
├── DEVELOPMENT.md              # This file
├── CHANGELOG.md               # Version history
└── LICENSE                    # MIT license
```

## Contributing Guidelines

1. **Fork and Clone**: Fork the repo and clone your fork
2. **Branch**: Create a feature branch (`git checkout -b feature/amazing-feature`)
3. **Develop**: Make your changes with tests
4. **Format**: Run `black` and `isort` on your code
5. **Test**: Ensure all tests pass (`pytest`)
6. **Commit**: Make clear, descriptive commits
7. **Push**: Push to your fork
8. **PR**: Create a Pull Request with a clear description

## Common Development Tasks

### Adding New Features

1. Add implementation in `src/uagents_a2a_adapter/`
2. Add tests in `tests/`
3. Update documentation in `README.md`
4. Add examples if applicable
5. Update `CHANGELOG.md`

### Debugging Issues

1. Enable debug logging: `export PYTHONPATH=. && python -c "import logging; logging.basicConfig(level=logging.DEBUG)"`
2. Check bridge seed: `echo $UAGENTS_BRIDGE_SEED`
3. Verify agent addresses are valid
4. Test with curl commands

### Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v0.1.0`
4. Build: `python -m build`
5. Test on Test PyPI
6. Release on PyPI
7. Push tag: `git push origin v0.1.0`

## Getting Help

- **Issues**: Open GitHub issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact radhika@fetch.ai for urgent matters

## License

MIT License - see LICENSE file for details.

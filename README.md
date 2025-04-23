# Local MCP Client
Local MCP Client is a cross-platform web and API interface for interacting with configurable MCP servers using natural language, powered by Ollama and any local LLM of choice, enabling structured tool execution and dynamic agent behavior.

<br>

## Step 1a: Create Virtual Env & Install Requirements - MAC/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
cd Local_MCP_Client
uv init .
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Step 1b: Create Virtual Env & Install Requirements - Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
cd Local_MCP_Client
uv init .
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

## Step 2: Run MCP Client
```bash
uv run local_mcp_client.py
```

## Step 2: Run Tests
```
python -m unittest discover -s tests

uv pip install coverage==7.8.0
coverage run --branch -m unittest discover -s tests
coverage report -m
coverage html
open htmlcov/index.html  # MAC
xdg-open htmlcov/index.html  # Linux
start htmlcov\index.html  # Windows
coverage erase
```

<br>

## License
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

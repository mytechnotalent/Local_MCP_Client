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

## Step 2a: Install Ollama & Pull LLM Model - MAC
```bash
brew install ollama
ollama serve
ollama pull llama3:8b
```

## Step 2b: Install Ollama & Pull LLM Model - Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3:8b
```

## Step 2c: Install Ollama & Pull LLM Model - Windows
#### Download Ollama [HERE](https://ollama.com/download/windows)
```bash
ollama serve
ollama pull llama3:8b
```

## Step 3a: Clone MCP Servers - MAC/Linux
```bash
cd ~/Documents
git clone https://github.com/mytechnotalent/MalwareBazaar_MCP.git
git clone https://github.com/Invoke-RE/binja-lattice-mcp
```

## Step 3b: Clone MCP Servers - Windows
```bash
cd "$HOME\Documents"
git clone https://github.com/mytechnotalent/MalwareBazaar_MCP.git
git clone https://github.com/Invoke-RE/binja-lattice-mcp
```

## Step 4: Run Ollama
```bash
ollama serve
```

## Step 5a: Run MCP Client - MAC/Linux
```bash
export BNJLAT = "<your-binja-api-token>"
uv run local_mcp_client.py
```

## Step 5b: Run MCP Client - Windows
```bash
$env:BNJLAT = "<your-binja-api-token>"
uv run local_mcp_client.py
```

## Step 6: Run Tests
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

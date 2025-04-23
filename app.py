#!/usr/bin/env python3

"""
Local MCP Client

This script launches a local agent that connects to a Model Context Protocol (MCP) toolchain.
It provides two interfaces:
- Uses Ollama to work with a local LLM.
- A Gradio-powered web UI for interactive use.
- A FastAPI-based REST API for programmatic access (e.g., curl, automation).
"""

import os
import re
import json
import gradio as gr
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from praisonaiagents import Agent, MCP

# Load configuration from mcp_config.json
CONFIG_PATH = Path(__file__).parent / "mcp_config.json"
with CONFIG_PATH.open("r", encoding="utf-8") as f:
    config = json.load(f)


def choose_mcp_key(query: str) -> str:
    """
    Select MCP server key based on keywords in the query.

    Args:
        query (str): User input string.

    Returns:
        str: Key to select the appropriate MCP server.
    """
    for key, server in config["mcpServers"].items():
        if any(kw in query.lower() for kw in server.get("keywords", [])):
            return key
    return next(iter(config["mcpServers"]))


def create_agent(mcp_key: str = "MalwareBazaar") -> Agent:
    """
    Instantiate and return a configured PraisonAI Agent bound to the specified MCP server.

    Args:
        mcp_key (str): Key from mcpServers in config to use for binding.

    Returns:
        Agent: Ready-to-use MCP-enabled agent instance.
    """
    mcp_conf = config["mcpServers"][mcp_key]
    full_instructions = "\n".join(mcp_conf.get("instructions", []))
    return Agent(
        instructions=full_instructions,
        llm=config["llm"],
        tools=MCP(
            os.path.expanduser(mcp_conf["command"]),
            args=mcp_conf.get("args", []),
            cwd=os.path.expanduser(mcp_conf.get("cwd", "")),
            env=mcp_conf.get("env"),
        ),
    )


def auto_format_backticks(text: str) -> str:
    """
    Automatically wrap filenames, hashes, hex values, and symbol names in backticks.

    Args:
        text (str): Raw markdown.

    Returns:
        str: Cleaned markdown with backtick-wrapped tokens.
    """
    text = re.sub(r"\b([A-Za-z0-9_]+\.(exe|dll|bin|so))\b", r"`\1`", text)
    text = re.sub(r"\b([a-fA-F0-9]{64})\b", r"`\1`", text)
    text = re.sub(r"\b(0x[0-9a-fA-F]+)\b", r"`\1`", text)
    text = re.sub(r"\b(_[a-zA-Z0-9_]+)\b", r"`\1`", text)
    return text


def query_handler(query: str) -> tuple[str, str]:
    """
    Process a natural language query and return a formatted markdown response.

    Args:
        query (str): User question or prompt.

    Returns:
        tuple[str, str]: Formatted markdown response and cleared input.
    """
    mcp_key = choose_mcp_key(query)
    agent = create_agent(mcp_key)
    result = agent.start(query)

    if result is None:
        return (
            "## ❌ Error\n\nThe agent returned no result. There may have been an internal LLM error (likely a missing or malformed tool call). Check the logs for details.",
            "",
        )

    lines = result.splitlines()
    formatted = []
    buffer = []

    def flush_buffer():
        if buffer:
            formatted.append("\n".join(buffer))
            buffer.clear()

    for line in lines:
        if line.strip().startswith("{") and line.strip().endswith("}"):
            flush_buffer()
            formatted.append("```json\n" + line.strip() + "\n```")
        elif line.strip() == "" or re.match(r"^[*#-] ", line.strip()):
            flush_buffer()
            formatted.append(line)
        else:
            buffer.append(line)

    flush_buffer()
    final_markdown = auto_format_backticks(
        "## MCP Agent Response\n\n" + "\n".join(formatted)
    )
    return final_markdown, ""


# FastAPI app
app = FastAPI(title="Local MCP REST API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """
    Schema for incoming POST requests to /query endpoint.

    Attributes:
        query (str): The user question or command string.
    """

    query: str


@app.post("/query")
async def handle_query(req: QueryRequest):
    """
    Endpoint to handle POST /query calls and return MCP output.

    Args:
        req (QueryRequest): The request body containing a query string.

    Returns:
        JSONResponse: Structured result from the agent.
    """
    response, _ = query_handler(req.query)
    return JSONResponse(content={"response": response})


def clear_output() -> str:
    """
    Clears the markdown display in the Gradio UI.

    Returns:
        str: An empty string.
    """
    return ""


# Gradio UI
with gr.Blocks(
    title="Local MCP Client",
    css="""
        .wrap-markdown pre {
            overflow-x: auto;
            white-space: pre-wrap;
            background: #1e1e1e;
            color: #eee;
            padding: 0.75em;
            border-radius: 8px;
        }
    """,
) as demo:
    gr.Markdown(
        """# Local MCP Client\nEnter a natural language request. Press SHIFT+ENTER to submit."""
    )
    query_input = gr.Textbox(
        placeholder="e.g. Get latest MalwareBazaar SHA256 tags...",
        show_label=False,
        lines=3,
    )
    submit_btn = gr.Button("Submit")
    output_display = gr.Markdown(elem_classes=["wrap-markdown"])

    query_input.submit(
        fn=clear_output, inputs=[], outputs=[output_display], queue=False
    ).then(fn=query_handler, inputs=query_input, outputs=[output_display, query_input])
    submit_btn.click(
        fn=clear_output, inputs=[], outputs=[output_display], queue=False
    ).then(fn=query_handler, inputs=query_input, outputs=[output_display, query_input])

if __name__ == "__main__":
    import threading

    def launch_gradio():
        """
        Start the Gradio app on localhost:7860.
        This runs in a separate thread to allow FastAPI to launch in parallel.
        """
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

    threading.Thread(target=launch_gradio).start()
    uvicorn.run(app, host="0.0.0.0", port=7861)

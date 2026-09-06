"""
MCP Server for genpark-prompt-semantic-cache-similarity-dedup-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import SemanticPromptCacheClient

client = SemanticPromptCacheClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "lookup_cache",
                        "description": "Check semantic cache for similar cached prompt response.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string"},
                                "model": {"type": "string"}
                            },
                            "required": ["prompt"]
                        }
                    },
                    {
                        "name": "store_cache",
                        "description": "Store prompt and response in semantic cache.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {"type": "string"},
                                "response": {"type": "string"},
                                "model": {"type": "string"}
                            },
                            "required": ["prompt", "response"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "lookup_cache":
            res = client.lookup(args.get("prompt", ""), args.get("model"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "store_cache":
            client.store(args.get("prompt", ""), args.get("response", ""), args.get("model", "default"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "OK"}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()

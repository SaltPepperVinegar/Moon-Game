from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPOSITORY_ROOT / "tools" / "skills"
sys.path.insert(0, str(SKILLS_DIR))

from scaffold_domain import scaffold_domain  # noqa: E402


TOOL_SCHEMA: dict[str, Any] = {
    "name": "scaffold_domain",
    "description": "Scaffold a Moon Game gameplay domain under MoonGame/Assets/Scripts/Domains.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "domain_name": {
                "type": "string",
                "description": "PascalCase domain name, for example Combat.",
                "pattern": "^[A-Z][A-Za-z0-9]*$",
            },
            "core_guid": {
                "type": "string",
                "description": "32-character Unity GUID for MoonGame/Assets/Scripts/Core/Core.asmdef.",
                "pattern": "^[0-9a-fA-F]{32}$",
            },
        },
        "required": [
            "domain_name",
            "core_guid"
        ],
        "additionalProperties": False,
    },
}


def _send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _success(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
    }


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
        },
    }


def _handle(request: dict[str, Any]) -> dict[str, Any] | None:
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}

    if method == "initialize":
        return _success(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "moon-game-scaffold-domain",
                    "version": "1.0.0",
                },
            },
        )

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return _success(request_id, {})

    if method == "tools/list":
        return _success(request_id, {"tools": [TOOL_SCHEMA]})

    if method == "tools/call":
        if not isinstance(params, dict):
            return _error(request_id, -32602, "Invalid params")

        name = params.get("name")
        arguments = params.get("arguments") or {}

        if name != "scaffold_domain":
            return _error(request_id, -32601, f"Unknown tool: {name}")

        if not isinstance(arguments, dict):
            return _error(request_id, -32602, "Tool arguments must be an object")

        try:
            result = scaffold_domain(repository_root=REPOSITORY_ROOT, **arguments)
        except Exception as exc:
            payload = {"ok": False, "error": str(exc)}
            return _success(
                request_id,
                {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(payload, indent=2),
                        }
                    ],
                    "structuredContent": payload,
                    "isError": True,
                },
            )

        payload = {"ok": True, **result}
        return _success(
            request_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(payload, indent=2),
                    }
                ],
                "structuredContent": payload,
            },
        )

    if request_id is None:
        return None

    return _error(request_id, -32601, f"Method not found: {method}")


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError as exc:
            _send(_error(None, -32700, f"Parse error: {exc}"))
            continue

        if not isinstance(request, dict):
            _send(_error(None, -32600, "Invalid request"))
            continue

        response = _handle(request)
        if response is not None:
            _send(response)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

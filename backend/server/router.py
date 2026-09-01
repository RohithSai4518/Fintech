"""
Fintech HTTP Router & Dispatcher
Zero external library dependencies (pure Python standard library).
Handles URL routing, parameter extraction, CORS, and JSON response formatting.
"""

import json
import re
from typing import Callable, Dict, List, Tuple, Any, Optional


class HTTPResponse:
    """Encapsulates HTTP status, headers, and body payload."""

    def __init__(self, status: int = 200, body: Any = None, headers: Optional[Dict[str, str]] = None):
        self.status = status
        self.headers = headers or {"Content-Type": "application/json"}
        if isinstance(body, (dict, list)):
            self.body = json.dumps(body, indent=2).encode('utf-8')
        elif isinstance(body, str):
            self.body = body.encode('utf-8')
        elif isinstance(body, bytes):
            self.body = body
        else:
            self.body = b""


class Router:
    """Regex-based lightweight HTTP request router."""

    def __init__(self):
        self.routes: Dict[str, List[Tuple[re.Pattern, Callable, List[str]]]] = {
            "GET": [],
            "POST": [],
            "PUT": [],
            "DELETE": [],
            "OPTIONS": []
        }

    def add_route(self, method: str, path_pattern: str, handler: Callable) -> None:
        """Registers a route pattern, extracting named parameter groups."""
        # Convert path like "/api/accounts/:id" to regex r"^/api/accounts/(?P<id>[^/]+)$"
        regex_path = re.sub(r':([a-zA-Z_]+)', r'(?P<\1>[^/]+)', path_pattern)
        compiled = re.compile(f"^{regex_path}$")
        self.routes[method.upper()].append((compiled, handler, []))

    def dispatch(self, method: str, path: str, request_data: Dict[str, Any]) -> HTTPResponse:
        """Matches request path to handler and returns HTTPResponse."""
        method = method.upper()

        if method == "OPTIONS":
            return HTTPResponse(200, {"status": "ok"}, {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Idempotency-Key"
            })

        if method not in self.routes:
            return HTTPResponse(405, {"error": f"Method {method} not allowed"})

        for pattern, handler, _ in self.routes[method]:
            match = pattern.match(path)
            if match:
                path_params = match.groupdict()
                try:
                    res = handler(request_data, **path_params)
                    if isinstance(res, HTTPResponse):
                        return res
                    return HTTPResponse(200, res)
                except ValueError as ve:
                    return HTTPResponse(400, {"error": "Validation Error", "details": str(ve)})
                except Exception as ex:
                    return HTTPResponse(500, {"error": "Internal Server Error", "details": str(ex)})

        return HTTPResponse(404, {"error": f"Route not found: {method} {path}"})

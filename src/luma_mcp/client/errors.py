"""Errors safe to return to MCP callers without leaking request data."""


class LumaError(Exception):
    def __init__(
        self,
        code: str,
        *,
        status: int | None = None,
        retry_after: float | None = None,
        outcome_unknown: bool = False,
    ) -> None:
        super().__init__(code)
        self.details = {
            "code": code,
            "status": status,
            "retry_after": retry_after,
            "outcome_unknown": outcome_unknown,
        }

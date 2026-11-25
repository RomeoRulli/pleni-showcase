"""Fallback between two LLM providers (ADR 0003): Gemini first, Claude when it fails.

Excerpt from `app/llm/fallback.py`. Comments and log messages translated from Portuguese; code unchanged.

The switch happens per call, inside the tool loop: the fallback receives the same conversation (with the
tools already executed and their results), so no tool runs twice. A conversation that already holds a
message from the fallback stays on it until the end of the turn. The history stored between turns is
text only, so the next turn starts on the primary again.
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.llm.types import LLMProvider, LLMRequest, LLMResponse, OnSlow

logger = get_logger("llm.fallback")


class FallbackProvider:
    """`LLMProvider` that tries `primary` and, if it raises, repeats the call on `fallback`."""

    def __init__(self, primary: LLMProvider, fallback: LLMProvider) -> None:
        self._primary = primary
        self._fallback = fallback
        self.name = f"{primary.name}+{fallback.name}"

    async def aclose(self) -> None:
        try:
            await self._primary.aclose()
        finally:
            await self._fallback.aclose()

    async def generate(self, request: LLMRequest, on_slow: OnSlow | None = None) -> LLMResponse:
        if any(m.native_provider == self._fallback.name for m in request.messages):
            return await self._fallback.generate(request, on_slow=on_slow)
        try:
            return await self._primary.generate(request, on_slow=on_slow)
        except Exception as exc:
            logger.warning(
                "%s failed (%s); the same call goes to %s", self._primary.name, exc, self._fallback.name, exc_info=True
            )
        # Primary exhausted: the turn is already slow and still has to reach the fallback, so the user gets
        # the "just a moment" notice.
        if on_slow is not None:
            try:
                await on_slow()
            except Exception as exc:
                logger.warning("Non-fatal failure while telling the user about the delay: %s", exc, exc_info=True)
        return await self._fallback.generate(request, on_slow=on_slow)

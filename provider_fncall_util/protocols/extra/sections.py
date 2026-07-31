"""Shared prompt section assembly for tagged protocol prompts."""

from __future__ import annotations

from echotools.fncall.prompt.templates import (
    _HISTORY_CLARIFY_EN,
    _HISTORY_CLARIFY_ZH,
)


def join_tagged_sections(
    instruction: str,
    lang: str,
    user_system_prompt: str = "",
    history_text: str = "",
    loop_warning: str = "",
    history_markup_warning: str = "",
    current_user_message: str = "",
    *,
    empty_current_user: bool = False,
) -> str:
    """Append standard tagged context sections after an instruction block."""
    sections = [instruction]
    usp = (user_system_prompt or "").strip()
    if usp:
        sections.append(f"<user_system_prompt>\n{usp}\n</user_system_prompt>")
    if history_text:
        clarify = _HISTORY_CLARIFY_ZH if lang == "zh" else _HISTORY_CLARIFY_EN
        sections.append(
            f"<conversation_history>\n{clarify}\n\n{history_text}\n</conversation_history>"
        )
    if loop_warning:
        sections.append(f"<loop_warning>\n{loop_warning}\n</loop_warning>")
    if history_markup_warning:
        sections.append(
            f"<history_markup_warning>\n{history_markup_warning}\n</history_markup_warning>"
        )
    if current_user_message:
        sections.append(
            f"<current_user_message>\n{current_user_message}\n</current_user_message>"
        )
    elif empty_current_user:
        sections.append("<current_user_message>\n</current_user_message>")
    return "\n\n".join(sections)

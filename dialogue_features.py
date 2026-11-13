import re

STUBS: list[str] = ["Извините, я пока не могу помочь с этим вопросом."]

_PROFANITY_RE = re.compile(
    r"""
    (?i)
    (?<![а-яё])
    (?:
        (?:по|на|о|от|за|про|с)?ху[йеёяию]\w*
        |(?:рас|раз|про|о|от|вз|до|за|на|пере|вы|по|с)?п[иеё]зд\w*
        |бля(?:д\w*|ть|т)?(?![а-яё])
        |(?:долбо|за|на|по|под|про|пере|раз|вы|до|отъ?|объ?|взъ?|изъ?|при|съ|у)?[её]б\w*
        |су(?:к(?:а|и|е|у|ой|ами)|ч(?:ара\w*|ий\w*|ка\w*|ье\w*|ку|ки|ке))(?![а-яё])
        |пид[аое]?р\w*
        |муд(?:ак\w*|ач\w*|ил\w*|лан\w*|о\w*)
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def collect_dialogue_features(dialogue: dict) -> dict:
    """Собрать детерминированные признаки диалога."""
    history = dialogue["history"]
    text = "\n".join(message["content"] for message in history)
    return {
        "message_count": len(history),
        "has_stub": _has_stub(text),
        "has_profanity": _PROFANITY_RE.search(text) is not None,
    }


def _has_stub(text: str) -> bool:
    folded = text.casefold()
    return any(stub.casefold() in folded for stub in STUBS if stub)

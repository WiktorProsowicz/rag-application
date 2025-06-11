import re
from typing import Optional

from .google_api import official_token_count


def estimate_token_count(text: str) -> int:
    """Roughly estimate the number of tokens in *text*.

    The heuristic is based on word count, total characters,
    digits and punctuation density. It does not require any
    external tokenizer but should give values in the same
    order of magnitude as common language model tokenizers.
    """
    if not text:
        return 0

    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)

    char_count = len(text)

    digit_count = sum(c.isdigit() for c in text)
    punctuation_count = len(re.findall(r"[^\w\s]", text))

    avg_word_len = char_count / max(word_count, 1)

    estimate = word_count
    estimate += int(char_count / 25)
    estimate += int(digit_count / 3)
    estimate += int(punctuation_count / 3)

    if avg_word_len > 7:
        estimate += int((avg_word_len - 7) * 0.5 * word_count / 10)

    return max(1, estimate)


def _actual_token_count(text: str) -> Optional[int]:
    """Return the token count using tiktoken when available."""
    try:
        import tiktoken
    except Exception:
        return None

    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def google_token_count(text: str) -> Optional[int]:
    """Return the official token count using Google's API.

    If the Google Generative AI client is not available or the request fails,
    ``None`` is returned. This allows graceful degradation when the
    environment lacks credentials or network access.
    """
    return official_token_count(text)


if __name__ == "__main__":
    import sys

    input_text = " ".join(sys.argv[1:]) or "Hello world!"
    est = estimate_token_count(input_text)
    real = _actual_token_count(input_text)

    print(f"Text: {input_text!r}")
    print(f"Estimated tokens: {est}")
    if real is not None:
        print(f"Actual tokens: {real}")
    else:
        print("tiktoken not installed; cannot compute actual token count")


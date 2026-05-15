"""Generate MP3 voiceovers for all flashcards using edge-tts (free, no API key).

Parses the `allCards` JS array from index.html and writes one MP3 per card to
`card_audio/{file}.mp3`. Speaks "article word" (e.g. "de emmer") at a slightly
slowed rate for learning. Skips files that already exist.

Usage:
    python3 -m venv .venv && .venv/bin/pip install edge-tts
    .venv/bin/python generate_audio.py
"""

import asyncio
import re
from pathlib import Path

import edge_tts

VOICE = "nl-NL-FennaNeural"  # female, native Netherlands Dutch
RATE = "-10%"                 # slightly slower for learners
HTML = Path(__file__).parent / "index.html"
OUT_DIR = Path(__file__).parent / "card_audio"

CARD_RE = re.compile(
    r"file\s*:\s*'([^']+)'\s*,\s*"
    r"article\s*:\s*'([^']*)'\s*,\s*"
    r"word\s*:\s*'([^']+)'"
)


def parse_cards(html_text: str) -> list[tuple[str, str, str]]:
    """Return list of (file, article, word) tuples from the allCards block."""
    start = html_text.index("const allCards = [")
    end = html_text.index("];", start)
    return CARD_RE.findall(html_text[start:end])


def phrase(article: str, word: str) -> str:
    return f"{article} {word}".strip()


async def synth(text: str, dest: Path) -> None:
    comm = edge_tts.Communicate(text, VOICE, rate=RATE)
    await comm.save(str(dest))


async def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    cards = parse_cards(HTML.read_text())
    print(f"Found {len(cards)} cards, voice={VOICE}, rate={RATE}")

    skipped = generated = 0
    for file_name, article, word in cards:
        dest = OUT_DIR / f"{file_name}.mp3"
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        text = phrase(article, word)
        try:
            await synth(text, dest)
            generated += 1
            print(f"  {file_name:25} {text}")
        except Exception as e:
            print(f"  FAIL {file_name}: {e}")

    print(f"\nDone. Generated {generated}, skipped {skipped} existing.")


if __name__ == "__main__":
    asyncio.run(main())

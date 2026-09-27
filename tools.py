"""
The three FitFindr tools.
"""

import re

import config  # noqa: F401
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    listings = load_listings()

    def size_matches(item_size: str) -> bool:
        if not size:
            return True
        requested = size.strip().lower()
        tokens = [t for t in re.split(r"[^a-z0-9]+", item_size.lower()) if t]
        return requested in tokens

    desc_words = set(re.findall(r"[a-z0-9]+", description.lower())) if description else set()

    scored = []
    for item in listings:
        if max_price is not None and item["price"] > max_price:
            continue
        if not size_matches(item["size"]):
            continue

        haystack = " ".join(
            [
                item.get("title", ""),
                item.get("description", ""),
                " ".join(item.get("style_tags", [])),
            ]
        ).lower()
        haystack_words = set(re.findall(r"[a-z0-9]+", haystack))

        score = len(desc_words & haystack_words)
        if score == 0:
            continue

        scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    items = wardrobe.get("items", [])

    item_desc = (
        f"{new_item.get('title')} ({new_item.get('category')}), "
        f"colors: {', '.join(new_item.get('colors', []))}, "
        f"style: {', '.join(new_item.get('style_tags', []))}"
    )

    if not items:
        prompt = (
            f"Someone is considering buying this thrifted item:\n{item_desc}\n\n"
            "They don't have any wardrobe items on file yet. Suggest one or "
            "two general outfit ideas for this piece — what kind of things it "
            "would pair well with — in a sentence or two."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {w['name']} ({w['category']}), colors: {', '.join(w.get('colors', []))}, "
            f"style: {', '.join(w.get('style_tags', []))}"
            for w in items
        )
        prompt = (
            f"Someone is considering buying this thrifted item:\n{item_desc}\n\n"
            f"Their existing wardrobe:\n{wardrobe_lines}\n\n"
            "Suggest one or two specific outfits using pieces they already "
            "own, naming the pieces directly."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    if not outfit or not outfit.strip():
        return (
            f"{new_item.get('title', 'This item')} — "
            f"${new_item.get('price', '?')} on "
            f"{new_item.get('platform', 'an unknown platform')}. "
            "No outfit suggestion available for this one."
        )

    prompt = (
        "Write a short, casual social-media caption (2-4 sentences) for a "
        "thrift find, in the voice of someone who just found it and is "
        "excited about it.\n\n"
        f"Item: {new_item.get('title')}\n"
        f"Price: ${new_item.get('price')}\n"
        f"Platform: {new_item.get('platform')}\n"
        f"Outfit idea: {outfit}\n\n"
        "Mention the item and its price and platform once each. Make it "
        "sound like a real post, not a product listing."
    )

    return generate(prompt)

#!/usr/bin/env python3
"""
Translate i18n/en.json into all target languages using the DeepL API.
Writes i18n/{lang}.json for each target language.

Requires env var: DEEPL_API_KEY
DeepL free tier keys end in :fx  → uses api-free.deepl.com
DeepL pro keys                   → uses api.deepl.com
"""

import json
import os
import sys
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Target languages: { output filename: DeepL language code }
# ---------------------------------------------------------------------------
TARGETS = {
    "fr": "FR",
    "de": "DE",
    "es": "ES",
    "pt": "PT-BR",
    "ru": "RU",
}

# Languages that support the formality parameter in DeepL
FORMALITY_SUPPORTED = {"FR", "DE", "ES", "PT-BR", "RU"}


def get_endpoint(api_key: str) -> str:
    return (
        "https://api-free.deepl.com/v2/translate"
        if api_key.endswith(":fx")
        else "https://api.deepl.com/v2/translate"
    )


def flatten(obj: dict, prefix: str = "") -> dict:
    """Recursively flatten a nested dict into dot-notation keys."""
    items = {}
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.update(flatten(v, key))
        else:
            items[key] = v
    return items


def unflatten(flat: dict) -> dict:
    """Reconstruct a nested dict from dot-notation keys."""
    result = {}
    for key, value in flat.items():
        parts = key.split(".")
        d = result
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = value
    return result


def translate_batch(
    texts: list[str], target_lang: str, api_key: str, endpoint: str
) -> list[str]:
    payload = {
        "text": texts,
        "source_lang": "EN",
        "target_lang": target_lang,
    }
    if target_lang in FORMALITY_SUPPORTED:
        payload["formality"] = "prefer_less"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        return [t["text"] for t in result["translations"]]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  DeepL HTTP {e.code}: {body}", file=sys.stderr)
        raise


def main():
    api_key = os.environ.get("DEEPL_API_KEY", "").strip()
    if not api_key:
        print("Error: DEEPL_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    endpoint = get_endpoint(api_key)
    print(f"Using endpoint: {endpoint}")

    with open("i18n/en.json", "r", encoding="utf-8") as f:
        source = json.load(f)

    flat   = flatten(source)
    keys   = list(flat.keys())
    values = list(flat.values())

    BATCH = 50  # DeepL recommends ≤ 50 strings per request

    for lang_file, deepl_code in TARGETS.items():
        print(f"Translating → {deepl_code} ({lang_file}.json) ...")
        translated_values = []

        for i in range(0, len(values), BATCH):
            batch = values[i : i + BATCH]
            translated_values.extend(
                translate_batch(batch, deepl_code, api_key, endpoint)
            )

        translated_flat = dict(zip(keys, translated_values))
        translated      = unflatten(translated_flat)

        out_path = f"i18n/{lang_file}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(translated, f, ensure_ascii=False, indent=2)
        print(f"  Written {out_path}")

    print("Done.")


if __name__ == "__main__":
    main()

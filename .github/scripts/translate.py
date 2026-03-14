#!/usr/bin/env python3
"""
Translate i18n/en.json into all target languages using the DeepL API.

Diff-based: compares en.json against a snapshot (i18n/.en_snapshot.json)
and only translates new or changed strings. Existing translations for
unchanged strings are kept as-is, saving API quota.

Exit codes:
  0 — success, or nothing needed to translate
  1 — strings need translation but the API call failed (quota, auth, etc.)
      Deployment is blocked until this is resolved.

Requires env var: DEEPL_API_KEY
  Free tier keys end in :fx  → api-free.deepl.com
  Pro keys                   → api.deepl.com
"""

import json
import os
import sys
import urllib.request
import urllib.error

TARGETS = {
    "fr": "FR",
    "de": "DE",
    "es": "ES",
    "pt": "PT-BR",
    "ru": "RU",
}

FORMALITY_SUPPORTED = {"FR", "DE", "ES", "PT-BR", "RU"}
SNAPSHOT_PATH       = "i18n/.en_snapshot.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_endpoint(api_key: str) -> str:
    return (
        "https://api-free.deepl.com/v2/translate"
        if api_key.endswith(":fx")
        else "https://api.deepl.com/v2/translate"
    )


def load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def flatten(obj: dict, prefix: str = "") -> dict:
    out = {}
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out


def unflatten(flat: dict) -> dict:
    result = {}
    for key, value in flat.items():
        parts = key.split(".")
        d = result
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = value
    return result


# ---------------------------------------------------------------------------
# DeepL call — fails loudly with actionable messages
# ---------------------------------------------------------------------------

def translate_batch(
    texts: list[str], target_lang: str, api_key: str, endpoint: str
) -> list[str]:
    payload: dict = {
        "text": texts,
        "source_lang": "EN",
        "target_lang": target_lang,
    }
    if target_lang in FORMALITY_SUPPORTED:
        payload["formality"] = "prefer_less"

    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return [t["text"] for t in json.loads(resp.read())["translations"]]

    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 456:
            print(
                "\n❌  DEEPL QUOTA EXCEEDED\n"
                "    Your free-tier character quota for this month is exhausted.\n"
                "    Translations cannot be updated — deployment is blocked.\n"
                "    ➜  Upgrade your DeepL plan at deepl.com/pro\n"
                "       or wait for the monthly quota reset.\n",
                file=sys.stderr,
            )
        elif e.code == 403:
            print(
                "\n❌  DEEPL AUTHENTICATION FAILED\n"
                "    The DEEPL_API_KEY secret is invalid or has been revoked.\n"
                "    ➜  Go to: GitHub repo → Settings → Secrets → Actions\n"
                "       and update the DEEPL_API_KEY value.\n",
                file=sys.stderr,
            )
        elif e.code == 429:
            print(
                "\n❌  DEEPL RATE LIMIT\n"
                "    Too many requests were sent to the DeepL API in a short time.\n"
                "    ➜  Re-run the workflow in a few minutes.\n",
                file=sys.stderr,
            )
        else:
            print(
                f"\n❌  DEEPL API ERROR  (HTTP {e.code})\n"
                f"    Response body: {body}\n",
                file=sys.stderr,
            )
        raise


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    api_key  = os.environ.get("DEEPL_API_KEY", "").strip()
    endpoint = get_endpoint(api_key) if api_key else None

    en_flat       = flatten(load_json("i18n/en.json"))
    snapshot_flat = flatten(load_json(SNAPSHOT_PATH))

    # Keys that are new or whose English value changed since last translation
    changed = {k: v for k, v in en_flat.items() if snapshot_flat.get(k) != v}

    if not changed:
        print("✓  Nothing to translate — all strings match the snapshot.")
        return

    print(f"→  {len(changed)} string(s) need translation:\n")
    for k in sorted(changed):
        marker = "NEW    " if k not in snapshot_flat else "CHANGED"
        print(f"   [{marker}]  {k}")

    # Block here if no API key — there IS work to do
    if not api_key:
        print(
            f"\n❌  DEEPL_API_KEY NOT SET\n"
            f"    {len(changed)} string(s) need translation but no API key is configured.\n"
            "    ➜  Go to: GitHub repo → Settings → Secrets → Actions\n"
            "       and add DEEPL_API_KEY (get a free key at deepl.com/pro-api).\n",
            file=sys.stderr,
        )
        sys.exit(1)

    keys   = list(changed.keys())
    values = list(changed.values())
    BATCH  = 50

    for lang_file, deepl_code in TARGETS.items():
        print(f"\n→  Translating {len(keys)} string(s) → {deepl_code} ...")

        # Load existing translations, drop keys deleted from en.json
        existing = flatten(load_json(f"i18n/{lang_file}.json"))
        existing = {k: v for k, v in existing.items() if k in en_flat}

        # Translate only the diff
        translated_values: list[str] = []
        for i in range(0, len(values), BATCH):
            translated_values.extend(
                translate_batch(values[i : i + BATCH], deepl_code, api_key, endpoint)
            )

        # Merge new translations into existing
        for k, v in zip(keys, translated_values):
            existing[k] = v

        out_path = f"i18n/{lang_file}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(unflatten(existing), f, ensure_ascii=False, indent=2)
        print(f"   ✓  Written {out_path}")

    # Save snapshot so next run only translates future changes
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(en_flat, f, ensure_ascii=False, indent=2)
    print(f"\n✓  Snapshot updated → {SNAPSHOT_PATH}")
    print("✓  Translation complete.")


if __name__ == "__main__":
    main()

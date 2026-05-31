# Dev Setup

## Prerequisites

- Python 3 (for `make serve` — usually pre-installed on Linux/macOS)
- Git

## Local Preview

```bash
make serve   # serves at http://localhost:8080
```

Open `http://localhost:8080` in a browser. No build step — edits are visible on page refresh.

## Deploy

Push to `master` — GitHub Pages publishes automatically within ~30 seconds.

```bash
git push origin master
```

GitHub Pages config: repo Settings → Pages → Source: Deploy from branch → `master` / `/(root)`.

## Gotchas

> Populate as issues are discovered.

# Development Workflow

Use slash commands to start a workflow:

- `/new-feature` — start a new feature
- `/fix-bug` — start a bug fix
- `/ui-change` — start a UI change

## New Feature

1. **Create a branch** — `git checkout master && git pull && git checkout -b feat/<kebab-case-name>`
2. Receive specs (loose or detailed)
3. Write a plan — listing what will be created, reused, or modified — no code yet
4. Wait for validation (approved / adjusted / rejected)
5. Execute in small, coherent commits so changes can be followed in the editor and cherry-picked if needed

## Bug Fix

1. **Create a branch** — `git checkout master && git pull && git checkout -b fix/<kebab-case-name>`
2. Receive bug description
3. If 95%+ confident in a quick fix: "It's an easy fix, here's how: {plan}" and wait for go-ahead
4. Otherwise: follow the feature workflow (plan → validate → execute)

## UI Changes

Two-step plan before any code:
1. **Visual plan** — what the user will see, how it looks, layout and feel
2. **Technical plan** — which files to edit or create, what changes to make in code

Both plans require validation before execution starts.

## Execution Rules

- Always start from an up-to-date `master` — pull before branching
- Changes must be small and coherent — each chunk should be committable and cherry-pickable independently
- Never write code before a plan is validated
- Keep the user able to follow along and course-correct at any point
- Before asking to commit, update `site-plan.md` if pages were added, removed, or their purpose changed
- Use `prompts/` templates as specs input when starting a skill

## Translations

Translations are static JSON files — there is no automated pipeline. Any time `i18n/en.json` is added to or changed, **update all five language files in the same commit**:

| File | Language |
|------|----------|
| `i18n/fr.json` | French |
| `i18n/de.json` | German |
| `i18n/es.json` | Spanish |
| `i18n/pt.json` | Portuguese (BR) |
| `i18n/ru.json` | Russian |

Rules:
- Keep gaming terms untranslated where they are used as proper nouns: `Tryharder`, `Entertainer`, `Warfare`, `Sineva`, `Girl`, `Streamer Showcase`, `Community Reference`, `Competitive Hub`, `Data Hub`
- Use informal register (`tu`/`du`/`tú`/`ты`) — this is a gaming site
- Never leave a key untranslated or copied from English (except the proper nouns listed above)

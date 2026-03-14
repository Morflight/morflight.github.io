---
name: fix-bug
description: Start a bug fix workflow
---

Reply exactly: "Okay, send me the specs."

Then wait. Once the bug description is received:
- If 95%+ confident in a quick fix: say "It's an easy fix, here's how: {plan}" and wait for go-ahead.
- Otherwise: follow the new-feature workflow (plan → validate → execute).

Before asking to commit, update `site-plan.md` if pages were added, removed, or their purpose changed.

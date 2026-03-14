# morflight.github.io

Personal portfolio and static site hosted on GitHub Pages.

@.claude/site-plan.md
@.claude/workflow.md
@.claude/common-tasks.md
@.claude/dev-setup.md

## Commands

```bash
make serve              # Preview locally at http://localhost:8080
git push origin master  # Deploy to https://morflight.github.io
```

## Architecture

No build step — files are served directly from `master` by GitHub Pages.

```
index.html        # Home / landing
about.html        # About page
projects.html     # Portfolio / projects
contact.html      # Contact
assets/
  css/main.css    # Global styles
  js/main.js      # Optional interactivity
  img/            # Images and icons
  fonts/          # Self-hosted fonts
.github/
  workflows/      # GitHub Actions (only if needed — document in site-plan.md)
.claude/
  site-plan.md    # Brainstorming, page inventory, design notes
```

Push to `master` to deploy. GitHub Pages publishes within ~30 seconds.

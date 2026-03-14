# Troubleshooting

> Populate as issues and solutions are discovered.

## Page not updating after push

**Symptom:** Changes pushed to `master` are not visible at `morflight.github.io`.

**Cause:** GitHub Pages can take up to 60 seconds to rebuild. Occasionally a cache issue delays it further.

**Fix:**
1. Wait ~60 seconds and hard-refresh the browser (`Ctrl+Shift+R` / `Cmd+Shift+R`)
2. Check the Actions tab on GitHub — if a build failed, the error will appear there
3. Verify Pages is set to deploy from `master` / `/(root)` in repo Settings → Pages

## Local preview shows different result than GitHub Pages

**Symptom:** Site looks correct on `localhost:8080` but broken on the live URL.

**Cause:** Absolute paths (e.g. `/assets/css/main.css`) work on `localhost` but may resolve incorrectly on a project page URL (`username.github.io/repo`). For a user site (`username.github.io`), the root is `/` so absolute paths work fine.

**Fix:** Use relative paths (`assets/css/main.css`) unless the site is a user page deployed at the root.

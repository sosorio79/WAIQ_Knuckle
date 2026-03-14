# Pre-Publish Checklist (GitHub)

Run this before your first public push.

## Sensitive Data — Must NOT be committed

- [ ] No `.env` file (only `.env.example` is committed)
- [ ] No `data/` directory or `*.db` files
- [ ] No `venv/` or `node_modules/`
- [ ] No API keys, tokens, or real credentials in code
- [ ] No local paths (e.g. `Z:\`, `C:\Users\you\`) in committed files

## Quick verify (run before commit)

```bash
# Ensure nothing sensitive is staged
git status
git diff --cached --name-only | grep -E "\.env$|/data/|venv/|node_modules" && echo "⚠️ STOP: Sensitive files staged!" || echo "✓ No sensitive files"

# Review what's being committed
git diff --cached --stat
```

Windows PowerShell:
```powershell
git status
$bad = git diff --cached --name-only | Select-String -Pattern "\.env$|/data/|venv/|node_modules"
if ($bad) { Write-Host "⚠️ STOP: Sensitive files staged!" } else { Write-Host "✓ No sensitive files" }
```

## Already configured

- `.gitignore` excludes: `.env`, `data/`, `venv/`, `node_modules/`, `*.db`, `.cursor/`, logs, IDE files
- `.env.example` has placeholder values only
- Information-disclosure lab uses mock path `/app/data/app.db` (not real local path)
- SECURITY.md warns that app is intentionally vulnerable

## Before push — GitHub identity

- Repo will be published under the remote's account (e.g. `git remote -v`). Change remote if you want a different GitHub identity.

## After push

- Add repository description and topics on GitHub
- Consider enabling GitHub Issues for feedback

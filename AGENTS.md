# Repository Guidelines

## Project Structure

This is an asset-first Codex/PetDex package; there is no conventional `src/` application.

- `pets/<slug>/` contains each distributable `pet.json` and `spritesheet.webp`.
- `prompts/` contains generation prompts for the base character and animation rows.
- `qa/` contains timestamped validation, visual-review, and release evidence.
- `install.sh` and `install.ps1` are the cross-platform installers.
- `ASSETS-LICENSE.md`, `NOTICE`, and `LICENSES/` define separate asset and installer-code rights.

## Build, Test, and Development Commands

There is no package-manager build step. Run installer checks before submitting changes:

```bash
bash -n install.sh
shellcheck -S warning install.sh
```

Parse the PowerShell installer with PowerShell 7 when available:

```powershell
$null = [System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path .\install.ps1), [ref]$null, [ref]$null)
```

For sprite changes, use the bundled `hatch-pet` runtime and validator (not a bare system Python); every package must pass `validate_atlas.py --require-v2` and the documented visual QA workflow. Test installers in a temporary `CODEX_HOME` and verify both supported and unknown slugs.

## Coding Style and Naming

Use strict Bash (`set -euo pipefail`) with two-space indentation and quoted paths. Use four-space indentation and `Set-StrictMode` in PowerShell. Format JSON with two-space indentation. Pet slugs and prompt filenames use lowercase kebab-case; QA files use `<topic>-<YYYYMMDD>-vN.json`. Keep scripts deterministic, explicit, and free of silent fallbacks.

## Testing Guidelines

Each sprite must be a transparent `1536x2288` WebP RGBA v2 atlas (`8x11` cells), with matching `spriteVersionNumber: 2` metadata. Record new checks under `qa/`, including commands, results, and any reviewed warnings. Do not treat static QA as a substitute for Codex App playback or multi-display acceptance.

## Commits and Pull Requests

Follow the history's Conventional Commit style, for example `fix: repair sprite proportions`, `qa: record release evidence`, or `docs: update install guidance`. PRs should list affected slugs, validation commands and outcomes, visual evidence paths, and any linked issue. Do not include credentials, private paths, or machine-specific identifiers; never create duplicate PetDex slugs.

## Security and Licensing

Brand names, character art, prompts, and related creative content remain governed by `ASSETS-LICENSE.md`; installer code alone is Apache-2.0. Preserve notices and do not relicense or commercially redistribute brand assets without permission.

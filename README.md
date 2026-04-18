# ha-material-theme <a href="https://josephmienko.github.io/ha-material-theme"><img src="auth-logo-light.svg" align="right" height="75" /></a>

<!-- badges: start -->

Part of the Crooked Sentry universe | [![Validate](https://github.com/josephmienko/ha-material-theme/actions/workflows/validate.yml/badge.svg)](https://github.com/josephmienko/ha-material-theme/actions/workflows/validate.yml)
[![Codecov test coverage](https://codecov.io/gh/josephmienko/ha-material-theme/badge.svg)](https://app.codecov.io/gh/josephmienko/ha-material-theme)
<!-- badges: end -->

## Overview

`ha-material-theme` is a HACS theme repository for a Material 3 inspired Home Assistant theme.

The install surface is a single generated file under `themes/`. Everything else in the repo is maintainer tooling.

## Repo Layout

```text
ha-material-theme/
  .github/
    workflows/
      validate.yml
  scripts/
    build_theme.py
  screenshots/
  src/
    material-theme.json
  tests/
    test_build_theme.py
  themes/
    ha-material-theme.yaml
  .gitignore
  README.md
  hacs.json
```

## Included Themes

- `Crooked Material`
- `Crooked Material Medium Contrast`
- `Crooked Material High Contrast`

## HACS Install

1. Add the repository to HACS as a `Theme`.
2. Install `HA Material Theme`.
3. Restart Home Assistant if HACS prompts for it.
4. Select one of the included theme names in your user profile.

## Manual Install

1. Copy `themes/ha-material-theme.yaml` into your Home Assistant `themes/` directory.
2. Ensure your `configuration.yaml` includes:

   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```

3. Restart Home Assistant.
4. Select one of the included theme names in your user profile.

## Maintainer Workflow

1. Replace `src/material-theme.json` with the latest Material Theme Builder export.
2. Rebuild the install artifact:

   ```bash
   python3 scripts/build_theme.py
   ```

3. Run validation:

   ```bash
   python3 -m pip install pytest pytest-cov
   pytest --cov=scripts --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml:coverage.xml -q
   ```

4. Commit both the source JSON and the generated `themes/ha-material-theme.yaml`.

The CI workflow fails if the generated theme file is out of date and uploads coverage to Codecov from GitHub Actions via OIDC.

## Extraction Mapping

Current source files in this monorepo map to the extracted repo like this:

- `homeassistant/themes/crooked_material/material-theme-crooked.json` -> `src/material-theme.json`
- `scripts/build_ha_theme.py` -> `scripts/build_theme.py`
- `homeassistant/themes/crooked_material/crooked_material.yaml` -> `themes/ha-material-theme.yaml`

## Notes

- `src/material-theme.json` is the source of truth.
- `themes/ha-material-theme.yaml` is the only HACS runtime artifact.
- The generated file is JSON-compatible YAML because that matches the current appliance repo output exactly.
- `screenshots/` is for README assets only and should never be required at runtime.

<h1 style="display: none;"><a href="https://josephmienko.github.io/ha-material-theme/">ha-material-theme</a></h1>
<picture align="center">
  <!-- Desktop Dark Mode -->
  <source media="(min-width: 769px) and (prefers-color-scheme: dark)" srcset="assets/header-wide-dark-inline.svg">
  <!-- Desktop Light Mode -->
  <source media="(min-width: 769px) and (prefers-color-scheme: light)" srcset="assets/header-wide-light-inline.svg">
  <!-- Mobile Dark Mode -->
  <source media="(max-width: 768px) and (prefers-color-scheme: dark)" srcset="assets/header-stacked-dark-inline.svg">
  <!-- Mobile Light Mode -->
  <source media="(max-width: 768px) and (prefers-color-scheme: light)" srcset="assets/header-stacked-light-inline.svg">
  <img src="assets/header-wide-light-inline.svg" alt="ha-material-theme">
</picture>
<b align="left" class="cs-repo-meta">
  <span class="cs-repo-subtitle">Part of the Crooked Sentry universe</span>
  <span class="cs-repo-meta-separator" aria-hidden="true">|</span>
  <span class="cs-repo-badges">
    <a href="https://github.com/josephmienko/ha-material-theme/actions/workflows/validate.yml"><img src="https://github.com/josephmienko/ha-material-theme/actions/workflows/validate.yml/badge.svg" alt="Validate" align="absmiddle" /></a>
    <a href="https://app.codecov.io/gh/josephmienko/ha-material-theme"><img src="https://codecov.io/gh/josephmienko/ha-material-theme/badge.svg" alt="Codecov test coverage" align="absmiddle" /></a>
  </span>
</b>

Material 3 inspired Home Assistant theme with light, medium, and high contrast variants. Install via HACS or manually to your themes directory.

## Configuration

### Installation Instructions

#### HACS Install

1. Add the repository to HACS as a `Theme`.
2. Install `HA Material Theme`.
3. Restart Home Assistant if HACS prompts for it.
4. Select one of the included theme names in your user profile.

#### Manual Install

1. Copy `themes/ha-material-theme.yaml` into your Home Assistant `themes/` directory.
2. Ensure your `configuration.yaml` includes:

   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```

3. Restart Home Assistant.
4. Select one of the included theme names in your user profile.

### Available Themes

- `Crooked Material`
- `Crooked Material Medium Contrast`
- `Crooked Material High Contrast`

### Maintainer Workflow

1. Replace `src/material-theme.json` with the latest Material Theme Builder export.
2. Rebuild the install artifact:

   ```bash
   python3 scripts/build_theme.py
   ```

3. Run validation:

   ```bash
   python3 -m pip install pytest pytest-cov
   pytest --cov=scripts --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml:coverage.xml -q
  # Design Notes

- `src/material-theme.json` is the source of truth (generated from Material Theme Builder)
- `themes/ha-material-theme.yaml` is the only HACS runtime artifact
- Variants maintain consistency with the M3 design system used across Crooked Sentry components
## Notes

- `src/material-theme.json` is the source of truth.
- `themes/ha-material-theme.yaml` is the only HACS runtime artifact.
- The generated file is JSON-compatible YAML because that matches the current appliance repo output exactly.
- `screenshots/` is for README assets only and should never be required at runtime.

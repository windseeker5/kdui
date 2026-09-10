# AGENTS.md — KD UI development rules

KD UI is an installable Jinja component library with a Flask showroom.

## Architecture

- Flask and Jinja server-side rendering only.
- Basecoat supplies visual and interactive primitives.
- Tailwind is used for layout and application-specific adjustments.
- No SPA framework.
- `src/kdui/` is distributable library code.
- `app/` is the showroom, not a sample business application.

## UI layers

1. Vendor macros: `src/kdui/templates/kdui/basecoat/`
2. Components: `src/kdui/templates/kdui/components/`
3. Patterns: `src/kdui/templates/kdui/patterns/`

Use namespaced imports such as:

```jinja
{% from "kdui/components/card.html" import card %}
{% from "kdui/patterns/form_page.html" import form_page %}
```

## Rules

- Inspect Basecoat and existing components before creating UI.
- Components and patterns must contain no domain-specific routes or data.
- Prefer `call` blocks over raw HTML string parameters for rich content.
- Keep JavaScript minimal; use Basecoat behavior when available.
- Add every public macro to the showroom gallery with usage documentation.
- Verify mobile, desktop, light, dark, keyboard, and multiple-instance states.
- Rebuild CSS after changing Tailwind classes: `npm run build:css`.
- Run `pytest` before release.
- Consumer projects pin versions and upgrade deliberately.
- Do not add application generators, CRUD scaffolders, or fake business apps.

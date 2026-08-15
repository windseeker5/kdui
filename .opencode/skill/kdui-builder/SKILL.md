---
name: kdui-builder
description: Use when designing, creating, improving, auditing, or publishing reusable KD UI Jinja components or blocks built with Flask, Tailwind, and Basecoat. Trigger on "KD UI", "KDUI component", "publish component", "promote component", reusable component work, or changes under app/templates/components. Not for one-off page markup or backend-only work.
---

# KD UI Component Builder

Prototype reusable UI in a real application, then promote the generalized
result into the standalone KD UI repository. Consuming applications do not
host a UI gallery; KD UI owns the component and block showrooms.

## Repositories on this machine

- Active prototype app: use the current repository root.
- KD UI repository: locate the local `windseeker5/kdui` checkout and verify
  its Git remote before editing; do not assume a portable absolute path.
- KD UI component gallery: `app/templates/gallery/components.html`
- KD UI block gallery: `app/templates/gallery/blocks.html`
- Promotion helper: `scripts/kdui_promote.py`

`scripts/sync_basecoat.mjs` is unrelated to promotion. It only vendors the
installed `basecoat-css` npm package into whichever repository runs it.

## Non-negotiable rules

1. Use Basecoat primitives before creating a new low-level component.
2. Prototype against real content in the consuming application.
3. Reusable macros need Usage/Params documentation and `class_=""` support.
4. Put reusable browser behavior in
   `app/static/js/components/<component>.js`, not app-specific `app.js`.
5. Rebuild CSS after every Tailwind class change with `npm run build:css`.
6. KD UI's gallery is the only catalog. Do not add `/ui` routes to consuming apps.
7. Never commit or push the KD UI repository without explicit user approval.

## Phase 1: Prototype in the application

1. Decide whether the pattern is a component or a full-page/block composition.
2. Inspect existing Basecoat primitives and 2-3 related KD UI components.
3. Build or improve the component in `app/templates/components/` and use it
   directly in the real application page that needs it.
4. Keep domain-specific data outside the macro and expose customization through
   parameters and `class_`.
5. If JavaScript is required, make it instance-scoped through data attributes
   and place it under `app/static/js/components/`.
   Register each promoted controller in KD UI's base layout and document the
   script requirement with the component.
6. Run `npm run build:css` and verify the real page with Playwright on desktop
   and mobile.

## Phase 2: Audit and promote

From the KD UI repository, audit the source application:

```bash
python scripts/kdui_promote.py status --source /path/to/prototype --kind component
```

Preview and promote one explicit file:

```bash
python scripts/kdui_promote.py component file_upload --source /path/to/prototype --dry-run
python scripts/kdui_promote.py component file_upload --source /path/to/prototype
```

Use `block` instead of `component` for a reusable block. The helper copies an
optional same-named JavaScript controller automatically. It does not copy
gallery markup, commit, or push.

## Phase 3: Catalog and verify in KD UI

1. Add or update the live example in KD UI's gallery, with a usage snippet.
2. Keep examples generic; do not mention the source application's domain.
3. Update README/HOWTO when the public component inventory or contract changes.
4. Run `npm run build:css` inside KD UI.
5. Render and visually verify `/ui/components` or `/ui/blocks` with Playwright.
6. Run syntax checks and review `git diff` in both repositories.
7. Show the user the KD UI diff and ask before commit or push.

## Completion checklist

- [ ] Solves a demonstrated need in a real application
- [ ] Reuses Basecoat instead of rebuilding an existing primitive
- [ ] Generic macro with documented parameters and `class_` override
- [ ] Reusable JavaScript travels as an optional same-named controller
- [ ] Application page tested on desktop and mobile
- [ ] Component/block promoted to the local KD UI repository
- [ ] KD UI gallery demo and usage snippet added
- [ ] CSS rebuilt and KD UI gallery visually verified
- [ ] Both repository diffs reviewed
- [ ] No KD UI commit or push without explicit approval

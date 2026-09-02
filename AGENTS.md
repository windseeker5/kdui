# AGENTS.md — UI Development Rules

This file instructs AI coding agents (OpenCode, Cursor, Copilot, etc.) on how
to work within this Flask/Jinja starter.

---

## Stack

- **Flask** + **Jinja** = server-side rendering, always.
- **Basecoat UI** = shadcn-compatible visual engine (buttons, cards, dialogs,
  sidebar, forms, dark mode, etc.).
- **Tailwind CSS** = layout and application-specific adjustments only.
- **No React, Vue, Svelte, or any SPA framework** unless there is an explicit,
  documented architectural requirement.

---

## UI Development Rules

1. **Use Flask and Jinja as the default rendering architecture.**
   Do not reach for client-side rendering when Flask can handle it.

2. **Prefer server-side behavior over client-side JavaScript.**
   - Search → `/customers?q=acme`
   - Filter → `/customers?status=active`
   - Sort   → `/customers?sort=name&order=asc`
   - Pagination → `/customers?page=3`
   All implemented with Flask routes + Jinja re-render.

3. **Use Basecoat UI for visual primitives.**
   Do not rebuild: `btn`, `card`, `badge`, `input`, `label`, `table`,
   `alert`, `empty`, `dialog`, `dropdown-menu`, `sidebar`, `tabs`,
   `select`, `combobox`, `toast`, `pagination`-style links.

4. **Before creating new UI, inspect existing components and blocks.**
   - Components → `app/templates/components/`
   - Blocks     → `app/templates/blocks/`
   - Basecoat macros → `app/templates/basecoat/`

5. **Reuse an existing block whenever possible.**
   Compose from blocks before writing a new one-off page.

6. **Do not create a new low-level component if Basecoat already provides it.**
   Extend Basecoat's HTML patterns instead.

7. **Use Tailwind utilities primarily for layout and application-specific
   adjustments**, not to rebuild what Basecoat's semantic classes already cover.
   Avoid long chains of Tailwind utility soup.

8. **Keep JavaScript minimal.**
   Basecoat's `all.min.js` handles: dialog, dropdown, sidebar toggle,
   tabs, select, combobox, toast, popover, slider.
   Do not rewrite these.

9. **When a UI pattern will likely be reused, create or improve a Block**
   rather than embedding a one-off implementation into a page.

10. **Maintain the shadcn/Basecoat visual language across all screens.**
    Use the same spacing, border-radius, colors, and typography conventions.

11. **New Blocks must be demonstrated in the UI gallery** (`/ui/blocks`).
    Document: file path, extends, and expected template variables.

12. **Basecoat Jinja macros** are in `app/templates/basecoat/`.
    Import them like:
    ```jinja
    {% from "basecoat/sidebar.html.jinja" import sidebar %}
    {% from "basecoat/tabs.html.jinja"    import tabs %}
    {% from "basecoat/dialog.html.jinja"  import dialog %}
    ```

13. **Promote proven components from real applications explicitly.**
    Run `python scripts/kdui_promote.py status --source <project>` to audit
    drift, then promote one named component or block. The helper never commits
    or pushes. Generalize app-specific content, add a KD UI gallery demo,
    rebuild CSS, and verify the result before publishing.

---

## Project File Map

```
app/
  templates/
    layouts/      base.html | app.html | public.html
    components/   stat_card | page_header | data_table | pagination |
                  search_filter | card | alert | empty_state
    blocks/       dashboard | crm_list | detail_page | form_page |
                  settings_page | login_page | landing_page
    basecoat/     sidebar | tabs | dialog | select | combobox |
                  dropdown-menu | toast | popover | command
    gallery/      index | how_it_works | maintainer | components | blocks
  blueprints/
    public/       routes: / and /login
    dashboard/    routes: /app/dashboard, /app/customers, /app/settings
    gallery/      routes: /ui, /ui/how-it-works, /ui/maintainer,
                         /ui/components, /ui/blocks
  static/
    css/output.css   compiled Tailwind + Basecoat (committed)
    js/vendor/basecoat.all.min.js
```

---

## Starting a New Project

Generate a separate, minimal Flask application from this toolbox:

```bash
python scripts/kdui.py new ../my-new-project
cd ../my-new-project
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python wsgi.py
```

Generated applications use precompiled assets and do not require npm. npm is
only used while maintaining KD UI itself.

To add a new block to the KD UI toolbox:
1. Create `app/templates/blocks/my_block.html` (extends a layout).
2. Add a route in the appropriate blueprint.
3. Document it in `app/templates/gallery/blocks.html`.

---

## MCP (Future — v2)

Do not build MCP tooling in v1.
Once the block catalog is stable, MCP becomes an interface over the content
already in `app/templates/components/` and `app/templates/blocks/`.

# Skill: Scaffold a New Page

Use this skill whenever the user asks to create a new page, section, screen,
or resource in a project based on `flask-shadcn-starter`.

---

## When to use this skill

Trigger phrases:
- "add a projects page"
- "create an invoices section"
- "I need a list of orders"
- "build me a CRUD for tickets"
- "new page for [anything]"

---

## Step 1 — Gather information (ask if missing)

You need exactly three things before running the command:

1. **Resource name** — singular noun, lowercase (e.g. `project`, `invoice`, `order`)
2. **Fields** — comma-separated list with optional types:
   - `text` (default) — plain text
   - `badge` — shown as a badge (Active/Inactive) + filter dropdown
   - `date` — date input
   - `email` — email input
   - `currency` — right-aligned, number input
   - `number` — right-aligned, number input
3. **Sidebar icon** — a Lucide icon name (e.g. `folder-kanban`, `briefcase`, `file-text`, `package`, `tag`, `calendar`)
   - If the user doesn't specify, pick the most sensible one silently.

**Example conversation:**
> User: "add a projects page with name, owner, status, and due date"
>
> You infer:
> - name: `project`
> - fields: `name,owner,status:badge,due:date`
> - icon: `folder-kanban`

---

## Step 2 — Run the scaffold command

```bash
flask --app wsgi scaffold resource <name> \
      --fields "<fields>" \
      --icon <icon>
```

Real example:
```bash
flask --app wsgi scaffold resource project \
      --fields "name,owner,status:badge,due:date" \
      --icon folder-kanban
```

Run this with the Shell tool. The command:
- Creates the blueprint (`blueprints/project/`)
- Creates 3 block templates (`blocks/project_list.html`, `_detail.html`, `_form.html`)
- Wires the blueprint into `app/__init__.py`
- Adds the sidebar nav entry in `layouts/app.html`
- Adds the gallery entry in `gallery/blocks.html`

---

## Step 3 — Restart Flask and verify

If Flask is running, restart it so the new blueprint is picked up:
```bash
# Kill the current process and restart
flask --app wsgi run --debug
```

Then verify:
- `http://localhost:5000/app/<name>` — list page renders with 3 sample rows
- Sidebar has the new nav item
- `http://localhost:5000/ui/blocks` — new block appears in gallery

---

## Step 4 — Customize if needed

The scaffold generates working but generic output. Common customizations:

### Change badge colors
In `blocks/<name>_list.html`, find the badge `<td>` cell and change the
`data-variant` logic:
```html
{# Before: Active=outline, Inactive=secondary #}
<span class="badge" data-variant="{{ 'secondary' if row.status == 'Inactive' else 'outline' }}">

{# Example: add a third state #}
<span class="badge" data-variant="{{ 'destructive' if row.status == 'Overdue' else 'outline' }}">
```

### Add more columns to the table
In `blocks/<name>_list.html`, add to the `columns` list and add a `<td>` in the `call(row)` block.

### Add more filter dropdowns
In `blocks/<name>_list.html`, add to the `search_filter` call:
```jinja
{{ search_filter(
  action=url_for("project.list_project"),
  q=q,
  filters=[
    {"name": "status", "options": [("", "All"), ("active", "Active")], "value": status},
    {"name": "owner",  "options": [("", "All owners"), ("alice", "Alice")], "value": owner}
  ]
) }}
```
Then add the corresponding query param in `blueprints/<name>/routes.py`.

### Replace fake data with real data
Open `blueprints/<name>/routes.py` and replace the `_filter()` + list logic
with a real database query. The template variables stay the same.

---

## Field type reference

| Type | Table column | Form input | Notes |
|------|-------------|-----------|-------|
| `text` | plain text | `<input type="text">` | default |
| `badge` | `<span class="badge">` | `<select>` Active/Inactive | adds filter dropdown |
| `date` | plain text | `<input type="date">` | |
| `email` | muted text | `<input type="email">` | |
| `currency` | right-aligned | `<input type="number">` | |
| `number` | right-aligned | `<input type="number">` | |

---

## Available Lucide icons for --icon

`folder-kanban`, `briefcase`, `file-text`, `list`, `package`, `users`,
`shopping-cart`, `tag`, `calendar`, `bar-chart`, `settings`

For any other icon, the scaffold uses a generic square. You can always edit
the SVG manually in `layouts/app.html` after scaffolding.

---

## Rules (from AGENTS.md)

- Never scaffold inside an existing blueprint folder (the command will refuse).
- Always document in the gallery — the scaffold does this automatically.
- Replace fake data before shipping to production.
- If a block already covers the use case, reuse it instead of scaffolding.

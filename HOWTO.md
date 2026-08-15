# How to Use Flask Shadcn Starter

---

## Fastest Path — One Command to a Working Page

```bash
# 1. Clone and run
git clone <repo-url> my-project && cd my-project
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
flask --app wsgi run --debug

# 2. Generate a new page (in a second terminal)
flask --app wsgi scaffold resource projects \
      --fields "name,owner,status:badge,due:date" \
      --icon folder-kanban
```

That's it. Refresh your browser. You have a **Projects** page with:
- Sidebar nav entry (auto-added)
- Search bar + status filter dropdown
- Sortable columns
- Server-side pagination
- View / Edit buttons per row
- Linked detail page and create/edit form
- Gallery entry at `/ui/blocks`

**Field types you can use:** `text` (default), `badge`, `date`, `email`, `currency`, `number`

**Using an AI agent?** Just say:
> *"Add a projects page with name, owner, status (badge), and due date"*
>
> The agent will run the scaffold command for you automatically.

---

Everything below is **reference material** for when you need to customize
beyond the scaffold or understand how the framework is structured.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [How the Framework Works](#2-how-the-framework-works)
3. [Build Your First Page Manually](#3-build-your-first-page-manually)
4. [Add a New Block](#4-add-a-new-block)
5. [Jinja Component Reference](#5-jinja-component-reference)
6. [Basecoat HTML Cheat-Sheet](#6-basecoat-html-cheat-sheet)
7. [Block Reference](#7-block-reference)
8. [Layouts Reference](#8-layouts-reference)
9. [CSS and JS](#9-css-and-js)
10. [Rules for AI Agents](#10-rules-for-ai-agents)

---

## 1. Quick Start

```bash
# Clone
git clone <repo-url> my-project
cd my-project

# Python environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# Install Flask
pip install -r requirements.txt

# Run
flask --app wsgi run --debug
```

Open http://localhost:5000

| Route | What you see |
|---|---|
| `/` | Landing page |
| `/login` | Login page |
| `/app/dashboard` | Dashboard with KPI cards |
| `/app/customers` | CRM list with search / filter / pagination |
| `/app/customers/1` | Customer detail page |
| `/app/customers/new` | Create customer form |
| `/app/settings` | Tabbed settings page |
| `/ui/` | UI Gallery — live component + block catalog |

That's it. No Node.js needed to run the app. CSS and JS are pre-compiled and
committed.

> **Only run `npm` when you change Tailwind classes or upgrade Basecoat.**
> See [Section 9](#9-css-and-js).

---

## 2. How the Framework Works

There are exactly three layers. Keep them clear in your head.

```
┌─────────────────────────────────────────┐
│  LAYER 3 — Pages                        │
│  Your app-specific Flask routes +       │
│  real data. Lives in blueprints/.       │
├─────────────────────────────────────────┤
│  LAYER 2 — Blocks                       │
│  Reusable composed screens.             │
│  Lives in templates/blocks/             │
│  e.g. dashboard, crm_list, form_page    │
├─────────────────────────────────────────┤
│  LAYER 1 — Components                   │
│  Primitive Jinja macros + Basecoat HTML │
│  Lives in templates/components/         │
│  e.g. stat_card, data_table, pagination │
└─────────────────────────────────────────┘
```

### The golden rule

> **Never write one-off UI directly in a route template.**
> Find an existing Block. Extend it. Pass your data to it.
> If no Block fits, create a new Block and add it to the gallery.

---

## 3. Build Your First Page Manually

Scenario: you want a **Projects** page — sidebar app, page header, a table of
projects, and server-side search.

### Step 1 — Add your blueprint

```python
# app/blueprints/projects/__init__.py
from flask import Blueprint
projects_bp = Blueprint("projects", __name__, url_prefix="/app")
from app.blueprints.projects import routes  # noqa
```

```python
# app/blueprints/projects/routes.py
from flask import render_template, request
from app.blueprints.projects import projects_bp

PROJECTS = [
    {"id": 1, "name": "Website Redesign", "status": "Active",  "owner": "Alice", "due": "2026-09-01"},
    {"id": 2, "name": "API Migration",     "status": "Paused",  "owner": "Bob",   "due": "2026-10-15"},
    {"id": 3, "name": "Mobile App",        "status": "Active",  "owner": "Alice", "due": "2026-12-01"},
]

@projects_bp.route("/projects")
def projects():
    q = request.args.get("q", "")
    rows = [p for p in PROJECTS if q.lower() in p["name"].lower()] if q else PROJECTS
    return render_template("blocks/projects_list.html", projects=rows, q=q)
```

Register it in `app/__init__.py`:

```python
from app.blueprints.projects import projects_bp
app.register_blueprint(projects_bp)
```

### Step 2 — Create the Block template

Copy the closest existing block (`crm_list.html`) and adapt it, or write from
scratch by extending `layouts/app.html`:

```html
{# app/templates/blocks/projects_list.html #}
{% extends "layouts/app.html" %}
{% from "components/page_header.html"   import page_header %}
{% from "components/search_filter.html" import search_filter %}

{% block title %}Projects – My App{% endblock %}
{% block breadcrumb %}Projects{% endblock %}

{% block content %}

{{ page_header(title="Projects", description="Track all active projects.") }}

{{ search_filter(action=url_for("projects.projects"), q=q) }}

<div class="table-container">
  <table class="table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Owner</th>
        <th>Status</th>
        <th>Due</th>
      </tr>
    </thead>
    <tbody>
      {% for p in projects %}
      <tr>
        <td class="font-medium">{{ p.name }}</td>
        <td>{{ p.owner }}</td>
        <td>
          <span class="badge" data-variant="{{ 'secondary' if p.status == 'Paused' else 'outline' }}">
            {{ p.status }}
          </span>
        </td>
        <td class="text-muted-foreground">{{ p.due }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

{% endblock %}
```

### Step 3 — Add it to the sidebar

Open `app/templates/layouts/app.html` and add a nav item to the `nav_items`
list:

```jinja
{ "type": "item", "label": "Projects", "url": url_for("projects.projects"),
  "icon": '<svg ...>', "current": ("projects" in request.endpoint) }
```

Use any Lucide SVG from https://lucide.dev — copy the `<svg>` tag directly.

### Step 4 — Visit your page

```
http://localhost:5000/app/projects
```

Done. You have a sidebar app with a search bar, table, and badges — all
server-side rendered, no JavaScript written.

---

## 4. Add a New Block

A Block is a Jinja template in `templates/blocks/` that extends a layout and
uses components. Follow these steps every time.

### 4.1 Create the template

```
app/templates/blocks/my_block.html
```

Minimum structure:

```html
{% extends "layouts/app.html" %}
{% from "components/page_header.html" import page_header %}

{% block title %}My Block – App{% endblock %}
{% block breadcrumb %}My Block{% endblock %}

{% block content %}
{{ page_header(title="My Block", description="What this block does.") }}
{# your content here #}
{% endblock %}
```

### 4.2 Add a route

```python
@my_bp.route("/my-thing")
def my_thing():
    return render_template("blocks/my_block.html", data=my_data)
```

### 4.3 Document it in the gallery

Open `app/templates/gallery/blocks.html` and add an entry to `blocks_list`:

```python
{
  "name": "My Block",
  "description": "One sentence describing what it is.",
  "url": url_for("my_bp.my_thing"),
  "file": "blocks/my_block.html",
  "extends": "layouts/app.html",
  "vars": "data (list of dicts)"
}
```

That's the full workflow. Every new block gets a gallery entry. This keeps the
catalog useful for you and for AI agents.

---

## 5. Jinja Component Reference

Import components at the top of any template, then call them.

### `stat_card` — KPI metric card

```jinja
{% from "components/stat_card.html" import stat_card %}

{{ stat_card(
  label="Revenue",
  value="$48,290",
  delta="+12.5% from last month",
  trend="up"           {# "up" | "down" | "neutral" #}
) }}
```

Use inside a grid for a stat grid:

```html
<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
  {{ stat_card(label="Revenue",   value="$48,290", delta="+12%", trend="up") }}
  {{ stat_card(label="Customers", value="128",     delta="+4",   trend="up") }}
  {{ stat_card(label="Churn",     value="2.1%",    delta="-0.3%",trend="up") }}
  {{ stat_card(label="Avg. Deal", value="$3,800",  delta="+$200",trend="up") }}
</div>
```

---

### `page_header` — Title + description + action button

```jinja
{% from "components/page_header.html" import page_header %}

{{ page_header(
  title="Customers",
  description="Manage your accounts.",
  action='<a href="/app/customers/new" class="btn">Add customer</a>'
) }}
```

The `action` parameter accepts raw HTML — use a Basecoat `btn` link or button.

---

### `card` — Content card with header and footer

```jinja
{% from "components/card.html" import card %}

{% call card(title="Revenue", description="Last 30 days") %}
  <p class="text-2xl font-bold">$48,290</p>
{% endcall %}

{# With footer #}
{% call card(title="Actions", footer='<button class="btn w-full">Save</button>') %}
  <p>Card content here.</p>
{% endcall %}
```

---

### `data_table` — Sortable table with caller rows

```jinja
{% from "components/data_table.html" import data_table %}

{% set columns = [
  {"key": "name",   "label": "Name",   "sortable": true},
  {"key": "status", "label": "Status", "sortable": true},
  {"key": "amount", "label": "Amount", "sortable": false, "align": "end"}
] %}

{% call(row) data_table(
  columns=columns,
  rows=customers,
  sort=sort,
  order=order,
  base_url=url_for("dashboard.customers")
) %}
  <td class="font-medium">{{ row.name }}</td>
  <td>
    <span class="badge" data-variant="outline">{{ row.status }}</span>
  </td>
  <td class="text-end">{{ row.amount }}</td>
{% endcall %}
```

The `caller(row)` pattern means you control the `<td>` cells — the macro
handles the `<table>`, `<thead>`, sort links, and empty state automatically.
Use `align="end"` on a column to align its heading, then add `text-end` to the
matching `<td>` in the caller. Pass
`scrollable=false` when rows contain popover-based controls such as
`action_menu`, and use `class_` for wrapper-level layout overrides.

---

### `pagination` — Server-side page links

```jinja
{% from "components/pagination.html" import pagination %}

{{ pagination(
  page=page,
  total_pages=total_pages,
  base_url=url_for("dashboard.customers"),
  extra_params={"q": q, "status": status, "sort": sort, "order": order}
) }}
```

Pass all current query params in `extra_params` so they survive page changes.

---

### `search_filter` — Search input + dropdown filters

```jinja
{% from "components/search_filter.html" import search_filter %}

{{ search_filter(
  action=url_for("dashboard.customers"),
  q=q,
  filters=[
    {
      "name": "status",
      "options": [("", "All"), ("active", "Active"), ("inactive", "Inactive")],
      "value": status
    }
  ],
  show_submit=true
) }}
```

Add as many `filters` dicts as you need. Each becomes a `<select>` that
auto-submits on change. Set `show_submit=false` when your application uses
Enter-to-search and does not need a visible button. Use `submit_label` to
change the button text and `class_` for form-level layout overrides.

---

### `alert` — Info and error messages

```jinja
{% from "components/alert.html" import alert %}

{{ alert(message="Saved successfully.") }}
{{ alert(title="Error", message="Something failed.", variant="destructive") }}
```

---

### `empty_state` — Empty list placeholder

```jinja
{% from "components/empty_state.html" import empty_state %}

{{ empty_state(
  title="No projects yet",
  description="Create your first project to get started.",
  action='<a href="/app/projects/new" class="btn">New project</a>'
) }}
```

---

### `timeline` — Chronological activity list

```jinja
{% from "components/timeline.html" import timeline %}

{{ timeline(items=[
  {"date": "Aug 14, 2026", "title": "Release deployed", "description": "Version 2.4 is live.", "badge": "Release"},
  {"date": "Aug 12, 2026", "title": "Review approved", "badge": "Review", "badge_variant": "secondary"}
]) }}
```

Each item accepts `date`, `title`, optional `description`, optional `badge`,
and optional `badge_variant`. Use `class_` to extend the root layout.

---

### `file_upload` — File picker, dropzone, and image preview

```jinja
{% from "components/file_upload.html" import file_upload %}

<form method="post" enctype="multipart/form-data">
  <div id="photo-preview-container" class="hidden">
    <img id="photo-preview" alt="Selected photo preview" />
  </div>
  {{ file_upload(
    input_id="photo",
    name="photo",
    prompt="Add a photo",
    hint="JPEG or PNG. 5 MB maximum.",
    accept="image/jpeg,image/png",
    preview_id="photo-preview",
    preview_container_id="photo-preview-container"
  ) }}
  <button type="submit" class="btn">Upload</button>
</form>
```

Click/tap selection works without JavaScript. Include
`static/js/components/file_upload.js` for drag/drop, selection text, previews,
loading states, and opt-in auto-submit. Browser `accept` filters are advisory;
always validate uploaded files on the server.

---

### Basecoat macros (complex interactive components)

These ship from Basecoat directly and live in `templates/basecoat/`.

```jinja
{# Sidebar (used in layouts/app.html — you normally don't call this directly) #}
{% from "basecoat/sidebar.html.jinja" import sidebar %}

{# Tabbed interface #}
{% from "basecoat/tabs.html.jinja" import tabs %}
{{ tabs(tabsets=[
  {"tab": "General",  "panel": "<p>General content</p>"},
  {"tab": "Advanced", "panel": "<p>Advanced content</p>"}
]) }}

{# Dialog / modal #}
{% from "basecoat/dialog.html.jinja" import dialog %}
{{ dialog(trigger="Open dialog", title="Confirm", description="Are you sure?",
          footer='<button class="btn" data-variant="destructive">Delete</button>') }}

{# Select (custom styled dropdown) #}
{% from "basecoat/select.html.jinja" import select %}
{{ select(name="country", items=[
  {"value": "ca", "label": "Canada"},
  {"value": "us", "label": "United States"}
]) }}

{# Toast notification #}
{% from "basecoat/toast.html.jinja" import toaster, toast %}
{{ toaster() }}  {# place once in your layout #}
```

---

## 6. Basecoat HTML Cheat-Sheet

Use these directly in any Jinja template. No import needed — just HTML classes.

### Buttons

```html
<button class="btn">Primary</button>
<button class="btn" data-variant="secondary">Secondary</button>
<button class="btn" data-variant="outline">Outline</button>
<button class="btn" data-variant="ghost">Ghost</button>
<button class="btn" data-variant="destructive">Delete</button>
<button class="btn" data-size="sm">Small</button>
<button class="btn" data-size="lg">Large</button>
<button class="btn" data-size="icon" aria-label="Settings">
  <svg .../>
</button>

{# Button as a link #}
<a href="/somewhere" class="btn" data-variant="outline">Go somewhere</a>

{# Button with icon #}
<button class="btn">
  <svg data-icon="inline-start" .../>
  Add item
</button>
```

### Badges

```html
<span class="badge">Default</span>
<span class="badge" data-variant="secondary">Secondary</span>
<span class="badge" data-variant="destructive">Error</span>
<span class="badge" data-variant="outline">Outline</span>

{# Colored status badges (Tailwind) #}
<span class="badge bg-green-50 text-green-700 dark:bg-green-950 dark:text-green-300">Active</span>
<span class="badge bg-red-50 text-red-700 dark:bg-red-950 dark:text-red-300">Failed</span>
```

### Cards

```html
<div class="card">
  <header>
    <h2>Card Title</h2>
    <p>Card description</p>
    <div class="card-action">
      <button class="btn" data-variant="outline" data-size="sm">Action</button>
    </div>
  </header>
  <section>
    Card body content
  </section>
  <footer>
    <button class="btn">Save</button>
  </footer>
</div>

{# Compact card #}
<div class="card" data-size="sm">...</div>
```

### Inputs and forms

```html
<div class="grid gap-2">
  <label class="label" for="name">Name</label>
  <input class="input" type="text" id="name" placeholder="Acme Corp" />
</div>

<div class="grid gap-2">
  <label class="label" for="notes">Notes</label>
  <textarea class="input min-h-24" id="notes"></textarea>
</div>

<select class="input" name="plan">
  <option value="starter">Starter</option>
  <option value="pro">Pro</option>
</select>
```

### Tables

```html
<div class="table-container">
  <table class="table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Status</th>
        <th class="text-end">Amount</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="font-medium">Acme Corp</td>
        <td><span class="badge" data-variant="outline">Active</span></td>
        <td class="text-end">$12,400</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Alerts

```html
<div class="alert" role="alert">
  <svg class="lucide lucide-info" .../>
  <p class="alert-description">Your changes have been saved.</p>
</div>

<div class="alert" data-variant="destructive" role="alert">
  <svg class="lucide lucide-circle-alert" .../>
  <p class="alert-title">Error</p>
  <p class="alert-description">Something went wrong.</p>
</div>
```

### Empty state

```html
<div class="empty">
  <div class="empty-icon">
    <svg class="lucide lucide-inbox" .../>
  </div>
  <p class="empty-title">No results found</p>
  <p class="empty-description">Try adjusting your search.</p>
</div>
```

### Dark mode toggle

```html
<button
  type="button"
  onclick="window.basecoat.theme.toggle()"
  class="btn" data-variant="ghost" data-size="icon"
  aria-label="Toggle dark mode"
>
  <span class="hidden dark:block"><!-- sun SVG --></span>
  <span class="block dark:hidden"><!-- moon SVG --></span>
</button>
```

---

## 7. Block Reference

All blocks live in `app/templates/blocks/`. Each is a standalone Jinja template
that extends a layout. See live previews at `/ui/blocks`.

| Block | File | Layout | Key Variables |
|---|---|---|---|
| Dashboard | `blocks/dashboard.html` | `layouts/app.html` | `stats`, `recent_customers`, `recent_activity` |
| CRM List | `blocks/crm_list.html` | `layouts/app.html` | `customers`, `q`, `status`, `sort`, `order`, `page`, `total_pages`, `total` |
| Detail Page | `blocks/detail_page.html` | `layouts/app.html` | `customer` dict |
| Form Page | `blocks/form_page.html` | `layouts/app.html` | `customer` (`None` = create, dict = edit) |
| Settings | `blocks/settings_page.html` | `layouts/app.html` | none |
| Login | `blocks/login_page.html` | `layouts/public.html` | none |
| Landing Page | `blocks/landing_page.html` | `layouts/public.html` | none |

### How to adapt a block for your domain

The CRM blocks use `customer` as the model. Swap it for whatever your app
needs — `project`, `invoice`, `order`, `ticket`, etc. The structure stays
identical, only the column names and data change.

Example — adapting `crm_list.html` for invoices:

```python
# Route
@invoices_bp.route("/invoices")
def invoices():
    return render_template("blocks/invoices_list.html", invoices=INVOICES, ...)
```

```html
{# blocks/invoices_list.html — copy of crm_list.html, columns changed #}
{% extends "layouts/app.html" %}
...
{% set columns = [
  {"key": "number",  "label": "Invoice #", "sortable": true},
  {"key": "client",  "label": "Client",    "sortable": true},
  {"key": "amount",  "label": "Amount",    "sortable": true},
  {"key": "due",     "label": "Due Date",  "sortable": true},
  {"key": "status",  "label": "Status",    "sortable": true}
] %}
```

---

## 8. Layouts Reference

Three layouts. Every page extends one of them.

### `layouts/app.html` — The sidebar app shell

Use this for all authenticated / internal pages.

```html
{% extends "layouts/app.html" %}

{% block title %}My Page – App{% endblock %}
{% block breadcrumb %}My Page{% endblock %}  {# shown in the top header bar #}

{% block content %}
  {# your page content here #}
{% endblock %}
```

The sidebar is defined once in `layouts/app.html`. To add a nav item, edit
the `nav_items` list there — it accepts groups, items, submenus, and separators
(see Basecoat sidebar macro docs).

### `layouts/public.html` — No sidebar

Use this for landing pages, login, register, error pages.

```html
{% extends "layouts/public.html" %}

{% block public_body %}
  {# full-width content, no sidebar #}
{% endblock %}
```

### `layouts/base.html` — Bare HTML shell

Contains `<html>`, `<head>`, CSS/JS links, theme flash prevention. Normally
you do not extend this directly — extend `app.html` or `public.html`.

---

## 9. CSS and JS

### Pre-compiled assets (committed to git)

These files are committed so teammates can run the app with zero Node.js:

```
app/static/css/output.css          compiled Tailwind + Basecoat
app/static/css/basecoat-vega.css   Basecoat Vega CDN bundle (source for build)
app/static/js/vendor/basecoat.all.min.js  Basecoat JS runtime
```

### When to rebuild CSS

Rebuild when you:
- Add new Tailwind utility classes that don't exist in `output.css` yet
- Upgrade `basecoat-css` to a new version
- Change the Basecoat style pack (e.g. vega → nova)

```bash
npm install          # first time only
npm run build:css    # one-time rebuild
npm run watch:css    # watch mode while developing
```

### Upgrading Basecoat

```bash
npm install basecoat-css@latest
npm run build        # runs sync:basecoat + build:css
```

`sync:basecoat` automatically re-copies the Jinja macros and JS bundle from
`node_modules` into `app/templates/basecoat/` and `app/static/js/vendor/`.

### Changing the style pack

The starter uses the **Vega** pack (closest to shadcn default). To switch:

1. In `scripts/sync_basecoat.mjs`, change `basecoat-vega.cdn.css` to
   `basecoat-nova.cdn.css` (or maia, lyra, mira, luma, sera, rhea).
2. In `app/static/css/input.css`, update `./basecoat-vega.css` to match.
3. Run `npm run build`.

---

## 10. Rules for AI Agents

When using OpenCode, Cursor, or GitHub Copilot on a project built with this
starter, paste or reference these rules:

```
1. Use Flask + Jinja for all rendering. No SPA frameworks.
2. Server-side for search, filter, sort, pagination.
3. Use Basecoat semantic classes (btn, card, badge, input, table, alert, empty).
4. Check templates/blocks/ before writing new UI. Reuse first.
5. Check templates/components/ for Jinja macros before writing raw HTML.
6. New reusable patterns go in templates/blocks/, not in route templates.
7. Document every new block in templates/gallery/blocks.html.
8. Tailwind utilities are for layout only — not for rebuilding Basecoat components.
9. Basecoat JS (all.min.js) handles: sidebar, dialog, dropdown, tabs, select,
   combobox, toast, popover, slider. Do not rewrite these.
10. See AGENTS.md for the full rule set.
```

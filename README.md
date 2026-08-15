# kdui — Flask Shadcn Starter

> Beautiful Flask/Jinja apps with shadcn-style UI. No React. No TypeScript. One scaffold command.

Built on [Basecoat UI](https://basecoatui.com) + Tailwind CSS. Designed to be cloned and reused
across projects. Works with AI agents (OpenCode, Cursor, Copilot) out of the box.

---

## Fastest Path — One Command to a Working Page

```bash
# 1. Clone and run (30 seconds)
git clone https://github.com/telus/kdui my-project
cd my-project
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
flask --app wsgi run --debug
```

Open **http://localhost:5000** — you'll see the live app with landing page, dashboard,
CRM list, settings, and the UI gallery.

```bash
# 2. Scaffold a new resource page (in a second terminal, 5 seconds)
flask --app wsgi scaffold resource invoices \
      --fields "number,client,amount:currency,status:badge,due:date" \
      --icon file-text
```

That's it. You now have:
- An **Invoices** page at `/app/invoices` with search, filter, sort, pagination
- A detail page at `/app/invoices/1`
- A create/edit form at `/app/invoices/new`
- A sidebar nav entry — added automatically
- A gallery entry at `/ui/blocks` — added automatically

**Using an AI agent?** Just say:
> *"Add an invoices page with number, client, amount (currency), status (badge), and due date"*

The bundled skill at `.opencode/skill/scaffold-page/SKILL.md` teaches any OpenCode agent
to run the scaffold command automatically.

---

## What's Inside

### Stack

| Layer | Technology |
|---|---|
| Server | Flask 3+ |
| Templates | Jinja2 |
| UI | [Basecoat UI](https://basecoatui.com) — shadcn-compatible |
| Styling | Tailwind CSS v4 |
| JS | Basecoat's minimal vanilla JS bundle |

No React. No TypeScript. No SPA framework. Server-side rendered, always.

### Blocks included (copy-paste ready)

| Block | Route | What it is |
|---|---|---|
| Dashboard | `/app/dashboard` | KPI stat cards, data table, activity feed |
| CRM List | `/app/customers` | Search, filter, sort, paginate any dataset |
| Detail Page | `/app/customers/1` | Single record view with quick actions |
| Form Page | `/app/customers/new` | Create / edit form |
| Settings | `/app/settings` | Tabbed settings page |
| Login | `/login` | Centered login card |
| Landing Page | `/` | Full public marketing page |

### Components included

`stat_card` · `page_header` · `card` · `data_table` · `pagination` · `search_filter` ·
`alert` · `empty_state` · Basecoat sidebar · Basecoat tabs · Basecoat dialog ·
Basecoat select · Basecoat toast · dark mode toggle

See them all live at **`/ui/components`** and **`/ui/blocks`**.

---

## Project Structure

```
kdui/
├── app/
│   ├── __init__.py              create_app() factory
│   ├── cli.py                   flask scaffold resource command
│   ├── blueprints/
│   │   ├── public/              /  and /login
│   │   ├── dashboard/           /app/* with fake data
│   │   └── gallery/             /ui/* catalog
│   ├── templates/
│   │   ├── basecoat/            Vendored Basecoat Jinja macros
│   │   ├── components/          Reusable Jinja macros
│   │   ├── blocks/              Full page blocks (copy and adapt)
│   │   ├── layouts/             base.html / app.html / public.html
│   │   └── gallery/             Live UI catalog
│   └── static/
│       ├── css/output.css       Compiled CSS (committed — no Node needed to run)
│       └── js/vendor/           Basecoat JS runtime
├── scripts/sync_basecoat.mjs    Re-sync Basecoat assets after npm upgrade
├── .opencode/skill/             Bundled AI agent skill for scaffolding
├── AGENTS.md                    Rules for AI coding agents
├── HOWTO.md                     Full usage reference
├── package.json                 Tailwind + Basecoat build
├── requirements.txt             Flask only
└── wsgi.py
```

---

## Scaffold Command Reference

```bash
flask --app wsgi scaffold resource <name> \
      --fields "<field1>,<field2:type>,..." \
      --icon <lucide-icon-name>
```

**Field types:** `text` (default) · `badge` · `date` · `email` · `currency` · `number`

**Available icons:** `folder-kanban` · `briefcase` · `file-text` · `list` · `package` ·
`users` · `shopping-cart` · `tag` · `calendar` · `bar-chart`

Examples:

```bash
# Projects page
flask --app wsgi scaffold resource project \
      --fields "name,owner,status:badge,due:date" \
      --icon folder-kanban

# Invoices page
flask --app wsgi scaffold resource invoice \
      --fields "number,client,amount:currency,status:badge,due:date" \
      --icon file-text

# Orders page
flask --app wsgi scaffold resource order \
      --fields "ref,customer:text,total:currency,status:badge" \
      --icon shopping-cart
```

The scaffold never overwrites existing files. It refuses and prints an error if the
resource name already exists — safe to run repeatedly with different names.

---

## Using This as a Starter for a New Project

```bash
git clone https://github.com/telus/kdui my-new-project
cd my-new-project

# Start fresh git history
Remove-Item -Recurse -Force .git   # Windows
# rm -rf .git                      # macOS / Linux

git init
git add .
git commit -m "init from kdui flask starter"
```

Then:
1. Replace fake data in `blueprints/*/fake_data.py` with real DB queries
2. Add your real blueprint logic in `blueprints/*/routes.py`
3. Scaffold new resource pages with `flask scaffold resource`
4. Customize blocks in `templates/blocks/` as needed

---

## Rebuilding CSS (optional)

`output.css` is committed so teammates can run the app with **zero Node.js**.
Only rebuild when you add new Tailwind utility classes or upgrade Basecoat.

```bash
npm install          # first time only
npm run build:css    # one-off rebuild
npm run watch:css    # watch mode while developing
```

To upgrade Basecoat:
```bash
npm install basecoat-css@latest
npm run build        # syncs macros + JS + rebuilds CSS
```

---

## Dark Mode

Built in. Click the moon icon in the sidebar footer. Persists across page loads.
Powered by Basecoat's `window.basecoat.theme.toggle()` — no custom JavaScript required.

---

## For AI Agents

- Read **`AGENTS.md`** for coding rules (what to use, what not to rebuild)
- Read **`HOWTO.md`** for the full component and block reference
- Use the bundled skill at **`.opencode/skill/scaffold-page/SKILL.md`**

---

## License

MIT — use it, adapt it, ship it.

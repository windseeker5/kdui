# KD UI

A reusable Flask/Jinja UI starter and component library built with:

- Flask
- Jinja
- Basecoat UI
- Tailwind CSS
- Minimal vanilla JavaScript

KD UI helps create server-rendered web applications and prototypes quickly
without React, Vue, or another SPA framework.

## What KD UI Is

KD UI serves two related purposes:

1. A starter repository for new Flask/Jinja applications.
2. A catalog of reusable components and page blocks developed in real applications.

KD UI is built on Basecoat UI. Basecoat provides low-level visual and
interactive primitives. KD UI adds reusable Jinja macros, application patterns,
page blocks, examples, and development conventions.

## Architecture

There are three separate layers:

| Layer | Purpose |
|---|---|
| Basecoat UI | Third-party buttons, cards, dialogs, selects, sidebars, tabs, and other primitives |
| KD UI | Reusable Jinja components, blocks, JavaScript controllers, and the UI gallery |
| Your application | Business logic, routes, database models, and application-specific pages |

A consuming application should not expose the KD UI gallery to its users. The
gallery belongs in this repository and acts as the component showroom and
regression environment.

## Important: KD UI Is Currently Copy-Based

KD UI is not currently distributed as a Python or npm package.

Components are copied between KD UI and consuming projects as regular files:

```text
KD UI
app/templates/components/file_upload.html
app/static/js/components/file_upload.js

Your project
app/templates/components/file_upload.html
app/static/js/components/file_upload.js
```

This keeps applications independent and easy to run, but component improvements
must be deliberately promoted back to this repository.

## Start a New Project

Clone KD UI as the starting point:

```bash
git clone https://github.com/windseeker5/kdui.git my-project
cd my-project
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install the Python and frontend dependencies:

```bash
pip install -r requirements.txt
npm install
```

Run the application:

```bash
flask --app wsgi run --debug
```

Open `http://127.0.0.1:5000`. The KD UI gallery is available at:

```text
http://127.0.0.1:5000/ui/
http://127.0.0.1:5000/ui/components
http://127.0.0.1:5000/ui/blocks
```

## Start Independent Git History

When using KD UI to create a separate application, remove the starter
repository's Git history and create a new repository.

Linux or macOS:

```bash
rm -rf .git
git init
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .git
git init
```

Create the application's initial commit:

```bash
git add .
git commit -m "Initialize project from KD UI"
```

## Using a Component

Import the component macro into a Jinja template:

```jinja
{% from "components/file_upload.html" import file_upload %}
```

Render it where needed:

```jinja
<form method="post" enctype="multipart/form-data">
  <div id="photo-preview-container" class="hidden">
    <img
      id="photo-preview"
      alt="Selected photo preview"
      class="max-h-80 w-full object-contain"
    />
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

  <button type="submit" class="btn">Save</button>
</form>
```

Some components have an optional JavaScript controller. Include it in the
application's base layout:

```jinja
<script
  src="{{ url_for('static', filename='js/components/file_upload.js') }}"
  defer
></script>
```

Always validate uploaded files and form data on the server. Browser validation
is only a user-experience improvement.

## Components and Blocks

Components are reusable interface primitives stored in:

```text
app/templates/components/
```

Current examples include:

- Action Menu
- Alert
- Card
- Data Table
- Empty State
- File Upload
- Metric Pill
- Page Header
- Pagination
- Search Filter
- Stat Card
- Timeline

Blocks are larger page or section compositions stored in:

```text
app/templates/blocks/
```

Current examples include dashboards, list pages, detail pages, forms, settings,
login, and landing pages.

Application-specific business logic should remain in the consuming application
and should not be promoted to KD UI.

## Basecoat UI

Basecoat provides the underlying UI engine. Vendored Basecoat files live in:

```text
app/templates/basecoat/
app/static/js/vendor/
app/static/css/basecoat-vega.css
```

The following command copies Basecoat assets from the installed npm package
into the current repository:

```bash
npm run sync:basecoat
```

This command does not communicate with KD UI or GitHub. It only copies files
from `node_modules/basecoat-css/`. Run it after upgrading `basecoat-css`.

## Tailwind CSS

Tailwind is compiled ahead of time. After adding or changing Tailwind classes
in a template, rebuild the CSS:

```bash
npm run build:css
```

During active UI development, use:

```bash
npm run watch:css
```

Flask's debug reload does not rebuild Tailwind CSS. A component may appear
broken or unstyled if its classes were added after the last CSS build.

## Improving a Component in a Real Project

Reusable components should be developed in a real application first. For
example, Estate Copilot may need a new upload control.

1. Check whether Basecoat already provides the required primitive.
2. Check whether KD UI already contains a suitable component.
3. Prototype the solution in the real application page.
4. Test it with real data and realistic content.
5. Test desktop and mobile layouts.
6. Extract reusable behavior into a Jinja macro.
7. Remove application-specific names, routes, and text.
8. Add documented parameters and a `class_=""` override.
9. Move reusable JavaScript into a same-named component controller.
10. Promote the finished component into KD UI.
11. Add a generic example to the KD UI gallery.
12. Rebuild and verify KD UI before committing.

Do not promote business logic, database queries, estate-specific routes, or
application-specific forms unless they have been generalized into a genuinely
reusable block.

## Component Contract

A reusable KD UI component should:

- Be a documented Jinja macro.
- Include a usage example.
- Document required and optional parameters.
- Accept `class_=""` for layout customization.
- Reuse Basecoat primitives where possible.
- Avoid hardcoded application-specific content.
- Work without JavaScript where practical.
- Use instance-scoped data attributes when JavaScript is required.
- Support multiple instances on the same page.
- Remain usable on desktop and mobile.
- Require server-side validation for submitted data.

Reusable JavaScript should be stored at:

```text
app/static/js/components/<component_name>.js
```

The Jinja macro and JavaScript controller should use the same base name.

## Auditing a Prototype Project

KD UI includes an optional helper for comparing another Flask/Jinja project
with this repository. Run it from the KD UI repository:

```bash
python scripts/kdui_promote.py status \
  --source /absolute/path/to/project \
  --kind component
```

The audit reports:

```text
= identical
~ different
+ missing from KD UI
i KD UI only
```

A difference is not automatically an error. Some application-specific
differences are intentional and should not be promoted.

## Promoting a Component

Preview the operation first:

```bash
python scripts/kdui_promote.py component file_upload \
  --source /absolute/path/to/project \
  --dry-run
```

Promote the component:

```bash
python scripts/kdui_promote.py component file_upload \
  --source /absolute/path/to/project
```

Promote a reusable block:

```bash
python scripts/kdui_promote.py block dashboard \
  --source /absolute/path/to/project
```

The helper copies only the explicitly named template. If a same-named
controller exists, it is also copied from:

```text
app/static/js/components/<component_name>.js
```

The helper does not:

- Copy an entire application.
- Update the KD UI gallery automatically.
- Commit changes.
- Push to GitHub.
- Modify the source project.

After promotion:

```bash
npm run build:css
git diff
git status
```

Add or update the component example in:

```text
app/templates/gallery/components.html
```

Blocks are documented in:

```text
app/templates/gallery/blocks.html
```

## Manually Promoting a Component

The helper is optional. Components can also be copied manually:

```bash
cp /path/to/project/app/templates/components/example.html \
   app/templates/components/example.html
```

If the component has JavaScript:

```bash
cp /path/to/project/app/static/js/components/example.js \
   app/static/js/components/example.js
```

After copying, update the KD UI gallery, rebuild CSS, and review the Git diff.

## Bringing a KD UI Improvement Back Into an Application

The promotion helper currently works from a prototype into KD UI. To bring a
later KD UI improvement back into an application, copy the updated files
manually:

```bash
cp app/templates/components/example.html \
   /path/to/project/app/templates/components/example.html
```

Copy its controller when applicable:

```bash
cp app/static/js/components/example.js \
   /path/to/project/app/static/js/components/example.js
```

Then rebuild CSS and test the consuming application.

## UI Gallery

The gallery is KD UI's visual catalog and regression environment. Every
reusable component should have:

- A live rendered example.
- A short description.
- A Jinja usage example.
- Generic sample content.
- Desktop verification.
- Mobile verification.

The gallery is development tooling. It should not be copied into production
applications unless there is a deliberate reason to expose it.

## Optional Page Scaffolding

KD UI includes a Flask command for generating starter resource pages:

```bash
flask --app wsgi scaffold resource invoices \
  --fields "number,client,amount:currency,status:badge,due:date" \
  --icon file-text
```

The scaffold creates a starting point. Generated pages should still be
reviewed, connected to real data, and tested before use.

## Project Structure

```text
app/
  blueprints/                 Flask routes and example data
  templates/
    basecoat/                 Vendored Basecoat macros
    components/               Reusable KD UI macros
    blocks/                   Reusable page compositions
    gallery/                  KD UI showroom
    layouts/                  Base application layouts
  static/
    css/
      input.css               Tailwind source
      output.css              Compiled CSS
    js/
      components/             Reusable component controllers
      vendor/                 Basecoat JavaScript

scripts/
  kdui_promote.py             Audit and promote reusable UI
  sync_basecoat.mjs           Vendor Basecoat assets

AGENTS.md                     Development conventions
HOWTO.md                      Detailed usage reference
```

## Publishing Changes to KD UI

Before committing:

```bash
npm run build:css
git diff --check
git status
git diff
```

Commit only the intended component, controller, gallery, documentation, and
generated CSS changes.

Example:

```bash
git add app/templates/components/example.html
git add app/templates/gallery/components.html
git add app/static/css/output.css
git commit -m "Add example component"
git push
```

## Design Principles

- Server-rendered Flask and Jinja first.
- Basecoat before custom low-level primitives.
- Tailwind for layout and application-specific adjustments.
- Minimal JavaScript.
- Progressive enhancement.
- Mobile support by default.
- Real application validation before library promotion.
- Explicit copying instead of hidden synchronization.
- No automatic commits or pushes.

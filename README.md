# KD UI

KD UI is an installable library of polished, Basecoat-powered Jinja macros for
server-rendered Flask applications. This repository contains the library and its
live showroom—no fake CRM and no application generator.

## Use KD UI in a Flask project

Install a tagged release from Git:

```bash
pip install "flask-kdui @ git+https://github.com/windseeker5/kdui.git@v0.3.0"
```

Register the extension:

```python
from flask import Flask
from kdui import KDUI

app = Flask(__name__)
KDUI(app)
```

Load the packaged assets in the base layout:

```jinja
{% from "kdui/assets.html" import styles, scripts %}
<head>{{ styles() }}</head>
<body>
  {% block body %}{% endblock %}
  {{ scripts() }}
</body>
```

Import a component or pattern:

```jinja
{% from "kdui/components/card.html" import card %}
{% from "kdui/patterns/form_page.html" import form_page %}
```

Applications should pin a release and upgrade deliberately. During local
library development, use `pip install -e /path/to/kdui`.

## Run the showroom

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci
python wsgi.py --port 5005
```

Open:

- `http://127.0.0.1:5005/` — KD UI landing page
- `http://127.0.0.1:5005/ui/components` — component gallery
- `http://127.0.0.1:5005/ui/patterns` — composed patterns
- `http://127.0.0.1:5005/ui/maintainer` — maintainer guide

## Repository responsibilities

- `src/kdui/templates/kdui/components/` — reusable Jinja components
- `src/kdui/templates/kdui/patterns/` — reusable compositions
- `src/kdui/templates/kdui/basecoat/` — synchronized vendor macros
- `src/kdui/static/kdui/` — packaged compiled assets
- `app/` — showroom only
- `tests/` — package and rendering smoke tests

Maintainers use npm only to synchronize Basecoat and compile CSS:

```bash
npm run build
pytest
```

## To promote from apps

Generic pieces built inside consumer apps (mainly minicrm) that are not in KD UI
yet. Generalize each one (no app routes, data or wording), add a gallery demo and
a test, then remove the app's private copy.

- Avatar with photo-over-initials fallback (`minicrm/app/templates/crm/avatar.html`)
- Segmented control, chips and icon pill picker (`.crm-seg`, `.crm-chip`, `.crm-kind-pill`)
- Typed-phrase confirm dialog (`data-wipe-phrase`)
- Textarea placeholder highlighter (`data-hilite`) and narrow-screen Edit/Preview tabs
- Small behaviours: copy button, unsaved-changes guard, POST link with CSRF, focus first error
- App shell: sticky top bar with search, remembered sidebar toggle (Ctrl/⌘+B), flash toasts
- Profile card with clamped note, and activity feed with filter tabs

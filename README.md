# KD UI

KD UI is an installable library of polished, Basecoat-powered Jinja macros for
server-rendered Flask applications. This repository contains the library and its
live showroom—no fake CRM and no application generator.

## Use KD UI in a Flask project

Install a tagged release from Git:

```bash
pip install "flask-kdui @ git+https://github.com/windseeker5/kdui.git@v0.2.0"
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

# KD UI

KD UI is a toolbox for Flask developers who want to turn an idea into a useful,
good-looking prototype quickly. You focus on Python, application behavior, and
your database. KD UI provides the polished visual foundation.

Generated applications use normal Flask and Jinja with precompiled Basecoat UI
styling. They do **not** require React, Vue, TypeScript, Node.js, or npm.

## 1. Get the Toolbox

First time:

```bash
cd ~/projects
git clone https://github.com/windseeker5/kdui.git flask-shadcn-starter
cd flask-shadcn-starter
```

Already cloned it? Update it before generating an application:

```bash
cd ~/projects/flask-shadcn-starter
git pull
```

Keep this toolbox separate from the applications it creates.

## 2. Create a To-do Application

From inside the toolbox:

```bash
python scripts/kdui.py new ../my-todo
```

This creates a separate application:

```text
projects/
├── flask-shadcn-starter/   # KD UI toolbox
└── my-todo/                # your Flask application
```

## 3. Run the Application

```bash
cd ../my-todo
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py
```

Open <http://127.0.0.1:5005>.

The generated example can add, complete, and delete tasks. It stores tasks in
memory so you can understand the complete application before choosing a
database.

## Generated Project

```text
my-todo/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   ├── components/
│   │   ├── layouts/
│   │   └── todos/
│   └── static/
│       ├── css/
│       └── js/
├── requirements.txt
└── wsgi.py
```

- `app/routes.py` contains normal Flask routes.
- `app/templates/todos/index.html` is the Jinja page.
- `app/templates/components/` contains reusable UI pieces.
- `app/static/` contains ready-to-use compiled assets.

Replace the in-memory list in `app/routes.py` with your database when ready.

## Add a Component

List available components:

```bash
python scripts/kdui.py list components
```

Copy one component into an application:

```bash
python scripts/kdui.py add component card --target ../my-todo
```

The command copies only the requested component and its required support files.
It does not copy the gallery, demonstration pages, or KD UI development files.

## Why No npm?

KD UI distributes compiled CSS and JavaScript with generated applications.
Application developers can therefore work with Python, Flask, Jinja, and their
database without installing Node.js.

npm is used only while maintaining KD UI itself:

```bash
npm install
npm run build:css
```

These commands compile Tailwind CSS and synchronize Basecoat assets before the
finished files are distributed by the Python generator.

## Run the KD UI Showroom

To work on KD UI itself:

```bash
pip install -r requirements.txt
python wsgi.py
```

Open:

- <http://127.0.0.1:5005/ui/how-it-works> — create an application
- <http://127.0.0.1:5005/ui/maintainer> — maintain and contribute to Flask Starter
- <http://127.0.0.1:5005/ui/components> — component examples
- <http://127.0.0.1:5005/ui/blocks> — complete page examples

KD UI maintainers who change Tailwind classes should rebuild the committed CSS:

```bash
npm install
npm run build:css
```

## Development Principles

- Flask and Jinja first
- Server-rendered behavior by default
- Basecoat for visual primitives
- Minimal JavaScript
- Copy only what an application needs
- Keep the KD UI toolbox separate from generated applications

Advanced maintenance and contribution notes remain in `HOWTO.md` and
`AGENTS.md`.

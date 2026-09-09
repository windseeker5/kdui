"""Create small Flask applications and copy KD UI components into them.

Examples:
    python scripts/kdui.py new ../my-todo
    python scripts/kdui.py add component card --target ../my-todo
    python scripts/kdui.py list components

Generated applications use committed, precompiled UI assets. They do not need
Node.js or npm.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


KDUI_ROOT = Path(__file__).resolve().parents[1]
APP_SOURCE = KDUI_ROOT / "app"
SAFE_NAME = re.compile(r"^[a-z0-9_]+$")
BASECOAT_IMPORT = re.compile(r'{%\s*from\s+"(basecoat/[^"]+)"')
COMPONENT_IMPORT = re.compile(r'{%\s*from\s+"components/([a-z0-9_]+)\.html"')


FILES = {
    "requirements.txt": """flask>=3.0.0
""",
    "wsgi.py": """import argparse

from app import create_app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask development server.")
    parser.add_argument("--host", default="127.0.0.1", help="Address to listen on. Use 0.0.0.0 for your local network.")
    parser.add_argument("--port", type=int, required=True, help="Port to listen on, for example 5055.")
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port)
""",
    "app/__init__.py": """from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-change-me"

    from app.routes import todo_bp
    app.register_blueprint(todo_bp)

    return app
""",
    "app/routes.py": """from flask import Blueprint, redirect, render_template, request, url_for


todo_bp = Blueprint("todo", __name__)

# A tiny in-memory example. Replace this list with your database when ready.
TODOS = [
    {"id": 1, "title": "Learn how this page works", "done": True},
    {"id": 2, "title": "Build something useful", "done": False},
]


@todo_bp.get("/")
def index():
    return render_template("todos/index.html", todos=TODOS)


@todo_bp.post("/todos")
def create_todo():
    title = request.form.get("title", "").strip()
    if title:
        next_id = max((todo["id"] for todo in TODOS), default=0) + 1
        TODOS.append({"id": next_id, "title": title, "done": False})
    return redirect(url_for("todo.index"))


@todo_bp.post("/todos/<int:todo_id>/toggle")
def toggle_todo(todo_id):
    todo = next((item for item in TODOS if item["id"] == todo_id), None)
    if todo:
        todo["done"] = not todo["done"]
    return redirect(url_for("todo.index"))


@todo_bp.post("/todos/<int:todo_id>/delete")
def delete_todo(todo_id):
    TODOS[:] = [item for item in TODOS if item["id"] != todo_id]
    return redirect(url_for("todo.index"))
""",
    "app/templates/layouts/base.html": """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}My Flask App{% endblock %}</title>
  <script>
    (() => {
      try {
        const stored = localStorage.getItem("themeMode");
        if (stored ? stored === "dark" : matchMedia("(prefers-color-scheme: dark)").matches) {
          document.documentElement.classList.add("dark");
        }
      } catch (_) {}
    })();
  </script>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/kdui.css') }}">
</head>
<body class="min-h-screen bg-background text-foreground">
  {% block body %}{% endblock %}
  <script src="{{ url_for('static', filename='js/vendor/basecoat.all.min.js') }}" defer></script>
  <!-- KDUI:COMPONENT_SCRIPTS -->
  {% block scripts %}{% endblock %}
</body>
</html>
""",
    "app/templates/todos/index.html": """{% extends "layouts/base.html" %}
{% from "components/empty_state.html" import empty_state %}

{% block title %}My To-do List{% endblock %}

{% block body %}
<main class="mx-auto max-w-2xl p-4 md:p-8">
  <header class="mb-6 flex items-center justify-between gap-4">
    <div>
      <h1 class="text-2xl font-semibold tracking-tight">My to-do list</h1>
      <p class="mt-1 text-sm text-muted-foreground">A small Flask application created with KD UI.</p>
    </div>
    <button type="button" class="btn" data-variant="outline" data-size="icon" aria-label="Toggle dark mode" onclick="window.basecoat.theme.toggle()">
      <svg class="size-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
    </button>
  </header>

  <div class="card">
    <header>
      <h2>Tasks</h2>
      <p>Add a task, mark it complete, or remove it.</p>
    </header>
    <section>
      <form method="post" action="{{ url_for('todo.create_todo') }}" class="mb-5 flex gap-2">
        <label class="sr-only" for="title">New task</label>
        <input class="input" id="title" name="title" placeholder="What needs to be done?" required>
        <button class="btn" type="submit">Add</button>
      </form>

      {% if todos %}
      <ul class="divide-y">
        {% for todo in todos %}
        <li class="flex items-center gap-3 py-3">
          <form method="post" action="{{ url_for('todo.toggle_todo', todo_id=todo.id) }}">
            <button class="btn" data-variant="outline" data-size="icon-sm" aria-label="Mark {{ todo.title }} {{ 'incomplete' if todo.done else 'complete' }}">
              {% if todo.done %}✓{% else %}<span aria-hidden="true">○</span>{% endif %}
            </button>
          </form>
          <span class="min-w-0 flex-1 {{ 'text-muted-foreground line-through' if todo.done else '' }}">{{ todo.title }}</span>
          <form method="post" action="{{ url_for('todo.delete_todo', todo_id=todo.id) }}">
            <button class="btn" data-variant="ghost" data-size="sm">Delete</button>
          </form>
        </li>
        {% endfor %}
      </ul>
      {% else %}
        {{ empty_state(title="No tasks yet", description="Add your first task above.") }}
      {% endif %}
    </section>
  </div>

  <p class="mt-4 text-center text-xs text-muted-foreground">Example data is stored in memory and resets when Flask restarts.</p>
</main>
{% endblock %}
""",
}


STATIC_FILES = (
    "css/output.css",
    "css/kdui.css",
    "js/vendor/basecoat.all.min.js",
)


def write_file(target: Path, relative: str, content: str) -> None:
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    print(f"  created  {relative}")


def copy_file(source: Path, destination: Path, label: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    print(f"  copied   {label}")


def copy_foundation(target: Path) -> None:
    for relative in STATIC_FILES:
        copy_file(
            APP_SOURCE / "static" / relative,
            target / "app" / "static" / relative,
            f"app/static/{relative}",
        )


def new_app(args: argparse.Namespace) -> None:
    target = args.target.expanduser().resolve()
    if target.exists() and not target.is_dir():
        raise SystemExit(f"Target is not a folder: {target}")
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Target folder is not empty: {target}")
    target.mkdir(parents=True, exist_ok=True)

    print(f"\nCreating a Flask to-do application in {target}\n")
    for relative, content in FILES.items():
        write_file(target, relative, content)
    copy_foundation(target)
    copy_component("empty_state", target)

    print("\nDone. Run:\n")
    print(f"  cd {target}")
    print("  python -m venv .venv")
    print("  source .venv/bin/activate       # Windows: .venv\\Scripts\\activate")
    print("  pip install -r requirements.txt")
    print("  python wsgi.py --port 5055")
    print("\nOpen http://127.0.0.1:5055\n")
    print("Change 5055 to any available port.")
    print("For trusted local-network access, add: --host 0.0.0.0")
    print("No npm install is required.")


def copy_component(name: str, target: Path, seen: set[str] | None = None) -> None:
    if not SAFE_NAME.fullmatch(name):
        raise SystemExit("Component names use lowercase letters, numbers, and underscores only.")

    seen = seen if seen is not None else set()
    if name in seen:
        return
    seen.add(name)

    source = APP_SOURCE / "templates" / "components" / f"{name}.html"
    if not source.is_file():
        raise SystemExit(f"Unknown component: {name}. Run 'list components' to see available names.")

    destination = target / "app" / "templates" / "components" / source.name
    copy_file(source, destination, f"app/templates/components/{source.name}")

    content = source.read_text(encoding="utf-8")
    for basecoat_template in sorted(set(BASECOAT_IMPORT.findall(content))):
        dependency = APP_SOURCE / "templates" / basecoat_template
        copy_file(dependency, target / "app" / "templates" / basecoat_template, f"app/templates/{basecoat_template}")

    for component_name in sorted(set(COMPONENT_IMPORT.findall(content))):
        copy_component(component_name, target, seen)

    controller = APP_SOURCE / "static" / "js" / "components" / f"{name}.js"
    if controller.is_file():
        relative_controller = Path("app/static/js/components") / controller.name
        copy_file(controller, target / relative_controller, str(relative_controller))
        add_component_script(target, name)


def add_component_script(target: Path, name: str) -> None:
    layout = target / "app" / "templates" / "layouts" / "base.html"
    if not layout.is_file():
        print("  note     load the copied JavaScript controller in your base layout")
        return

    script = f"  <script src=\"{{{{ url_for('static', filename='js/components/{name}.js') }}}}\" defer></script>"
    content = layout.read_text(encoding="utf-8")
    if script in content:
        return
    marker = "  <!-- KDUI:COMPONENT_SCRIPTS -->"
    if marker not in content:
        print("  note     load the copied JavaScript controller in your base layout")
        return
    layout.write_text(content.replace(marker, f"{script}\n{marker}", 1), encoding="utf-8")
    print("  updated  app/templates/layouts/base.html")


def add_component(args: argparse.Namespace) -> None:
    target = args.target.expanduser().resolve()
    if not (target / "app" / "templates").is_dir():
        raise SystemExit(f"Not a generated Flask project: {target}")

    print(f"\nAdding component '{args.name}' to {target}\n")
    copy_foundation(target)
    copy_component(args.name, target)
    print("\nDone. No npm command is required.\n")


def list_components(_args: argparse.Namespace) -> None:
    for path in sorted((APP_SOURCE / "templates" / "components").glob("*.html")):
        print(path.stem)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create Flask apps with selected KD UI components.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a minimal Flask to-do application.")
    new_parser.add_argument("target", type=Path, help="New application folder.")
    new_parser.set_defaults(handler=new_app)

    add_parser = subparsers.add_parser("add", help="Copy one UI item into an application.")
    add_subparsers = add_parser.add_subparsers(dest="kind", required=True)
    component_parser = add_subparsers.add_parser("component", help="Copy one Jinja component.")
    component_parser.add_argument("name")
    component_parser.add_argument("--target", type=Path, default=Path.cwd())
    component_parser.set_defaults(handler=add_component)

    list_parser = subparsers.add_parser("list", help="List available UI items.")
    list_subparsers = list_parser.add_subparsers(dest="kind", required=True)
    components_parser = list_subparsers.add_parser("components")
    components_parser.set_defaults(handler=list_components)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()

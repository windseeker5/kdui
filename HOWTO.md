# How to Use KD UI

KD UI helps Flask developers turn an idea into a useful, polished prototype
without designing every interface element. Your application lives in its own
folder and receives only the UI files it needs.

## 1. Get the Toolbox

First time:

```bash
cd ~/projects
git clone https://github.com/windseeker5/kdui.git flask-shadcn-starter
cd flask-shadcn-starter
```

Already cloned it? Update it before creating an application:

```bash
cd ~/projects/flask-shadcn-starter
git pull
```

## 2. Create an Application

From inside the toolbox:

```bash
python scripts/kdui.py new ../my-todo
```

The folders stay separate:

```text
projects/
├── flask-shadcn-starter/   # toolbox and component showroom
└── my-todo/                # independent Flask application
```

## 3. Run the To-do Example

```bash
cd ../my-todo
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py --port 5055
```

Open <http://127.0.0.1:5055>. Replace `5055` with any available port.

For access from another device on a trusted local network:

```bash
python wsgi.py --host 0.0.0.0 --port 5055
```

Open `http://YOUR-COMPUTER-IP:5055` on that device. Never expose Flask debug
mode to the public internet or an untrusted network.

No npm command is required. The generator copies precompiled CSS and JavaScript.

## 4. Understand the Example

The generated application contains:

```text
app/routes.py                         Flask behavior and temporary task data
app/templates/todos/index.html       To-do page
app/templates/layouts/base.html      Shared HTML layout
app/templates/components/            Reusable Jinja UI
app/static/css/                       Precompiled styling
app/static/js/                        Precompiled browser behavior
```

The request flow is ordinary Flask:

1. The browser submits a form.
2. A route in `app/routes.py` changes the task list.
3. Flask redirects to the index route.
4. Jinja renders the updated HTML.

The example stores tasks in memory. Replace the `TODOS` list with your database
model and queries when ready.

## 5. Add a UI Component

See available components:

```bash
python scripts/kdui.py list components
```

Copy one into the to-do application:

```bash
python scripts/kdui.py add component card --target ../my-todo
```

The command refreshes compatible compiled assets and copies:

- The requested Jinja component
- A required Basecoat template, if the component uses one
- A same-named JavaScript controller, if the component needs one

It does not copy the KD UI gallery or demonstration applications.

Import the copied component in Jinja:

```jinja
{% from "components/card.html" import card %}

{% call card(title="Today") %}
  <p>Finish the prototype.</p>
{% endcall %}
```

## 6. Add Your Database

KD UI does not choose a database package. Install and configure the library you
normally use, then replace the temporary list in `app/routes.py`.

Keep responsibilities simple:

- Flask loads and validates data.
- Your database layer stores data.
- Jinja displays data.
- KD UI components provide the interface.

## Why Application Developers Do Not Need npm

The generated application receives finished CSS and JavaScript files. Node.js
is not part of the Flask server.

npm is only required when maintaining KD UI itself—for example, after changing
Tailwind classes or upgrading Basecoat:

```bash
npm install
npm run build:css
```

The Python generator then distributes those finished assets to applications.

## Working on KD UI Itself

Run the showroom:

```bash
pip install -r requirements.txt
python wsgi.py --port 5005
```

Useful pages:

```text
http://127.0.0.1:5005/ui/how-it-works     # application developer guide
http://127.0.0.1:5005/ui/maintainer       # maintainer and contributor guide
http://127.0.0.1:5005/ui/components
http://127.0.0.1:5005/ui/blocks
```

Reusable UI should be tested in a real application, generalized, demonstrated
in the gallery, and reviewed before being added to KD UI.

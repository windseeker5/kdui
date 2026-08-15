"""
Flask CLI scaffold commands.

Usage:
    flask --app wsgi scaffold resource <name> --fields "name,owner,status:badge,due:date" --icon folder-kanban

Field types:
    text      plain text column + text input (default)
    badge     badge column + select input (Active/Inactive)
    date      date column + date input
    email     email column + email input
    currency  right-aligned currency column + number input
    number    right-aligned number column + number input
"""

import os
import click
from flask import current_app
from flask.cli import AppGroup

scaffold_cli = AppGroup("scaffold", help="Generate new pages and resources.")

# ---------------------------------------------------------------------------
# Lucide SVG paths - a small curated set for the sidebar icon argument.
# For any icon not listed here, a generic square is used.
# ---------------------------------------------------------------------------
LUCIDE_PATHS = {
    "folder-kanban": '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/><path d="M8 10v4"/><path d="M12 10v2"/><path d="M16 10v6"/>',
    "briefcase": '<rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "list": '<line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/>',
    "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "shopping-cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "bar-chart": '<line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/>',
    "settings": '<path d="M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915"/><circle cx="12" cy="12" r="3"/>',
}
DEFAULT_ICON_PATH = '<rect width="18" height="18" x="3" y="3" rx="2"/>'


def _icon_svg(icon_name):
    paths = LUCIDE_PATHS.get(icon_name, DEFAULT_ICON_PATH)
    return (
        '<svg class="lucide lucide-' + icon_name + '" '
        'xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        + paths + '</svg>'
    )


# ---------------------------------------------------------------------------
# Field parsing
# ---------------------------------------------------------------------------

VALID_TYPES = {"text", "badge", "date", "email", "currency", "number"}


def parse_fields(fields_str):
    result = []
    for part in fields_str.split(","):
        part = part.strip()
        if ":" in part:
            fname, ftype = part.split(":", 1)
        else:
            fname, ftype = part, "text"
        fname = fname.strip().lower().replace(" ", "_")
        ftype = ftype.strip().lower()
        if ftype not in VALID_TYPES:
            raise click.BadParameter(
                "Unknown field type '{}' for field '{}'. Valid types: {}".format(
                    ftype, fname, ", ".join(sorted(VALID_TYPES)))
            )
        result.append({"name": fname, "type": ftype})
    return result


def to_label(field_name):
    return field_name.replace("_", " ").title()


# ---------------------------------------------------------------------------
# Sample data generator
# ---------------------------------------------------------------------------

def _sample_value(field, row_index):
    ftype = field["type"]
    fname = field["name"]
    lbl = to_label(fname)
    samples = {
        "text":     ["Sample " + lbl + " 1", "Example " + lbl + " 2", "Demo " + lbl + " 3"],
        "badge":    ["Active", "Inactive", "Active"],
        "date":     ["2026-09-01", "2026-10-15", "2026-12-01"],
        "email":    ["user1@example.com", "contact2@demo.com", "info3@sample.com"],
        "currency": ["$1,200.00", "$850.00", "$3,400.00"],
        "number":   ["10", "25", "7"],
    }
    return samples.get(ftype, ["-", "-", "-"])[row_index - 1]


def generate_fake_data(name, fields):
    rows = []
    for i in range(1, 4):
        values = {f["name"]: _sample_value(f, i) for f in fields}
        values_str = ", ".join('"{}": "{}"'.format(k, v) for k, v in values.items())
        rows.append('    {{"id": {}, {}}}'.format(i, values_str))
    rows_str = ",\n".join(rows)
    return '"""Fake data for the {} resource. Replace with real DB queries."""\n\n{} = [\n{},\n]\n'.format(
        name, name.upper(), rows_str)


# ---------------------------------------------------------------------------
# Blueprint generators
# ---------------------------------------------------------------------------

def generate_bp_init(name):
    return (
        "from flask import Blueprint\n\n"
        "{}_bp = Blueprint(\"{}\", __name__, url_prefix=\"/app\")\n\n"
        "from app.blueprints.{} import routes  # noqa: E402, F401\n"
    ).format(name, name, name)


def generate_routes(name, fields):
    sort_default = fields[0]["name"] if fields else "id"
    badge_fields = [f for f in fields if f["type"] == "badge"]
    filter_var = badge_fields[0]["name"] if badge_fields else None

    filter_arg_def = ', {}=""'.format(filter_var) if filter_var else ""
    filter_body = (
        '\n    if {}:\n        rows = [r for r in rows if r["{}"].lower() == {}.lower()]'.format(
            filter_var, filter_var, filter_var)
        if filter_var else ""
    )
    filter_get = (
        '\n    {} = request.args.get("{}", "")'.format(filter_var, filter_var)
        if filter_var else "\n    # no badge filter"
    )
    filter_call = ", {}={}".format(filter_var, filter_var) if filter_var else ""
    filter_render = "\n        {}={},".format(filter_var, filter_var) if filter_var else ""

    lines = []
    lines.append("from flask import render_template, request, abort")
    lines.append("from app.blueprints.{} import {}_bp".format(name, name))
    lines.append("from app.blueprints.{}.fake_data import {}".format(name, name.upper()))
    lines.append("")
    lines.append("PAGE_SIZE = 10")
    lines.append("")
    lines.append("")
    lines.append("def _filter(rows, q{}):".format(filter_arg_def))
    lines.append("    if q:")
    lines.append("        q_l = q.lower()")
    lines.append("        rows = [r for r in rows if any(q_l in str(v).lower() for v in r.values())]")
    if filter_var:
        lines.append('    if {}:'.format(filter_var))
        lines.append('        rows = [r for r in rows if r["{}"].lower() == {}.lower()]'.format(filter_var, filter_var))
    lines.append("    return rows")
    lines.append("")
    lines.append("")
    lines.append('@{}_bp.route("/{}")'.format(name, name))
    lines.append("def list_{}():".format(name))
    lines.append('    q     = request.args.get("q", "")')
    if filter_var:
        lines.append('    {} = request.args.get("{}", "")'.format(filter_var, filter_var))
    lines.append('    sort  = request.args.get("sort", "{}")'.format(sort_default))
    lines.append('    order = request.args.get("order", "asc")')
    lines.append('    page  = max(1, int(request.args.get("page", 1)))')
    lines.append("")
    lines.append("    rows = _filter({}, q{})".format(name.upper(), filter_call))
    lines.append('    rows = sorted(rows, key=lambda r: str(r.get(sort, "")), reverse=(order == "desc"))')
    lines.append("")
    lines.append("    total       = len(rows)")
    lines.append("    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)")
    lines.append("    page        = min(page, total_pages)")
    lines.append("    rows        = rows[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]")
    lines.append("")
    lines.append("    return render_template(")
    lines.append('        "blocks/{}_list.html",'.format(name))
    lines.append("        {}_list=rows,".format(name))
    lines.append("        q=q,{}".format(filter_render))
    lines.append("        sort=sort,")
    lines.append("        order=order,")
    lines.append("        page=page,")
    lines.append("        total_pages=total_pages,")
    lines.append("        total=total,")
    lines.append("    )")
    lines.append("")
    lines.append("")
    lines.append('@{}_bp.route("/{}/new")'.format(name, name))
    lines.append("def new_{}():".format(name))
    lines.append('    return render_template("blocks/{}_form.html", item=None)'.format(name))
    lines.append("")
    lines.append("")
    lines.append('@{}_bp.route("/{}/int:item_id")'.format(name, name) .replace("int:item_id", "<int:item_id>"))
    lines.append("def detail_{}(item_id):".format(name))
    lines.append("    item = next((r for r in {} if r[\"id\"] == item_id), None)".format(name.upper()))
    lines.append("    if not item:")
    lines.append("        abort(404)")
    lines.append('    return render_template("blocks/{}_detail.html", item=item)'.format(name))
    lines.append("")
    lines.append("")
    lines.append('@{}_bp.route("/{}/int:item_id/edit")'.format(name, name).replace("int:item_id", "<int:item_id>"))
    lines.append("def edit_{}(item_id):".format(name))
    lines.append("    item = next((r for r in {} if r[\"id\"] == item_id), None)".format(name.upper()))
    lines.append("    if not item:")
    lines.append("        abort(404)")
    lines.append('    return render_template("blocks/{}_form.html", item=item)'.format(name))
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Template generators
# ---------------------------------------------------------------------------

def _td_cell(f):
    v = "row." + f["name"]
    if f["type"] == "badge":
        return (
            "  <td>"
            '<span class="badge" '
            "data-variant=\"{{ 'secondary' if " + v + " == 'Inactive' else 'outline' }}\">"
            "{{ " + v + " }}</span></td>"
        )
    if f["type"] in ("currency", "number"):
        return "  <td class=\"text-end\">{{ " + v + " }}</td>"
    if f["type"] == "email":
        return "  <td class=\"text-muted-foreground\">{{ " + v + " }}</td>"
    return "  <td>{{ " + v + " }}</td>"


def _form_field(f):
    fname = f["name"]
    ftype = f["type"]
    lbl = to_label(fname)
    val = "{{ item." + fname + ' if item else "" }}'

    if ftype == "badge":
        return (
            '        <div class="grid gap-2">\n'
            '          <label class="label" for="{}">{}</label>\n'.format(fname, lbl) +
            '          <select class="input" id="{}" name="{}">\n'.format(fname, fname) +
            '            <option value="Active" {{ "selected" if item and item.' + fname + ' == "Active" else "" }}>Active</option>\n'
            '            <option value="Inactive" {{ "selected" if item and item.' + fname + ' == "Inactive" else "" }}>Inactive</option>\n'
            '          </select>\n'
            '        </div>'
        )
    if ftype == "email":
        input_type = "email"
    elif ftype == "date":
        input_type = "date"
    elif ftype in ("currency", "number"):
        input_type = "number"
    else:
        input_type = "text"

    placeholder = "" if ftype in ("date", "email", "currency", "number") else ' placeholder="{}..."'.format(lbl)
    return (
        '        <div class="grid gap-2">\n'
        '          <label class="label" for="{}">{}</label>\n'.format(fname, lbl) +
        '          <input class="input" type="{}" id="{}" name="{}" value="{}"{} />\n'.format(
            input_type, fname, fname, val, placeholder) +
        '        </div>'
    )


def generate_list_template(name, fields, icon):
    Names = name.capitalize() + "s"
    badge_fields = [f for f in fields if f["type"] == "badge"]
    bf = badge_fields[0]["name"] if badge_fields else None

    filter_extra = ""
    if bf:
        filter_extra = (
            ',\n  filters=[\n'
            '    {\n'
            '      "name": "' + bf + '",\n'
            '      "options": [("", "All"), ("active", "Active"), ("inactive", "Inactive")],\n'
            '      "value": ' + bf + '\n'
            '    }\n'
            '  ]'
        )

    filter_tpl_var = ', "{}": {}'.format(bf, bf) if bf else ""

    columns = []
    for f in fields:
        sortable = "false" if f["type"] == "badge" else "true"
        columns.append('  {{"key": "{}", "label": "{}", "sortable": {}}}'.format(
            f["name"], to_label(f["name"]), sortable))
    columns.append('  {"key": "_actions", "label": "", "sortable": false}')
    columns_str = ",\n".join(columns)

    td_cells = "\n".join(_td_cell(f) for f in fields)

    lines = []
    lines.append('{% extends "layouts/app.html" %}')
    lines.append('{% from "components/page_header.html"   import page_header %}')
    lines.append('{% from "components/search_filter.html" import search_filter %}')
    lines.append('{% from "components/data_table.html"    import data_table %}')
    lines.append('{% from "components/pagination.html"    import pagination %}')
    lines.append("")
    lines.append("{{% block title %}}{} - App{{% endblock %}}".format(Names))
    lines.append("{{% block breadcrumb %}}{}{{% endblock %}}".format(Names))
    lines.append("")
    lines.append("{% block content %}")
    lines.append("")
    lines.append("{{ page_header(")
    lines.append('  title="{}",'.format(Names))
    lines.append('  description="Manage your {} records.",'.format(name))
    lines.append("  action='<a href=\"' ~ url_for(\"{}.new_{}\") ~ '\" class=\"btn\">".format(name, name))
    lines.append('<svg data-icon="inline-start" class="lucide lucide-plus" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>')
    lines.append("Add {}</a>'".format(name))
    lines.append(") }}")
    lines.append("")
    lines.append("{{ search_filter(")
    lines.append('  action=url_for("{}.list_{}"),'.format(name, name))
    lines.append("  q=q" + filter_extra)
    lines.append(") }}")
    lines.append("")
    lines.append('<p class="text-sm text-muted-foreground mb-3">{{ total }} record{{ "s" if total != 1 else "" }}</p>')
    lines.append("")
    lines.append("{% set columns = [")
    lines.append(columns_str)
    lines.append("] %}")
    lines.append("")
    lines.append("{{% call(row) data_table(columns=columns, rows={}_list, sort=sort, order=order, base_url=url_for(\"{}.list_{}\")) %}}".format(name, name, name))
    lines.append(td_cells)
    lines.append('  <td class="text-end">')
    lines.append('    <div class="inline-flex gap-1">')
    lines.append("      <a href=\"{{ url_for('" + name + ".detail_" + name + "', item_id=row.id) }}\" class=\"btn\" data-variant=\"ghost\" data-size=\"sm\">View</a>")
    lines.append("      <a href=\"{{ url_for('" + name + ".edit_" + name + "',   item_id=row.id) }}\" class=\"btn\" data-variant=\"ghost\" data-size=\"sm\">Edit</a>")
    lines.append("    </div>")
    lines.append("  </td>")
    lines.append("{% endcall %}")
    lines.append("")
    lines.append("{{ pagination(")
    lines.append("  page=page,")
    lines.append("  total_pages=total_pages,")
    lines.append('  base_url=url_for("{}.list_{}"),'.format(name, name))
    lines.append('  extra_params={{"q": q, "sort": sort, "order": order{}}}'.format(filter_tpl_var))
    lines.append(") }}")
    lines.append("")
    lines.append("{% endblock %}")
    lines.append("")

    return "\n".join(lines)


def generate_detail_template(name, fields):
    Names = name.capitalize() + "s"
    first = fields[0]["name"] if fields else "id"

    dt_rows = []
    for f in fields:
        lbl = to_label(f["name"])
        if f["type"] == "badge":
            val = ('<span class="badge" '
                   "data-variant=\"{{ 'secondary' if item." + f["name"] + " == 'Inactive' else 'outline' }}\">"
                   "{{ item." + f["name"] + " }}</span>")
        else:
            val = "{{ item." + f["name"] + " }}"
        dt_rows.append(
            "        <div>\n"
            '          <dt class="text-xs text-muted-foreground uppercase tracking-wide">{}</dt>\n'.format(lbl) +
            '          <dd class="mt-1 font-medium">{}</dd>\n'.format(val) +
            "        </div>"
        )

    lines = []
    lines.append('{% extends "layouts/app.html" %}')
    lines.append('{% from "components/page_header.html" import page_header %}')
    lines.append("")
    lines.append("{{% block title %}}{{{{ item.{} }}}} - App{{% endblock %}}".format(first))
    lines.append("{% block breadcrumb %}")
    lines.append("  <a href=\"{{ url_for('" + name + ".list_" + name + "') }}\" class=\"hover:underline text-muted-foreground\">" + Names + "</a>")
    lines.append('  <span class="mx-2 text-muted-foreground">/</span>')
    lines.append("  {{ item." + first + " }}")
    lines.append("{% endblock %}")
    lines.append("")
    lines.append("{% block content %}")
    lines.append("")
    lines.append("{{ page_header(")
    lines.append("  title=item." + first + "|string,")
    lines.append("  action='<a href=\"' ~ url_for(\"" + name + ".edit_" + name + "\", item_id=item.id) ~ '\" class=\"btn\" data-variant=\"outline\">Edit</a>'")
    lines.append(") }}")
    lines.append("")
    lines.append('<div class="grid gap-4 md:grid-cols-3">')
    lines.append('  <div class="card md:col-span-2">')
    lines.append("    <header><h2>Details</h2></header>")
    lines.append("    <section>")
    lines.append('      <dl class="grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-3">')
    lines.append("\n".join(dt_rows))
    lines.append("      </dl>")
    lines.append("    </section>")
    lines.append("  </div>")
    lines.append('  <div class="card">')
    lines.append("    <header><h2>Actions</h2></header>")
    lines.append('    <section class="flex flex-col gap-2">')
    lines.append("      <a href=\"{{ url_for('" + name + ".edit_" + name + "', item_id=item.id) }}\" class=\"btn w-full\" data-variant=\"outline\">Edit</a>")
    lines.append('      <button type="button" class="btn w-full" data-variant="destructive">Delete</button>')
    lines.append("    </section>")
    lines.append("  </div>")
    lines.append("</div>")
    lines.append("")
    lines.append("{% endblock %}")
    lines.append("")

    return "\n".join(lines)


def generate_form_template(name, fields):
    Names = name.capitalize() + "s"
    Name = name.capitalize()
    first = fields[0]["name"] if fields else "id"

    form_fields_html = "\n".join(_form_field(f) for f in fields)

    lines = []
    lines.append('{% extends "layouts/app.html" %}')
    lines.append('{% from "components/page_header.html" import page_header %}')
    lines.append("")
    lines.append("{% set is_edit = item is not none %}")
    lines.append('{% block title %}{{ "Edit" if is_edit else "New" }} ' + Name + ' - App{% endblock %}')
    lines.append("{% block breadcrumb %}")
    lines.append("  <a href=\"{{ url_for('" + name + ".list_" + name + "') }}\" class=\"hover:underline text-muted-foreground\">" + Names + "</a>")
    lines.append('  <span class="mx-2 text-muted-foreground">/</span>')
    lines.append('  {{ "Edit" if is_edit else "New ' + Name + '" }}')
    lines.append("{% endblock %}")
    lines.append("")
    lines.append("{% block content %}")
    lines.append("")
    lines.append("{{ page_header(")
    lines.append("  title=(\"Edit \" ~ item." + first + "|string) if is_edit else \"New " + Name + "\",")
    lines.append('  description="Fill in the details below."')
    lines.append(") }}")
    lines.append("")
    lines.append('<div class="max-w-2xl">')
    lines.append('  <div class="card">')
    lines.append("    <header><h2>" + Name + " Details</h2></header>")
    lines.append("    <section>")
    lines.append('      <form id="' + name + '-form" method="post" class="grid gap-5">')
    lines.append(form_fields_html)
    lines.append("      </form>")
    lines.append("    </section>")
    lines.append('    <footer class="justify-end gap-2">')
    lines.append("      <a href=\"{{ url_for('" + name + ".list_" + name + "') }}\" class=\"btn\" data-variant=\"ghost\">Cancel</a>")
    lines.append('      <button type="submit" form="' + name + '-form" class="btn">')
    lines.append('        {{ "Save changes" if is_edit else "Create ' + name + '" }}')
    lines.append("      </button>")
    lines.append("    </footer>")
    lines.append("  </div>")
    lines.append("</div>")
    lines.append("")
    lines.append("{% endblock %}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# File system helpers
# ---------------------------------------------------------------------------

def app_root():
    return os.path.dirname(current_app.root_path)


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    rel = os.path.relpath(path, app_root())
    click.echo(click.style("  [OK] Created  " + rel, fg="green"))


def insert_after_marker(filepath, marker, insertion):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    if marker not in content:
        return False
    content = content.replace(marker, marker + "\n" + insertion, 1)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True


# ---------------------------------------------------------------------------
# Main command
# ---------------------------------------------------------------------------

@scaffold_cli.command("resource")
@click.argument("name")
@click.option("--fields", default="name", show_default=True,
              help='Comma-separated field specs: "name,email:email,status:badge,amount:currency"')
@click.option("--icon", default="list", show_default=True,
              help="Lucide icon name for the sidebar (e.g. folder-kanban, briefcase, users)")
def scaffold_resource(name, fields, icon):
    """
    Generate a full CRUD resource: list + detail + form pages,
    wired into the sidebar and Flask app automatically.

    \b
    Example:
        flask --app wsgi scaffold resource project \\
              --fields "name,owner,status:badge,due:date" \\
              --icon folder-kanban
    """
    name = name.lower().strip().replace("-", "_").replace(" ", "_")
    root = app_root()
    app_dir = os.path.join(root, "app")

    click.echo("\n" + click.style("Scaffolding resource: ", bold=True) + name + "\n")

    # Parse fields
    try:
        parsed_fields = parse_fields(fields)
    except click.BadParameter as e:
        raise click.UsageError(str(e))

    # Safety check
    bp_dir = os.path.join(app_dir, "blueprints", name)
    if os.path.exists(bp_dir):
        raise click.UsageError(
            "Blueprint '{}' already exists at {}. "
            "Delete the folder and remove its registration before re-scaffolding.".format(
                name, os.path.relpath(bp_dir, root))
        )

    # 1. Blueprint files
    write_file(os.path.join(bp_dir, "__init__.py"), generate_bp_init(name))
    write_file(os.path.join(bp_dir, "routes.py"), generate_routes(name, parsed_fields))
    write_file(os.path.join(bp_dir, "fake_data.py"), generate_fake_data(name, parsed_fields))

    # 2. Block templates
    tpl_dir = os.path.join(app_dir, "templates", "blocks")
    write_file(os.path.join(tpl_dir, name + "_list.html"), generate_list_template(name, parsed_fields, icon))
    write_file(os.path.join(tpl_dir, name + "_detail.html"), generate_detail_template(name, parsed_fields))
    write_file(os.path.join(tpl_dir, name + "_form.html"), generate_form_template(name, parsed_fields))

    # 3. Wire blueprint into app/__init__.py
    init_path = os.path.join(app_dir, "__init__.py")
    import_line = "    from app.blueprints.{} import {}_bp".format(name, name)
    register_line = "    app.register_blueprint({}_bp)".format(name)
    ok1 = insert_after_marker(init_path, "    # SCAFFOLD:IMPORTS", import_line)
    ok2 = insert_after_marker(init_path, "    # SCAFFOLD:REGISTER", register_line)
    if ok1 and ok2:
        click.echo(click.style("  [OK] Registered blueprint in app/__init__.py", fg="green"))
    else:
        click.echo(click.style("  [!!] Could not auto-register blueprint - add it manually to app/__init__.py", fg="yellow"))

    # 4. Add sidebar nav item — appended as a new group after the Main group
    Names = name.capitalize() + "s"
    icon_svg = _icon_svg(icon).replace("'", "\\'")
    # The marker ~~SCAFFOLD_NAV_END~~ sits right after the closing of the Main group ]},
    # We replace it with a new group entry + the marker (so future scaffolds append too)
    nav_group = (
        '\n  {{ "type": "group", "label": "{}", "items": [\n'
        '    {{ "type": "item", "label": "{}", '
        '"url": url_for("{}.list_{}"), '
        '"icon": \'{}\', '
        '"current": ("{}" in request.endpoint) }}\n'
        '  ]}},~~SCAFFOLD_NAV_END~~'
    ).format(Names, Names, name, name, icon_svg, name)
    app_html = os.path.join(app_dir, "templates", "layouts", "app.html")
    ok3 = insert_after_marker(app_html, "~~SCAFFOLD_NAV_END~~", ""  # marker already replaced inline
    )
    # Use direct replacement instead
    with open(app_html, encoding="utf-8") as f:
        app_content = f.read()
    if "~~SCAFFOLD_NAV_END~~" in app_content:
        app_content = app_content.replace("~~SCAFFOLD_NAV_END~~", nav_group, 1)
        # The nav_group itself ends with ~~SCAFFOLD_NAV_END~~ for future scaffolds.
        # Jinja cannot have ~~ in the template, so we must keep it ONLY inside
        # a Python string marker that Jinja never sees. Since it's inside the
        # Jinja set block, strip it out after insertion and rely on future scaffolds
        # searching for the last "]}},~~SCAFFOLD_NAV_END~~" they inserted.
        # For now: the marker inside nav_group already replaced the old one,
        # so the file now has exactly one occurrence. Keep it — Jinja actually
        # errors on ~ inside set blocks. Strip any remaining marker.
        app_content = app_content.replace("~~SCAFFOLD_NAV_END~~", "")
        with open(app_html, "w", encoding="utf-8") as f:
            f.write(app_content)
        ok3 = True
    else:
        ok3 = False
    if ok3:
        click.echo(click.style("  [OK] Added sidebar nav item in layouts/app.html", fg="green"))
    else:
        click.echo(click.style("  [!!] Could not add sidebar nav item - add it manually", fg="yellow"))

    # 5. Add gallery entry — insert before the closing "] %}" of blocks_list
    Names = name.capitalize() + "s"
    new_entry = (
        ',\n'
        '  {\n'
        '    "name": "' + Names + '",\n'
        '    "description": "Scaffolded resource: list, detail, and form pages for ' + name + '.",\n'
        '    "url": url_for("' + name + '.list_' + name + '"),\n'
        '    "file": "blocks/' + name + '_list.html",\n'
        '    "extends": "layouts/app.html",\n'
        '    "vars": "' + name + '_list, q, sort, order, page, total_pages, total"\n'
        '  }'
    )
    gallery_html = os.path.join(app_dir, "templates", "gallery", "blocks.html")
    with open(gallery_html, encoding="utf-8") as f:
        gallery_content = f.read()
    # Find the closing of the blocks_list Python list inside the template.
    # The anchor is the last "  }\n] %}" pattern — last entry closing followed by list end.
    anchor = "\n] %}"
    if anchor in gallery_content:
        pos = gallery_content.rfind(anchor)
        gallery_content = gallery_content[:pos] + new_entry + gallery_content[pos:]
        with open(gallery_html, "w", encoding="utf-8") as f:
            f.write(gallery_content)
        ok4 = True
    else:
        ok4 = False
    if ok4:
        click.echo(click.style("  [OK] Added entry to gallery/blocks.html", fg="green"))
    else:
        click.echo(click.style("  [!!] Could not add gallery entry - add it manually", fg="yellow"))

    # Done
    click.echo("\n" + click.style("Done!", bold=True, fg="green") + " Visit:\n")
    click.echo("    http://localhost:5000/app/{}".format(name))
    click.echo("    http://localhost:5000/ui/blocks\n")
    click.echo(click.style(
        "  Tip: open the generated _list / _detail / _form templates\n"
        "  to customize badge colors, add columns, or connect real data.\n", dim=True))

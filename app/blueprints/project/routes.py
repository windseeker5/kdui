from flask import render_template, request, abort
from app.blueprints.project import project_bp
from app.blueprints.project.fake_data import PROJECT

PAGE_SIZE = 10


def _filter(rows, q, status=""):
    if q:
        q_l = q.lower()
        rows = [r for r in rows if any(q_l in str(v).lower() for v in r.values())]
    if status:
        rows = [r for r in rows if r["status"].lower() == status.lower()]
    return rows


@project_bp.route("/project")
def list_project():
    q     = request.args.get("q", "")
    status = request.args.get("status", "")
    sort  = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    page  = max(1, int(request.args.get("page", 1)))

    rows = _filter(PROJECT, q, status=status)
    rows = sorted(rows, key=lambda r: str(r.get(sort, "")), reverse=(order == "desc"))

    total       = len(rows)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page        = min(page, total_pages)
    rows        = rows[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]

    return render_template(
        "blocks/project_list.html",
        project_list=rows,
        q=q,
        status=status,
        sort=sort,
        order=order,
        page=page,
        total_pages=total_pages,
        total=total,
    )


@project_bp.route("/project/new")
def new_project():
    return render_template("blocks/project_form.html", item=None)


@project_bp.route("/project/<int:item_id>")
def detail_project(item_id):
    item = next((r for r in PROJECT if r["id"] == item_id), None)
    if not item:
        abort(404)
    return render_template("blocks/project_detail.html", item=item)


@project_bp.route("/project/<int:item_id>/edit")
def edit_project(item_id):
    item = next((r for r in PROJECT if r["id"] == item_id), None)
    if not item:
        abort(404)
    return render_template("blocks/project_form.html", item=item)

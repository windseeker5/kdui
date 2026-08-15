from flask import render_template, request, abort
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.dashboard.fake_data import CUSTOMERS, STATS, RECENT_ACTIVITY

PAGE_SIZE = 5


def _filter_customers(q, status):
    rows = CUSTOMERS
    if q:
        q_lower = q.lower()
        rows = [c for c in rows if q_lower in c["name"].lower() or q_lower in c["email"].lower()]
    if status:
        rows = [c for c in rows if c["status"].lower() == status.lower()]
    return rows


@dashboard_bp.route("/dashboard")
def index():
    return render_template(
        "blocks/dashboard.html",
        stats=STATS,
        recent_activity=RECENT_ACTIVITY,
        recent_customers=CUSTOMERS[:5],
    )


@dashboard_bp.route("/customers")
def customers():
    q      = request.args.get("q", "")
    status = request.args.get("status", "")
    sort   = request.args.get("sort", "name")
    order  = request.args.get("order", "asc")
    page   = max(1, int(request.args.get("page", 1)))

    rows = _filter_customers(q, status)

    # Sort
    reverse = (order == "desc")
    rows = sorted(rows, key=lambda r: r.get(sort, ""), reverse=reverse)

    # Paginate
    total      = len(rows)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page       = min(page, total_pages)
    rows       = rows[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]

    return render_template(
        "blocks/crm_list.html",
        customers=rows,
        q=q,
        status=status,
        sort=sort,
        order=order,
        page=page,
        total_pages=total_pages,
        total=total,
    )


@dashboard_bp.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    customer = next((c for c in CUSTOMERS if c["id"] == customer_id), None)
    if not customer:
        abort(404)
    return render_template("blocks/detail_page.html", customer=customer)


@dashboard_bp.route("/customers/new")
def customer_new():
    return render_template("blocks/form_page.html", customer=None)


@dashboard_bp.route("/customers/<int:customer_id>/edit")
def customer_edit(customer_id):
    customer = next((c for c in CUSTOMERS if c["id"] == customer_id), None)
    if not customer:
        abort(404)
    return render_template("blocks/form_page.html", customer=customer)


@dashboard_bp.route("/settings")
def settings():
    return render_template("blocks/settings_page.html")

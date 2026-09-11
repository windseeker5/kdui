"""Flask extension that exposes KD UI templates and compiled assets."""

import hashlib
from calendar import month_abbr
from datetime import date, datetime, timedelta

from flask import Blueprint


def _md5(value):
    """Return the stable hash used by KDUI's deterministic avatar palette."""
    return hashlib.md5(str(value).encode("utf-8"), usedforsecurity=False).hexdigest()


def _coerce_date(value):
    """Return a date from a date, datetime, or ISO date string."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def _activity_year(rows):
    """Normalize sparse activity counts into the current calendar-year grid."""
    today = date.today()
    year = today.year
    supplied = {}

    for raw in rows or []:
        if not hasattr(raw, "get"):
            continue
        day = _coerce_date(raw.get("date"))
        if day is None or day.year != year:
            continue
        activities = list(raw.get("activities") or [])
        try:
            count = max(0, int(raw.get("count", len(activities))))
        except (TypeError, ValueError):
            count = len(activities)
        supplied[day] = {
            "count": count,
            "activities": activities,
            "level": raw.get("level"),
        }

    max_count = max((item["count"] for item in supplied.values()), default=0)
    first = date(year, 1, 1)
    last = date(year, 12, 31)
    # GitHub's graph starts each week on Sunday.
    grid_start = first - timedelta(days=(first.weekday() + 1) % 7)
    week_count = ((last - grid_start).days // 7) + 1

    days = []
    by_date = {}
    active_days = []
    cursor = first
    while cursor <= last:
        item = supplied.get(cursor, {})
        count = item.get("count", 0)
        explicit_level = item.get("level")
        if explicit_level is None:
            level = 0 if count == 0 or max_count == 0 else min(4, max(1, (count * 4 + max_count - 1) // max_count))
        else:
            try:
                level = min(4, max(0, int(explicit_level)))
            except (TypeError, ValueError):
                level = 0

        normalized = {
            "date": cursor.isoformat(),
            "label": f"{cursor.strftime('%B')} {cursor.day}, {year}",
            "count": count,
            "level": level,
            "activities": item.get("activities", []),
            "future": cursor > today,
            "week": (cursor - grid_start).days // 7,
            "weekday": (cursor.weekday() + 1) % 7,
        }
        days.append(normalized)
        by_date[normalized["date"]] = normalized
        if count or normalized["activities"]:
            active_days.append(normalized)
        cursor += timedelta(days=1)

    months = []
    for month in range(1, 13):
        month_start = date(year, month, 1)
        start_week = (month_start - grid_start).days // 7
        next_start = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
        next_week = (next_start - grid_start).days // 7
        months.append({
            "label": month_abbr[month],
            "week": start_week,
            "span": max(1, next_week - start_week),
        })

    return {
        "year": year,
        "total": sum(item["count"] for item in supplied.values()),
        "days": days,
        "active_days": active_days,
        "by_date": by_date,
        "months": months,
        "week_count": week_count,
    }


class KDUI:
    """Register namespaced Jinja macros and static assets with Flask."""

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if "kdui" not in app.blueprints:
            blueprint = Blueprint(
                "kdui",
                __name__,
                template_folder="templates",
                static_folder="static",
                static_url_path="/kdui-assets",
            )
            app.register_blueprint(blueprint)
        app.jinja_env.filters.setdefault("kdui_md5", _md5)
        app.jinja_env.filters.setdefault("kdui_activity_year", _activity_year)
        app.extensions["kdui"] = self

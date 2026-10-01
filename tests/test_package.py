from flask import Flask, render_template_string

from kdui import KDUI


def test_extension_registers_namespaced_templates():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/components/badge.html" import badge %}'
            '{{ badge(label="Ready") }}'
        )

    assert "Ready" in rendered
    assert 'class="badge' in rendered


def test_minipass_components_render_with_deterministic_avatar_colors():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/components/avatar.html" import avatar_initials, avatar_group %}'
            '{% from "kdui/components/image_picker.html" import image_picker, image_picker_dialogs %}'
            '{{ avatar_initials("Samuel Gendreau") }}'
            '{{ avatar_initials("Samuel Gendreau") }}'
            '{{ avatar_group(names=["Samuel Gendreau", "Marco Henry"], max=1) }}'
            '{{ image_picker(id="cover-photo") }}'
            '{{ image_picker_dialogs(id="cover-photo") }}'
        )

    avatar_classes = [
        part.split('"', 1)[0]
        for part in rendered.split('class="kdui-avatar-initials ')[1:3]
    ]
    assert avatar_classes[0] == avatar_classes[1]
    assert "kdui-avatar-group__more" in rendered
    assert 'data-kdui-image-picker="cover-photo"' in rendered
    assert 'role="tablist"' in rendered
    assert 'data-kdui-image-mode="search"' in rendered
    assert 'data-kdui-image-mode="upload"' in rendered
    assert "PNG, JPEG, or WebP up to 5 MB." in rendered
    assert 'aria-live="polite"' in rendered
    assert 'id="cover-photo-crop"' in rendered and 'id="cover-photo-crop-confirm"' in rendered
    assert 'id="cover-photo-results-grid"' in rendered


def test_table_actions_have_icons_and_mobile_pagination_renders():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/components/action_menu.html" import action_menu %}'
            '{% from "kdui/components/pagination.html" import pagination_mobile %}'
            '{{ action_menu("actions", [{"label": "View"}, {"label": "Edit"}, {"label": "Delete"}]) }}'
            '{{ pagination_mobile(page=1, pages=5, per_page=3, total=11, items_count=3, base_path="/records") }}'
        )

    assert rendered.count('role="menuitem"') == 3
    assert rendered.count("<svg") >= 6
    assert "Page <strong>1</strong> of 5" in rendered


def test_activity_heatmap_renders_current_year_and_accessible_dates():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/components/activity_heatmap.html" import activity_heatmap %}'
            '{{ activity_heatmap(days=[{"date": "2026-09-11", "count": 4, '
            '"activities": [{"time": "09:14", "title": "Contact created", "type": "Contact"}]}], '
            'selected_date="2026-09-11", label="activities") }}'
        )

    assert "4</strong> activities in 2026" in rendered
    assert 'aria-label="4 activities on September 11, 2026"' in rendered
    assert 'data-level="4"' in rendered
    assert "Activity for September 11, 2026" in rendered
    assert "Contact created" in rendered
    assert 'data-kdui-activity-heatmap' in rendered
    assert 'data-activity-reset' in rendered
    assert 'aria-label="Close activity details"' in rendered


def test_form_pattern_owns_working_form():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/patterns/form_page.html" import form_page %}'
            '{% call form_page(title="New item", card_title="Details", action="/items", '
            'cancel_url="/", form_id="item-form") %}'
            '<input name="name">'
            '{% endcall %}'
        )

    assert '<form id="item-form"' in rendered
    assert 'action="/items"' in rendered
    assert '<button type="submit"' in rendered


def test_form_pattern_secondary_submit_posts_the_same_form_elsewhere():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/patterns/form_page.html" import form_page %}'
            '{% call form_page(title="New item", card_title="Details", action="/items", cancel_url="/", '
            'secondary_submit={"label": "Save and add a lead", "formaction": "/items?next=lead"}) %}'
            '<input name="name">'
            '{% endcall %}'
        )

    assert 'formaction="/items?next=lead"' in rendered
    assert "Save and add a lead" in rendered
    assert rendered.count("<button type=\"submit\"") == 2


def test_kanban_renders_columns_cards_dock_and_tabs():
    app = Flask(__name__)
    KDUI(app)

    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/components/kanban.html" import kanban, kanban_column, kanban_dock, kanban_card, kanban_row %}'
            '{% set menu = [{"label": "Move to Done", "icon": "<svg></svg>"}] %}'
            '{% call kanban(id="deals", move_url="/deals/{id}/move", csrf_token="tok", cols=1, dock=true,'
            ' tabs=[{"id": "new", "label": "New", "count": 1}, {"id": "done", "label": "Done", "count": 0}], active="new") %}'
            '{% call kanban_column(id="new", label="New", count=1, total="$300") %}'
            '{{ kanban_card(id=7, title="Studio Lumen", href="/x", note="Due today", tone="warning", value="$300", actions=menu) }}'
            '{% endcall %}'
            '{% call kanban_dock() %}{% call kanban_column(id="done", label="Done", count=0, empty="Nothing yet", compact=true) %}{% endcall %}{% endcall %}'
            '{% endcall %}'
        )

    assert 'data-move-url="/deals/{id}/move"' in rendered
    assert 'data-kanban-col="new"' in rendered and 'data-kanban-col="done"' in rendered
    assert 'data-kanban-card' in rendered and 'data-id="7"' in rendered
    assert 'data-tone="warning"' in rendered
    assert 'data-dock' in rendered
    assert rendered.count('data-kanban-tab=') == 2
    assert 'Nothing yet' in rendered
    assert 'aria-label="Actions for Studio Lumen"' in rendered


def test_table_row_avatar_is_optional_and_can_be_square():
    app = Flask(__name__)
    KDUI(app)
    rows = [
        {"id": 1, "primary": "No avatar", "cells": [], "actions": []},
        {"id": 2, "avatar_name": "Round", "primary": "Round", "cells": [], "actions": []},
        {"id": 3, "avatar_name": "Square", "avatar_shape": "square", "primary": "Square", "cells": [], "actions": []},
        {"id": 4, "avatar_name": "Photo", "avatar_url": "/p.png", "avatar_shape": "square", "primary": "Photo", "cells": [], "actions": []},
    ]
    with app.test_request_context():
        rendered = render_template_string(
            '{% from "kdui/components/data_table.html" import table_desktop %}'
            '{{ table_desktop(id="t", columns=[], rows=rows, first_column="Project") }}',
            rows=rows,
        )
    assert "<th>Project</th>" in rendered
    assert rendered.count("kdui-avatar-initials") == 3  # nothing for the row without avatar_name
    assert rendered.count("kdui-table-avatar--square") == 2
    assert 'src="/p.png"' in rendered

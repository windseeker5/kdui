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
            '{% from "kdui/components/image_picker.html" import image_picker %}'
            '{{ avatar_initials("Samuel Gendreau") }}'
            '{{ avatar_initials("Samuel Gendreau") }}'
            '{{ avatar_group(names=["Samuel Gendreau", "Marco Henry"], max=1) }}'
            '{{ image_picker(id="cover-photo") }}'
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

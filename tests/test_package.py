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

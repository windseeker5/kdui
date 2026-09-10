from app import create_app


def test_showroom_routes_render():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    for path in ("/", "/ui/", "/ui/components", "/ui/patterns", "/ui/maintainer"):
        response = client.get(path)
        assert response.status_code == 200, path


def test_packaged_assets_are_served():
    app = create_app()
    app.config.update(TESTING=True)
    response = app.test_client().get("/kdui-assets/kdui/css/output.css")
    assert response.status_code == 200
    assert response.mimetype == "text/css"

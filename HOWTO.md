# KD UI maintainer notes

The canonical maintainer guide is available in the showroom at
`/ui/maintainer`. Keep this file intentionally short so the workflow has one
source of truth.

```bash
pip install -r requirements.txt
npm ci
python wsgi.py --port 5005
```

Reusable files belong under `src/kdui/`, while `app/` exists only to render the
showroom. Add every public component or pattern to the gallery, rebuild CSS,
run `pytest`, and release a tagged version before upgrading consumer projects.

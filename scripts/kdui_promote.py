"""Promote one proven Jinja macro from a Flask app into KD UI.

The source application may expose files in app/templates/components or
app/templates/patterns. This helper copies only the explicitly named file into
the local KD UI package; it never commits or pushes.
"""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "component": ROOT / "src/kdui/templates/kdui/components",
    "pattern": ROOT / "src/kdui/templates/kdui/patterns",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=TARGETS)
    parser.add_argument("name")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.name.replace("_", "").isalnum() or args.name.lower() != args.name:
        raise SystemExit("Names use lowercase letters, numbers, and underscores only.")

    source_root = args.source.expanduser().resolve()
    source = source_root / "app/templates" / ("components" if args.kind == "component" else "patterns") / f"{args.name}.html"
    if not source.is_file():
        raise SystemExit(f"Source file not found: {source}")

    target = TARGETS[args.kind] / source.name
    action = "create" if not target.exists() else "update"
    if args.dry_run:
        print(f"would {action} {target.relative_to(ROOT)}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f"{action} {target.relative_to(ROOT)}")
    print("Next: remove app assumptions, namespace imports, add a gallery demo, rebuild CSS, and run pytest.")


if __name__ == "__main__":
    main()

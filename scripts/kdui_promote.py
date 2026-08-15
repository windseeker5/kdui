"""Audit and promote reusable Jinja UI files from a prototype into KD UI.

Examples, run from the KD UI repository:

    python scripts/kdui_promote.py status --source /path/to/prototype --kind component
    python scripts/kdui_promote.py component file_upload --source /path/to/prototype --dry-run
    python scripts/kdui_promote.py component file_upload --source /path/to/prototype

This tool only copies files into the local KD UI working tree. It never edits
the source project and never runs git commit or git push.
"""

import argparse
import filecmp
import re
import shutil
from pathlib import Path


KDUI_ROOT = Path(__file__).resolve().parents[1]
KINDS = {
    "component": Path("app/templates/components"),
    "block": Path("app/templates/blocks"),
}
SAFE_NAME = re.compile(r"^[a-z0-9_]+$")


def _source_root(value):
    path = Path(value).expanduser().resolve()
    if not (path / "app" / "templates").is_dir():
        raise argparse.ArgumentTypeError(f"Not a Flask/Jinja project: {path}")
    if path == KDUI_ROOT:
        raise argparse.ArgumentTypeError("The source project cannot be the KD UI repository itself.")
    return path


def _component_files(root, kind, name):
    relative_template = KINDS[kind] / f"{name}.html"
    files = [relative_template]
    if kind == "component":
        companion = Path("app/static/js/components") / f"{name}.js"
        if (root / companion).is_file():
            files.append(companion)
    return files


def _state(source, target):
    if not target.exists():
        return "missing"
    return "identical" if filecmp.cmp(source, target, shallow=False) else "different"


def _assert_safe_file(path, root, label):
    if path.is_symlink():
        raise SystemExit(f"Refusing symlinked {label}: {path}")
    resolved = path.resolve(strict=path.exists())
    if not resolved.is_relative_to(root.resolve()):
        raise SystemExit(f"Refusing {label} outside repository root: {path}")


def status(args):
    drift = False
    kinds = (args.kind,) if args.kind else KINDS
    for kind in kinds:
        relative_dir = KINDS[kind]
        source_dir = args.source / relative_dir
        target_dir = KDUI_ROOT / relative_dir
        print(f"{kind.title()}s:")
        source_names = set()
        for source_file in sorted(source_dir.glob("*.html")):
            source_names.add(source_file.name)
            relative_files = _component_files(args.source, kind, source_file.stem)
            target_file = target_dir / source_file.name
            state = _state(source_file, target_file)
            marker = {"identical": "=", "different": "~", "missing": "+"}[state]
            print(f"  {marker} {source_file.stem}: {state}")
            drift = drift or state != "identical"
            for companion in relative_files[1:]:
                companion_state = _state(args.source / companion, KDUI_ROOT / companion)
                companion_marker = {
                    "identical": "=",
                    "different": "~",
                    "missing": "+",
                }[companion_state]
                print(f"    {companion_marker} {companion}: {companion_state}")
                drift = drift or companion_state != "identical"
        for target_file in sorted(target_dir.glob("*.html")):
            if target_file.name not in source_names:
                print(f"  i {target_file.stem}: KD UI only")
        if kind == "component":
            source_js_dir = args.source / "app/static/js/components"
            target_js_dir = KDUI_ROOT / "app/static/js/components"
            source_js_names = {path.name for path in source_js_dir.glob("*.js")}
            for target_js in sorted(target_js_dir.glob("*.js")):
                if target_js.name not in source_js_names:
                    print(f"  i app/static/js/components/{target_js.name}: KD UI only")
        print()

    if drift:
        print("Review differing files before promoting them; application-specific changes may be intentional.")
    else:
        scope = f"{args.kind}s" if args.kind else "components and blocks"
        print(f"All prototype {scope} already match KD UI.")


def promote(args):
    if not SAFE_NAME.fullmatch(args.name):
        raise SystemExit("Name must contain only lowercase letters, numbers, and underscores.")

    relative_files = _component_files(args.source, args.kind, args.name)
    source_template = args.source / relative_files[0]
    if not source_template.is_file():
        raise SystemExit(f"Source {args.kind} does not exist: {source_template}")
    _assert_safe_file(source_template, args.source, "source file")

    changed = False
    for relative_file in relative_files:
        source_file = args.source / relative_file
        target_file = KDUI_ROOT / relative_file
        _assert_safe_file(source_file, args.source, "source file")
        _assert_safe_file(target_file, KDUI_ROOT, "target file")
        state = _state(source_file, target_file)
        action = "create" if state == "missing" else "update"

        if state == "identical":
            print(f"unchanged  {relative_file}")
            continue
        if args.dry_run:
            print(f"would {action}  {relative_file}")
            changed = True
            continue

        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        print(f"{action:9} {relative_file}")
        changed = True

    if not changed:
        return
    if args.dry_run:
        print("\nDry run only; no files were copied.")
        return

    print("\nPromotion copied files into the local KD UI working tree only.")
    if len(relative_files) > 1:
        print("A JavaScript controller was included; ensure KD UI's base layout loads it.")
    print("Next: add or update the KD UI gallery demo, rebuild CSS, test it, and review git diff.")
    print("Do not commit or push until the component has been verified.")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Compare prototype UI files with KD UI.")
    status_parser.add_argument("--source", required=True, type=_source_root)
    status_parser.add_argument("--kind", choices=KINDS, help="Limit the audit to components or blocks.")
    status_parser.set_defaults(handler=status)

    for kind in KINDS:
        promote_parser = subparsers.add_parser(kind, help=f"Promote one {kind} into KD UI.")
        promote_parser.add_argument("name")
        promote_parser.add_argument("--source", required=True, type=_source_root)
        promote_parser.add_argument("--dry-run", action="store_true")
        promote_parser.set_defaults(handler=promote, kind=kind)

    return parser


def main():
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()

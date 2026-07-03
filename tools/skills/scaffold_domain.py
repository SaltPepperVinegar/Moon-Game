from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DOMAIN_NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
CORE_GUID_RE = re.compile(r"^[0-9a-fA-F]{32}$")


def _read_json(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(fallback)

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return dict(fallback)

    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return data


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _domain_rules_template(domain_name: str) -> str:
    return f"""# {domain_name} Domain Rules

{domain_name} code belongs under `MoonGame/Assets/Scripts/Domains/{domain_name}/`.

- Put public contracts in `API/`.
- Put implementation details in `Internal/`.
- Put presentation and Unity-facing view code in `UI/`.
- Reference `Core` only.
- Communicate with other domains through Core event-bus events.
"""


def _asmdef_template(domain_name: str, core_guid: str) -> dict[str, Any]:
    return {
        "name": f"Domain_{domain_name}",
        "rootNamespace": f"MoonGame.Domains.{domain_name}",
        "references": [
            f"GUID:{core_guid.lower()}"
        ],
        "includePlatforms": [],
        "excludePlatforms": [],
        "allowUnsafeCode": False,
        "overrideReferences": False,
        "precompiledReferences": [],
        "autoReferenced": True,
        "defineConstraints": [],
        "versionDefines": [],
        "noEngineReferences": False,
    }


def _upsert_route(config_path: Path, domain_name: str, rules_path: Path) -> str:
    config = _read_json(config_path, fallback={"routes": []})

    routes = config.setdefault("routes", [])
    if not isinstance(routes, list):
        raise ValueError(f"Expected 'routes' to be a list in {config_path}")

    pattern = f"MoonGame/Assets/Scripts/Domains/{domain_name}/**/*"
    load = rules_path.as_posix()
    for route in routes:
        if isinstance(route, dict) and route.get("pattern") == pattern:
            route["load"] = load
            break
    else:
        routes.append({"pattern": pattern, "load": load})

    _write_json(config_path, config)
    return pattern


def scaffold_domain(
    domain_name: str,
    core_guid: str,
    repository_root: str | Path | None = None,
) -> dict[str, Any]:
    if not DOMAIN_NAME_RE.fullmatch(domain_name):
        raise ValueError("domain_name must be PascalCase and contain only letters and digits")

    if not CORE_GUID_RE.fullmatch(core_guid):
        raise ValueError("core_guid must be a 32-character Unity GUID")

    repo_root = Path(repository_root) if repository_root is not None else Path.cwd()
    repo_root = repo_root.resolve()
    unity_root = repo_root / "MoonGame"
    assets_root = unity_root / "Assets"

    if not assets_root.is_dir():
        raise FileNotFoundError(f"Expected Unity Assets folder at {assets_root}")

    domain_root = assets_root / "Scripts" / "Domains" / domain_name
    created_dirs: list[str] = []
    for child in ("API", "Internal", "UI"):
        path = domain_root / child
        if not path.exists():
            created_dirs.append(str(path.relative_to(repo_root)))
        path.mkdir(parents=True, exist_ok=True)

    asmdef_path = domain_root / f"Domain_{domain_name}.asmdef"
    asmdef_written = False
    if not asmdef_path.exists():
        _write_json(asmdef_path, _asmdef_template(domain_name, core_guid))
        asmdef_written = True

    rules_path = repo_root / "docs" / "domains" / f"{domain_name.lower()}_rules.md"
    rules_written = False
    if not rules_path.exists():
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text(_domain_rules_template(domain_name), encoding="utf-8")
        rules_written = True

    route_pattern = _upsert_route(
        repo_root / ".opencode" / "config.json",
        domain_name,
        rules_path.relative_to(repo_root),
    )

    return {
        "domain": domain_name,
        "domain_root": str(domain_root.relative_to(repo_root)),
        "created_dirs": created_dirs,
        "asmdef": str(asmdef_path.relative_to(repo_root)),
        "asmdef_written": asmdef_written,
        "rules": str(rules_path.relative_to(repo_root)),
        "rules_written": rules_written,
        "route_pattern": route_pattern,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a Moon Game gameplay domain.")
    parser.add_argument("domain_name", help="PascalCase domain name, for example Combat")
    parser.add_argument("core_guid", help="32-character Unity GUID for Core.asmdef")
    parser.add_argument(
        "--repository-root",
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    args = parser.parse_args(argv)

    try:
        result = scaffold_domain(args.domain_name, args.core_guid, args.repository_root)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

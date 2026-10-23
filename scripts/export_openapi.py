"""Exporta ou verifica o contrato OpenAPI definitivo sem depender de rede."""

import argparse
import json
import sys
from pathlib import Path

from campusflow.api import create_app
from campusflow.repository import InMemoryReservationRepository


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).resolve().parents[1] / "docs/openapi.json"
    schema = create_app(InMemoryReservationRepository()).openapi()
    if args.check:
        if not path.exists() or json.loads(path.read_text(encoding="utf-8")) != schema:
            print("OPENAPI_MISMATCH: exporte o contrato e revise o diff", file=sys.stderr)
            return 1
        print("OPENAPI_OK: snapshot corresponde ao As-Built da API")
    else:
        path.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

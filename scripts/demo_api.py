"""Demonstração HTTP reproduzível usando somente dados fictícios."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from uuid import uuid4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--reservation-id", help="Verifica preservação após reinício")
    args = parser.parse_args()

    def call(method: str, path: str, expected: int, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            args.base_url + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                code, body = response.status, json.load(response)
        except urllib.error.HTTPError as error:
            code, body = error.code, json.load(error)
        if code != expected:
            raise RuntimeError(f"{method} {path}: esperado {expected}, recebido {code}: {body}")
        print(f"{method} {path} -> HTTP {code}")
        return body

    if args.reservation_id:
        body = call("GET", f"/reservations/{args.reservation_id}", 200)
        if body["status"] != "cancelled":
            raise RuntimeError("Estado não preservado após reinício")
        print("PERSISTENCE_OK: estado preservado apos recriacao do conteiner")
        return

    call("GET", "/health", 200)
    rooms = call("GET", "/rooms", 200)
    payload = {
        "room_id": rooms[0]["id"],
        "user_id": "demo-" + uuid4().hex,
        "starts_at": "2026-10-25T10:00:00-03:00",
        "ends_at": "2026-10-25T11:00:00-03:00",
        "attendees": 1,
    }
    created = call("POST", "/reservations", 201, payload)
    reservation_id = created["id"]
    call("GET", f"/reservations/{reservation_id}", 200)
    call("POST", "/reservations", 409, {**payload, "user_id": "conflict-" + uuid4().hex})
    listed = call("GET", f"/reservations?user_id={payload['user_id']}", 200)
    if len(listed) != 1:
        raise RuntimeError("Filtro por usuário inconsistente")
    call("DELETE", f"/reservations/{reservation_id}", 200)
    call("DELETE", f"/reservations/{reservation_id}", 409)
    print(f"RESERVATION_ID={reservation_id}")
    print("DEMO_OK: criacao, consulta, conflito, filtro e cancelamento validados")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, urllib.error.URLError) as error:
        print(f"DEMO_FAILED: {error}", file=sys.stderr)
        sys.exit(1)

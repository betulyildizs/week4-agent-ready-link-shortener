import sqlite3
import uuid

import pytest
from fastapi.testclient import TestClient

import main

app = main.app

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "links.db")
    main.init_db()


def test_custom_alias_creates_link_and_redirects():
    alias = f"custom-{uuid.uuid4().hex}"

    response = client.post(
        "/shorten",
        json={"url": "https://example.com/custom", "alias": alias},
    )

    assert response.status_code == 200
    assert response.json() == {"code": alias, "short_url": f"/{alias}"}

    redirect = client.get(f"/{alias}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/custom"


def test_valid_alias_with_hyphen_and_underscore():
    alias = f"valid_alias-{uuid.uuid4().hex}"

    response = client.post(
        "/shorten",
        json={"url": "https://example.com/valid", "alias": alias},
    )

    assert response.status_code == 200
    assert response.json() == {"code": alias, "short_url": f"/{alias}"}


@pytest.mark.parametrize(
    "alias",
    ["", "bad/alias", "bad?alias", "bad#alias", "a" * 65, "docs", "redoc"],
)
def test_invalid_alias_returns_unprocessable_entity(alias):
    response = client.post(
        "/shorten",
        json={"url": "https://example.com/invalid", "alias": alias},
    )

    assert response.status_code == 422


def test_duplicate_custom_alias_returns_conflict():
    alias = f"duplicate-{uuid.uuid4().hex}"
    first = client.post(
        "/shorten",
        json={"url": "https://example.com/first", "alias": alias},
    )
    assert first.status_code == 200

    duplicate = client.post(
        "/shorten",
        json={"url": "https://example.com/second", "alias": alias},
    )

    assert duplicate.status_code == 409


def test_shorten_without_alias_generates_code():
    response = client.post("/shorten", json={"url": "https://example.com/generated"})

    assert response.status_code == 200
    result = response.json()
    assert result["code"]
    assert result["short_url"] == f"/{result['code']}"

    redirect = client.get(result["short_url"], follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/generated"


def test_generated_code_skips_code_reserved_by_custom_alias():
    with sqlite3.connect(main.DB_PATH) as conn:
        row = conn.execute(
            "SELECT seq FROM sqlite_sequence WHERE name = 'links'"
        ).fetchone()
    next_id = (row[0] if row else 0) + 1
    occupied_code = _encode(next_id + 1)

    reserved = client.post(
        "/shorten",
        json={"url": "https://example.com/reserved", "alias": occupied_code},
    )
    assert reserved.status_code == 200

    generated = client.post(
        "/shorten",
        json={"url": "https://example.com/after-collision"},
    )

    assert generated.status_code == 200
    result = generated.json()
    assert result["code"] != occupied_code
    redirect = client.get(result["short_url"], follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/after-collision"


def _encode(number: int) -> str:
    base = len(main.ALPHABET)
    chars = []
    while number:
        number, remainder = divmod(number, base)
        chars.append(main.ALPHABET[remainder])
    return "".join(reversed(chars)) or main.ALPHABET[0]

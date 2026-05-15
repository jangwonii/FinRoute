from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.services.customers import DEV_ADVISOR_ID


def test_create_customer_writes_audit_log(client: TestClient, db_session: Session) -> None:
    response = client.post(
        "/customers",
        json={
            "name": "Kim Minjun",
            "birth_year": 1988,
            "occupation": "Engineer",
            "household_type": "single",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["errors"] == []
    assert body["data"]["name"] == "Kim Minjun"
    assert body["data"]["advisor_id"] == str(DEV_ADVISOR_ID)

    audit_log = db_session.scalar(select(AuditLog).where(AuditLog.event_type == "CUSTOMER_CREATED"))
    assert audit_log is not None
    assert audit_log.after_json["name"] == "Kim Minjun"


def test_list_customers_is_paginated_for_dev_advisor(client: TestClient) -> None:
    client.post("/customers", json={"name": "First"})
    client.post("/customers", json={"name": "Second"})

    response = client.get("/customers?page=1&page_size=1")

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 1
    assert body["meta"] == {"page": 1, "page_size": 1, "total": 2}


def test_get_and_update_customer(client: TestClient) -> None:
    created = client.post("/customers", json={"name": "Original"}).json()["data"]

    update_response = client.patch(
        f"/customers/{created['customer_id']}",
        json={"name": "Updated", "memo": "Reviewed by advisor"},
    )
    get_response = client.get(f"/customers/{created['customer_id']}")

    assert update_response.status_code == 200
    assert update_response.json()["data"]["name"] == "Updated"
    assert get_response.json()["data"]["memo"] == "Reviewed by advisor"


def test_get_missing_customer_returns_404(client: TestClient) -> None:
    response = client.get("/customers/00000000-0000-0000-0000-000000000999")

    assert response.status_code == 404

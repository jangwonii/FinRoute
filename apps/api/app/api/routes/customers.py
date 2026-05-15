from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.schemas.envelope import ApiResponse, success_response
from app.schemas.pagination import pagination_meta
from app.services.customers import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])
DbSession = Annotated[Session, Depends(get_db_session)]


@router.get("", response_model=ApiResponse)
def list_customers(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
) -> ApiResponse:
    customers, total = CustomerService(db).list_customers(page=page, page_size=page_size)
    data = [CustomerRead.model_validate(customer).model_dump(mode="json") for customer in customers]
    return success_response(data, pagination_meta(page=page, page_size=page_size, total=total))


@router.post("", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    db: DbSession,
) -> ApiResponse:
    customer = CustomerService(db).create_customer(payload)
    data = CustomerRead.model_validate(customer).model_dump(mode="json")
    return success_response(data)


@router.get("/{customer_id}", response_model=ApiResponse)
def get_customer(
    customer_id: UUID,
    db: DbSession,
) -> ApiResponse:
    customer = CustomerService(db).get_customer(customer_id)
    data = CustomerRead.model_validate(customer).model_dump(mode="json")
    return success_response(data)


@router.patch("/{customer_id}", response_model=ApiResponse)
def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
    db: DbSession,
) -> ApiResponse:
    customer = CustomerService(db).update_customer(customer_id, payload)
    data = CustomerRead.model_validate(customer).model_dump(mode="json")
    return success_response(data)

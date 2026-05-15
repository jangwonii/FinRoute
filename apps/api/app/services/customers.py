from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.audit_logs import AuditLogRepository
from app.repositories.customers import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate

DEV_ADVISOR_ID = UUID("00000000-0000-0000-0000-000000000001")
DEV_ADVISOR_EMAIL = "advisor@finroute.local"
DEV_ADVISOR_NAME = "Development Advisor"


class CustomerService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.customers = CustomerRepository(db)
        self.audit_logs = AuditLogRepository(db)

    def list_customers(self, *, page: int, page_size: int) -> tuple[list[Customer], int]:
        advisor_id = self._ensure_dev_advisor()
        total = self.customers.count_for_advisor(advisor_id)
        customers = self.customers.list_for_advisor(advisor_id, page=page, page_size=page_size)
        return customers, total

    def create_customer(self, payload: CustomerCreate) -> Customer:
        advisor_id = self._ensure_dev_advisor()
        customer = self.customers.create(advisor_id, payload)
        self.audit_logs.create(
            actor_id=advisor_id,
            event_type="CUSTOMER_CREATED",
            target_type="Customer",
            target_id=customer.customer_id,
            before_json=None,
            after_json=self._customer_snapshot(customer),
        )
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_customer(self, customer_id: UUID) -> Customer:
        advisor_id = self._ensure_dev_advisor()
        customer = self.customers.get_for_advisor(customer_id, advisor_id)
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        return customer

    def update_customer(self, customer_id: UUID, payload: CustomerUpdate) -> Customer:
        customer = self.get_customer(customer_id)
        customer = self.customers.update(customer, payload)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def _ensure_dev_advisor(self) -> UUID:
        self.customers.ensure_advisor(
            DEV_ADVISOR_ID,
            email=DEV_ADVISOR_EMAIL,
            name=DEV_ADVISOR_NAME,
        )
        return DEV_ADVISOR_ID

    @staticmethod
    def _customer_snapshot(customer: Customer) -> dict[str, str | int | None]:
        return {
            "customer_id": str(customer.customer_id),
            "advisor_id": str(customer.advisor_id),
            "name": customer.name,
            "birth_year": customer.birth_year,
            "gender": customer.gender,
            "occupation": customer.occupation,
            "household_type": customer.household_type,
        }

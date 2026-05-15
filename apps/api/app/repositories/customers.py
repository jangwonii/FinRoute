from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.user import User, UserRole
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def ensure_advisor(self, advisor_id: UUID, *, email: str, name: str) -> User:
        user = self.db.get(User, advisor_id)
        if user is not None:
            return user

        user = User(
            user_id=advisor_id,
            email=email,
            name=name,
            role=UserRole.ADVISOR.value,
            password_hash="dev-only-not-for-login",
        )
        self.db.add(user)
        self.db.flush()
        return user

    def count_for_advisor(self, advisor_id: UUID) -> int:
        statement = (
            select(func.count())
            .select_from(Customer)
            .where(Customer.advisor_id == advisor_id)
        )
        return int(self.db.scalar(statement) or 0)

    def list_for_advisor(self, advisor_id: UUID, *, page: int, page_size: int) -> list[Customer]:
        statement = (
            select(Customer)
            .where(Customer.advisor_id == advisor_id)
            .order_by(Customer.created_at.desc(), Customer.customer_id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(self.db.scalars(statement).all())

    def get_for_advisor(self, customer_id: UUID, advisor_id: UUID) -> Customer | None:
        statement = select(Customer).where(
            Customer.customer_id == customer_id,
            Customer.advisor_id == advisor_id,
        )
        return self.db.scalar(statement)

    def create(self, advisor_id: UUID, payload: CustomerCreate) -> Customer:
        customer = Customer(advisor_id=advisor_id, **payload.model_dump())
        self.db.add(customer)
        self.db.flush()
        return customer

    def update(self, customer: Customer, payload: CustomerUpdate) -> Customer:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(customer, field, value)
        self.db.flush()
        return customer

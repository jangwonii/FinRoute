from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        actor_id: UUID,
        event_type: str,
        target_type: str,
        target_id: UUID,
        before_json: dict | None,
        after_json: dict | None,
    ) -> AuditLog:
        audit_log = AuditLog(
            actor_id=actor_id,
            event_type=event_type,
            target_type=target_type,
            target_id=target_id,
            before_json=before_json,
            after_json=after_json,
        )
        self.db.add(audit_log)
        self.db.flush()
        return audit_log

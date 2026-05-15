from app.db.session import Base, engine


def test_database_engine_uses_configured_postgresql_url() -> None:
    assert Base.metadata is not None
    assert engine.url.get_backend_name() == "postgresql"

from sqlmodel import create_engine, Session

from app.config.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.app_debug,
    pool_pre_ping=True,
    pool_recycle=3600,
)


def get_session():
    """FastAPI dependency: yields a database session per request using SQLModel.Session."""
    with Session(engine) as session:
        yield session

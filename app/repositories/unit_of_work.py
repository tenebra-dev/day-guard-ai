from __future__ import annotations
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


class UnitOfWork(AbstractContextManager):
    def __init__(self, session_factory: Callable[[], Session] = SessionLocal):
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.session:
                self.session.close()
                self.session = None

    def commit(self) -> None:
        if self.session:
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()

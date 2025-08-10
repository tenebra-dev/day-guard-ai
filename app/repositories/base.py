from __future__ import annotations
from typing import Generic, TypeVar, Type, Sequence, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get(self, id_: int) -> Optional[T]:
        return self.session.get(self.model, id_)

    def count(self) -> int:
        return self.session.query(self.model).count()

    def list(self, offset: int = 0, limit: int = 100) -> Sequence[T]:
        return (
            self.session.query(self.model)
            .offset(max(offset, 0))
            .limit(max(min(limit, 1000), 1))
            .all()
        )

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.flush()
        self.session.refresh(obj)
        return obj

    def delete(self, id_: int) -> None:
        instance = self.get(id_)
        if instance is None:
            return
        self.session.delete(instance)

    def update(self, id_: int, **kwargs) -> Optional[T]:
        instance = self.get(id_)
        if instance is None:
            return None
        for k, v in kwargs.items():
            setattr(instance, k, v)
        self.session.flush()
        self.session.refresh(instance)
        return instance

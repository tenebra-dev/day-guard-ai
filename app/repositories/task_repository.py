from typing import Optional, Sequence, Literal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.repositories.base import Repository
from app.db.models.task import TaskORM


SortField = Literal["id", "title", "location", "mood", "created_at", "updated_at"]
SortDir = Literal["asc", "desc"]


class TaskRepository(Repository[TaskORM]):
    def __init__(self, session: Session):
        super().__init__(session, TaskORM)

    def find_by_title(self, title: str) -> Sequence[TaskORM]:
        return self.session.query(TaskORM).filter(TaskORM.title.ilike(f"%{title}%")).all()

    def upsert(self, id_: int, **kwargs) -> TaskORM:
        instance: Optional[TaskORM] = self.get(id_)
        if instance is None:
            instance = TaskORM(id=id_, **kwargs)
            return self.create(instance)
        for k, v in kwargs.items():
            setattr(instance, k, v)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def search(
        self,
        *,
        title: Optional[str] = None,
        location: Optional[str] = None,
        mood: Optional[str] = None,
        offset: int = 0,
        limit: int = 50,
        sort_by: Optional[SortField] = None,
        sort_dir: SortDir = "asc",
    ) -> Sequence[TaskORM]:
        q = self.session.query(TaskORM)
        if title:
            q = q.filter(TaskORM.title.ilike(f"%{title}%"))
        if location:
            q = q.filter(TaskORM.location.ilike(f"%{location}%"))
        if mood:
            q = q.filter(TaskORM.mood.ilike(f"%{mood}%"))
        if sort_by:
            column = getattr(TaskORM, sort_by)
            q = q.order_by(column.asc() if sort_dir == "asc" else column.desc())
        return q.offset(max(offset, 0)).limit(max(min(limit, 1000), 1)).all()

    def count_filtered(
        self,
        *,
        title: Optional[str] = None,
        location: Optional[str] = None,
        mood: Optional[str] = None,
    ) -> int:
        q = self.session.query(func.count(TaskORM.id))
        if title:
            q = q.filter(TaskORM.title.ilike(f"%{title}%"))
        if location:
            q = q.filter(TaskORM.location.ilike(f"%{location}%"))
        if mood:
            q = q.filter(TaskORM.mood.ilike(f"%{mood}%"))
        return int(q.scalar() or 0)

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.db.session import SessionLocal
from app.repositories.task_repository import TaskRepository
from app.db.models.task import TaskORM
from app.repositories.unit_of_work import UnitOfWork

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=Dict[str, Any])
async def list_tasks(
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    title: Optional[str] = None,
    location: Optional[str] = None,
    mood: Optional[str] = None,
    sort_by: Optional[str] = Query(None, pattern="^(id|title|location|mood|created_at|updated_at)$"),
    sort_dir: str = Query("asc", pattern="^(asc|desc)$"),
):
    repo = TaskRepository(db)
    items = repo.search(
        title=title,
        location=location,
        mood=mood,
        offset=offset,
        limit=limit,
        sort_by=sort_by,  # type: ignore[arg-type]
        sort_dir=sort_dir,  # type: ignore[arg-type]
    )
    total = repo.count_filtered(title=title, location=location, mood=mood)
    return {
        "items": [TaskRead.model_validate(obj, from_attributes=True) for obj in items],
        "total": total,
        "offset": offset,
        "limit": limit,
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def create_task(task: TaskCreate):
    with UnitOfWork() as uow:
        repo = TaskRepository(uow.session)  # type: ignore[arg-type]
        obj = TaskORM(**task.model_dump())
        created = repo.create(obj)
        return TaskRead.model_validate(created, from_attributes=True)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    obj = repo.get(task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskRead.model_validate(obj, from_attributes=True)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task: TaskUpdate):
    with UnitOfWork() as uow:
        repo = TaskRepository(uow.session)  # type: ignore[arg-type]
        updated = repo.update(task_id, **{k: v for k, v in task.model_dump().items() if v is not None})
        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskRead.model_validate(updated, from_attributes=True)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    with UnitOfWork() as uow:
        repo = TaskRepository(uow.session)  # type: ignore[arg-type]
        repo.delete(task_id)
        return None

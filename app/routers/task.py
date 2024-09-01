from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated, List
from models import Task, User
from schemas import CreateTask, UpdateTask
from sqlalchemy import select, insert, update, delete

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/', response_model=List[Task])
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Task)).scalars().all()
    return result


@router.get('/{task_id}', response_model=Task)
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    new_task = Task(
        title=task.title,
        content=task.content,
        priority=task.priority,
        user_id=user_id
    )
    db.execute(insert(Task).values(new_task))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{task_id}', status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    stmt = update(Task).where(Task.id == task_id).values(
        title=task.title,
        content=task.content,
        priority=task.priority
    )
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@router.delete('/delete/{task_id}', status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(Task).where(Task.id == task_id)
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deleted successfully!'}
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from schemas import Task


# GET
def get_task(db: Session, task_id: int):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return task


# GET
def get_all_tasks(db: Session):
    return db.query(models.Tasks).all() or []


# POST
def create_task(db: Session, task: Task):
    try:
        date_obj = datetime.strptime(str(task.date), '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format! Expected format: YYYY-MM-DD.")

    try:
        db_task = models.Tasks(description=task.description, date=date_obj)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(error)}")


# PUT
def change_task(db: Session, data: Task, task_id: int):
    task = get_task(db, task_id)
    task.description = data.description
    task.date = data.date
    task.is_done = data.is_done

    db.commit()
    db.refresh(task)

    return task


# DELETE
def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    try:
        db.delete(task)
        db.commit()
        return get_all_tasks(db)
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to delete task: {str(error)}")

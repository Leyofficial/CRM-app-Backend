from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from dependencies import get_db
from schemas import Task, StatusDetails, Tasks

router = APIRouter(
    prefix="/api"
)


@router.post("/task", response_model=StatusDetails)
def create_task(data: Task, db: Session = Depends(get_db)):
    task = crud.create_task(db, data)
    if task is None:
        raise HTTPException(status_code=400, detail="Failed to create task")
    if isinstance(task, dict) and task.get("error"):
        raise HTTPException(status_code=400, detail="Date must be in 'YYYY-MM-DD' format")
    return {'status': 200, 'detail': 'Success!'}


@router.get("/tasks", response_model=Tasks)
def get_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    return {'status': 200, 'detail': 'Success!', 'tasks': tasks}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from dependencies import get_db
from schemas import Task, StatusDetails, Tasks

router = APIRouter(
    prefix="/api",
    tags=["tasks"]
)


@router.post("/task", response_model=StatusDetails)
def create_task(data: Task, db: Session = Depends(get_db)):
    crud.create_task(db, data)
    return {'status': 200, 'detail': 'Success!'}


@router.get("/task/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, id)
    return {'status': 200, 'detail': 'Success!', 'task': task}


@router.get("/tasks", response_model=Tasks)
def get_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    return {'status': 200, 'detail': 'Success!', 'tasks': tasks}

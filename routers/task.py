from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from dependencies import get_db
from schemas import Task, StatusDetails, Tasks, TaskDetails

router = APIRouter(
    prefix="/api",
    tags=["tasks"]
)


@router.post("/task", response_model=StatusDetails)
def create_task(data: Task, db: Session = Depends(get_db)):
    crud.create_task(db, data)
    return {'status': 200, 'detail': 'Success!'}


@router.put("/task/{id}", response_model=TaskDetails)
def change_task(id: int, data: Task, db: Session = Depends(get_db)):
    updated_task = crud.change_task(db, data, id)
    return {'status': 200, 'detail': 'Task updated successfully', 'task': updated_task}


@router.get("/task/{id}", response_model=TaskDetails)
def get_task(id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, id)
    return {'status': 200, 'detail': 'Success!', 'task': task}


@router.get("/tasks", response_model=Tasks)
def get_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    return {'status': 200, 'detail': 'Success!', 'tasks': tasks}

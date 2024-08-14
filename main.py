from fastapi import FastAPI

import models
from database import engine
from routers.customer import router as customer_router
from routers.task import router as task_router
from routers.deal import router as deal_router

app = FastAPI()
app.include_router(customer_router)
app.include_router(task_router)
app.include_router(deal_router)
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

from fastapi import FastAPI

import models
from database import engine
from routers.customer import router as customer_router

app = FastAPI()
app.include_router(customer_router)
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

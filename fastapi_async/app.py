from fastapi import FastAPI
import uvicorn

import settings
from resources import database
import blog.views


app = FastAPI(debug=settings.DEBUG)
app.include_router(blog.views.router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

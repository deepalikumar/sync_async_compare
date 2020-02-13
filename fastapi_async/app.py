from fastapi import FastAPI
import uvicorn

import settings
from resources import database
import blog.views


async def on_startup():
    await database.connect()


async def on_shutdown():
    await database.disconnect()


app = FastAPI(debug=settings.DEBUG)
app.include_router(blog.views.router, prefix="/fastapi/api/v1")
app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

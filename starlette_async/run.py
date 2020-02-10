import uvicorn
from app import create_app

starlette_app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:starlette_app", reload=True)

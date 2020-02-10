import uvicorn
from app import create_app

fastapi_app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:fastapi_app", reload=True)

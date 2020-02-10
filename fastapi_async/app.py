from fastapi import FastAPI
import sqlalchemy
import databases


app = None
database = None
metadata = sqlalchemy.MetaData()


def create_app():
    global app
    app = FastAPI()

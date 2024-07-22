from http.client import HTTPException

from fastapi import FastAPI
from routers.database import router as database_router

app = FastAPI(title="Database API", openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc", version="0.1.0",
              description="Этот микросервис служит для связи с базой данных XP Academy",
              contact={"name": "Raev Andrei",
                       "url": "https://github.com/Andrei-Raev/dataBaseServer",
                       "email": "andrey-raev.raev@yandex.ru"})

app.include_router(database_router)


@app.exception_handler(HTTPException)
def _404_error_handler(request, exc):
    return {"message": exc.detail}, exc.status_code

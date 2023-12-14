import uvicorn
from fastapi import FastAPI
from routers import routers
from settings import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router)

if __name__ == "__main__":
    reload = settings.env == "DEV"
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=reload)

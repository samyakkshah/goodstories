from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.stories import story_router
import uvicorn
from config.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"msg": "Good Stories backend is running"}


app.include_router(story_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)

import uvicorn
from databaseDriver import DatabaseDriver
from stateManager import StateManager
from fastapi import FastAPI


app = FastAPI()

@app.get("/api/v2/{user_uuid}")
async def read_item(user_uuid: str):
    db = DatabaseDriver("cases.db")
    manager = StateManager().setDriver(db)
    return {
        "hasCovid": manager.currentlyHasCovid(user_uuid),
        "dateReported": db.dateReported(user_uuid),
    }


@app.post("/api/v2/{user_uuid}")
async def post_user(user_uuid, hasCovid: bool):
    db = DatabaseDriver("cases.db")
    db.flagWithCovid(user_uuid, hasCovid)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info")

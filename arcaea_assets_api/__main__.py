from route import app
from scheduler_job import scheduler


@app.on_event("startup")
async def _():
    scheduler.start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=17777,
    )

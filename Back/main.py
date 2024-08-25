import uvicorn

if __name__ == "__main__":
    config = uvicorn.run("app.api:app", host="localhost", port=9090, log_level="info")
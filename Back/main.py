import uvicorn

if __name__ == "__main__":
    config = uvicorn.run("app.endpoints.router:app", host="192.168.1.40", port=9090, log_level="info")
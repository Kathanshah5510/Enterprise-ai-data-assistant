from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Data Assistant",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Data Assistant API is running!"
    }
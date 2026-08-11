import os


def main() -> None:
    host = os.getenv("HLX_HOST", "127.0.0.1")
    port = int(os.getenv("HLX_PORT", "8000"))
    import uvicorn
    uvicorn.run("hlx_engine.api:app", host=host, port=port, reload=False)

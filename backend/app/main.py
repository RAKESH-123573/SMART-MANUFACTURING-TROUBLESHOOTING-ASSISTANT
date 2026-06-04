from fastapi import Request, UploadFile, File, WebSocket
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import os
import tempfile
from .rag import ingest_pdf, retrieve
from .agents import SupervisorAgent
from . import app

router = APIRouter()


@router.post('/ingest')
async def ingest(file: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    contents = await file.read()
    tmp.write(contents)
    tmp.flush()
    tmp.close()
    ingest_pdf(tmp.name)
    os.unlink(tmp.name)
    return JSONResponse({"status": "ingested"})


@router.post('/query')
async def query(payload: dict):
    """Accepts: {"query": str, "sensor_data": {...}}"""
    q = payload.get('query')
    sensor_data = payload.get('sensor_data', {})
    # retrieve RAG context
    docs = retrieve(q, k=4)
    supervisor = SupervisorAgent()
    report = supervisor.run(q, sensor_data, docs)
    return JSONResponse(report)


@router.websocket('/ws/chat')
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    supervisor = SupervisorAgent()
    try:
        while True:
            data = await ws.receive_json()
            q = data.get('query')
            sensor = data.get('sensor_data', {})
            docs = retrieve(q, k=4)
            # run agents and stream back partial updates
            for update in supervisor.run_streaming(q, sensor, docs):
                await ws.send_json(update)
    except Exception:
        await ws.close()


app.include_router(router, prefix="/api")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

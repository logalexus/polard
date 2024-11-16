import asyncio
import json

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from Crypto.Util.number import getPrime
from pydantic import BaseModel
from backend.crypto.factorizer import Factorizer
from backend.crypto.generators.rsa_gen import generate_pub_key
from backend.crypto.methods.factor import pollard_rho, yafu_factor_driver
from backend.crypto.tests.tester import PublicKeyTester

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="backend/templates")


@app.get("/api/pollard_test")
async def get(request: Request):
    return templates.TemplateResponse("pollard_test.html", {"request": request})


@app.get("/api/public_generate")
async def get_pub_key(bits: int):
    if bits < 20 or bits > 4096:
        raise HTTPException(
            status_code=400, detail="Key size must be between 20 and 4096 bits")
    return generate_pub_key(bits)


class FactorizeModel(BaseModel):
    public_key: str
    method: str
    timeout: int

@app.post("/api/factorize")
async def factorize(params: FactorizeModel):
    if params.timeout < 1 or params.timeout > 300:
        raise HTTPException(
            status_code=400, detail="Timeout size must be between 1 and 300 seconds")
        
    factorizer = Factorizer(params.method)
    factorResult = await factorizer.factorize(params.public_key.encode(), params.timeout)
    
    return factorResult

class CheckKeyModel(BaseModel):
    public_key: str
    timeout: int

@app.post("/api/check")
async def factorize(params: CheckKeyModel):
    if params.timeout < 1 or params.timeout > 30:
        raise HTTPException(
            status_code=400, detail="Timeout size must be between 1 and 30 seconds")
        
    tester = PublicKeyTester()
    results = await tester.run_tests(params.public_key.encode(), params.timeout)
    
    return results


class AnalyzeResult(BaseModel):
    id: int
    bits: int
    time: str
    status: str

@app.websocket("/api/analyze")
async def analyze(websocket: WebSocket, method: str, timeout: int):
    await websocket.accept()
    try:
        for i, bits in enumerate(range(22, 257)):
            public_key = generate_pub_key(bits)
            factorizer = Factorizer(method)
            factorResult = await factorizer.factorize(public_key.encode(), timeout)
            analyzeResult = AnalyzeResult(
                id=i,
                bits=bits,
                time=factorResult.factor_time,
                status=factorResult.status
            )
            await websocket.send_text(analyzeResult.model_dump_json())
            if factorResult.status == "Timeout":
                await websocket.close()
                return
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

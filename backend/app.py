import asyncio

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from Crypto.Util.number import getPrime
from pydantic import BaseModel
from backend.crypto.factorizer import Factorizer
from backend.crypto.generators.rsa_gen import generate_pub_key
from backend.crypto.methods.factor import pollard_rho, yafu_factor_driver

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

class FactorResult(BaseModel):
    status: str
    private_key: str
    factor_time: str

@app.post("/api/factorize")
async def factorize(params: FactorizeModel):
    if params.timeout < 1 or params.timeout > 300:
        raise HTTPException(
            status_code=400, detail="Timeout size must be between 1 and 300 seconds")
        
    factorizer = Factorizer(params.public_key.encode())
    private_key, time = factorizer.factorize(params.method)
    
    return FactorResult(status="Success", private_key=private_key, factor_time=time)


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        for i in range(10, 129):
            p = getPrime(i)
            q = getPrime(i)
            n = p * q
            phi = (p - 1) * (q - 1)
            e = 0x10001
            d = pow(e, -1, phi)

            result = f"Bits = {i}\nN = {n}\n"
            await websocket.send_text(result)

            factor = await asyncio.to_thread(yafu_factor_driver, n)
            p = factor
            q = n // p

            factor_result = f"Factor: p = {p}, q = {q}\n"
            await websocket.send_text(factor_result)

    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

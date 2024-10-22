import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi import Request
from Crypto.Util.number import getPrime
from backend.crypto.methods.factor import pollard_rho, yafu_factor_driver

app = FastAPI()

templates = Jinja2Templates(directory="backend/templates")


@app.get("/pollard_test")
async def get(request: Request):
    return templates.TemplateResponse("pollard_test.html", {"request": request})


@app.websocket("/ws")
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
    uvicorn.run(app, host="127.0.0.1", port=8000)

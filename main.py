from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permitir acceso desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RetiroRequest(BaseModel):
    wallet: str
    amount: float

@app.post("/api/retirar")
async def retirar(request: Request, retiro: RetiroRequest):
    api_key = request.headers.get("x-api-key")
    if api_key != "secret_token_123":
        raise HTTPException(status_code=401, detail="API Key inválida")

    if retiro.amount < 0.000075:
        raise HTTPException(status_code=400, detail="Monto mínimo no alcanzado")

    comision = round(retiro.amount * 0.05, 8)
    neto = round(retiro.amount - comision, 8)

    # Simular respuesta
    return {
        "success": True,
        "usuario": {
            "wallet": retiro.wallet,
            "monto_enviado": neto
        },
        "comision": {
            "monto_enviado": comision
        }
    }

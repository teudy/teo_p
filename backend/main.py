import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from kucoin.client import User
import uvicorn

app = FastAPI()

API_TOKEN = os.getenv("API_TOKEN", "secret_token_123")
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

if not all([KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE]):
    raise Exception("Falta configurar las claves KuCoin en variables de entorno")

kucoin_client = User(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE, is_sandbox=False)

def verificar_token(x_api_key: str = Header(...)):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="No autorizado")

class RetiroData(BaseModel):
    currency: str
    amount: float
    address: str
    memo: str = None

@app.get("/saldo/{currency}")
async def saldo(currency: str, x_api_key: str = Header(...)):
    verificar_token(x_api_key)
    currency = currency.upper()
    try:
        balances = kucoin_client.get_accounts()
        for b in balances:
            if b['currency'].upper() == currency:
                return {"currency": currency, "balance": float(b['available'])}
        return {"currency": currency, "balance": 0.0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retiro")
async def retiro(data: RetiroData, x_api_key: str = Header(...)):
    verificar_token(x_api_key)
    currency = data.currency.upper()
    try:
        balances = kucoin_client.get_accounts()
        available = 0.0
        for b in balances:
            if b['currency'].upper() == currency:
                available = float(b['available'])
                break

        if data.amount > available:
            raise HTTPException(status_code=400, detail=f"Saldo insuficiente. Disponible: {available}")

        result = kucoin_client.create_withdraw(
            currency=currency,
            amount=str(data.amount),
            address=data.address,
            memo=data.memo or ""
        )
        return {"success": True, "withdrawId": result.get('withdrawalId')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

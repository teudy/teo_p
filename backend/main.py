from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/api/retirar")
async def retirar(request: Request):
    datos = await request.json()
    # lógica para procesar el retiro...
    return {
        "success": True,
        "usuario": {
            "wallet": datos["wallet"],
            "monto_enviado": datos["amount"]
        },
        "comision": {
            "monto_enviado": round(datos["amount"] * 0.05, 8)
        }
    }

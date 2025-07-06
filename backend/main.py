
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.correo import enviar_correo
import json, time, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

RETIROS_FILE = "data/retiros.json"

class Retiro(BaseModel):
    wallet: str
    monto: float
    metodo: str  # "qik" o "usdt"
    cuenta: str

@app.post("/solicitar-retiro")
def solicitar_retiro(data: Retiro):
    comision = round(data.monto * 0.05, 8)
    neto = round(data.monto - comision, 8)
    retiro = {
        "wallet": data.wallet,
        "monto": data.monto,
        "metodo": data.metodo,
        "cuenta": data.cuenta,
        "comision": comision,
        "neto": neto,
        "fecha": int(time.time())
    }

    # Guardar en historial
    os.makedirs("data", exist_ok=True)
    historial = []
    if os.path.exists(RETIROS_FILE):
        with open(RETIROS_FILE) as f:
            historial = json.load(f)
    historial.append(retiro)
    with open(RETIROS_FILE, "w") as f:
        json.dump(historial, f, indent=2)

    # Enviar correo con datos del retiro
    enviar_correo(retiro)

    return { "success": True, "message": "Retiro solicitado correctamente. Se procesará manualmente." }

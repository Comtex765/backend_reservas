from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.routes import usuarios, laboratorios, login, reservas, historial, reportes

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def route():
    return {"success": "True"}


app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(laboratorios.router, prefix="/laboratorios", tags=["laboratorios"])
app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(reservas.router, prefix="/reservas", tags=["reservas"])
app.include_router(historial.router, prefix="/historial", tags=["historial"])
app.include_router(reportes.router, prefix="/reportes", tags=["reportes"])

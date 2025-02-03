from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.v1.conta.controller import router as conta_router
from api.v1.usuarios.controller import router as usuario_router
from api.v1.politicas.controller import router as politicas_router

app = FastAPI()

app.include_router(conta_router)
app.include_router(usuario_router)
app.include_router(politicas_router)

origins = ["*"]

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.get("/")
def read_root():
    return {"message": "Welcome"}
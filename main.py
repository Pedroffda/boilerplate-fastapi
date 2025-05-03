from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.routes import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")

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
from fastapi import FastAPI , Request , status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
import logging
import uuid

from app.routers.auth_router import router as auth_router
from app.routers.file_router import router as file_router

app = FastAPI(title="Cloud File Storage API", version="1.0")
app.include_router(auth_router)
app.include_router(file_router)



logger = logging.getLogger("uvicorn.error")

@app.exception_handler(OperationalError)
async def database_exception_handler(request: Request, exc: OperationalError):
    # Generate a unique ID for this specific error instance
    request_id = f"req-{uuid.uuid4().hex[:5]}" 
    
    # Log the full traceback for your own debugging
    logger.error(f"ID: {request_id} | Database Error: {exc}")

    # Return your specific custom JSON format to the user
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service Temporarily Unavailable",
            "message": "We are experiencing technical difficulties. Please try again later.",
            "request_id": request_id
        }
    )
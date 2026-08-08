"""
Δημιουργία ασύγχρονης εφαρμογής backend E-learning platform.
"""

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.database import create_tables
from app.api.routes import auth , courses , lessons,enrollments,progress, quizzes
from app.api.deps import get_current_active_user
import logging
import time



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(" Starting application...")
    await create_tables()
    yield
    logger.info(" Shutting down application...")


app = FastAPI(
    title="E-Learning Platform API",
    description="Online courses platform with authentication",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    auto_error=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f" {request.method} {request.url.path} from {client_ip}")
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f" {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
    return response

app.include_router(
    auth.router, 
    prefix="/api/auth", 
    tags=["Authentication"]
)

app.include_router(
    courses.router, 
    prefix="/api/courses", 
    tags=["Courses"],
    dependencies=[Depends(get_current_active_user)] 
)

app.include_router(
    lessons.router,
    prefix="/api", 
    tags=["Lessons"]
)

app.include_router(
    enrollments.router,
    prefix="/api",
    tags=["Enrollments"]
)

app.include_router(
    progress.router,
    prefix="/api",
    tags=["Progress"]
)

app.include_router(
    quizzes.router,
    prefix="/api",
    tags=["Quizzes"]
)


@app.get("/")
async def root(request: Request):
    return {
        "message": "Welcome to E-Learning Platform API",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "client_ip": request.client.host if request.client else "unknown",
        "docs": "/api/docs",
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
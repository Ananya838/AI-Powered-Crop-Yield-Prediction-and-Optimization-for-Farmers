from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, data_sources, farms, pest, prediction, recommendation
from app.api.routes.realtime import router as realtime_router
from app.core.background_tasks import orchestrator
from app.core.database import Base, engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    _.state.orchestrator = orchestrator
    Base.metadata.create_all(bind=engine)
    await orchestrator.startup()
    yield
    await orchestrator.shutdown()


app = FastAPI(title="AI-Powered Crop Yield Prediction and Optimization API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(prediction.router, prefix="/api/v1")
app.include_router(recommendation.router, prefix="/api/v1")
app.include_router(pest.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(farms.router, prefix="/api/v1")
app.include_router(data_sources.router, prefix="/api/v1")
app.include_router(realtime_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "crop-ai-backend"}

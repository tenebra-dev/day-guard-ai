from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import settings
from .core.logging import configure_logging
from .api.v1.router import api_router
from .workers.scheduler import Scheduler


scheduler = Scheduler()


def create_app() -> FastAPI:
    configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Scheduler
        scheduler.start()
        scheduler.add_daily_summary()
        try:
            yield
        finally:
            scheduler.shutdown()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    @app.get("/health")
    def health_check():
        return {"status": "ok", "env": settings.env}

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.statements import router as statements_router
from app.api.routes.merchant_mappings import router as merchant_mappings_router
from app.db.base import Base
from app.db.session import engine

from app.models.merchant_mapping import MerchantMapping

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title= "CardLens API",
    description = "Backend API for credit card spend analysis",
    version = "0.1.0",
)

app.include_router(health_router)
app.include_router(statements_router)
app.include_router(merchant_mappings_router)

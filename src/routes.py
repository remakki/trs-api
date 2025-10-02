from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from scalar_fastapi import get_scalar_api_reference

from src.schemas import HealthCheck
from src.storylines.rabbit_routes import rabbit_router as storyline_rabbit_router
from src.digests.rabbit_routes import rabbit_router as digests_rabbit_router

router = APIRouter(tags=["Monitoring"])


@router.get(
    "/healthcheck",
    summary="Health Check",
    description="""
        Checks whether the API service is operational and responding
    """,
    responses={
        200: {
            "description": "Service is running",
        },
    },
)
async def healthcheck() -> HealthCheck:
    return HealthCheck()


@router.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url="/api/v1/openapi.json",
        title="Erudit API",
    )


@router.get("/docs/scalar", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


def routes_register(app: FastAPI) -> None:
    app.include_router(router=router)
    app.include_router(router=storyline_rabbit_router)
    app.include_router(router=digests_rabbit_router)

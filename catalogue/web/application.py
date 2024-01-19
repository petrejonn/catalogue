from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from catalogue.logging import configure_logging
from catalogue.web.api.router import api_router
from catalogue.web.gql.router import gql_router
from catalogue.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="catalogue",
        version=metadata.version("catalogue"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Graphql router
    app.include_router(router=gql_router, prefix="/graphql")

    return app

import ast
from typing import Dict, Type

from pydantic import BaseModel, create_model
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from catalogue.settings import settings


async def create_database() -> None:
    """Create a database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'",  # noqa: E501, S608
            ),
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{settings.db_base}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            ),
        )


async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{settings.db_base}"'))


def create_pydantic_model(schema: Dict[str, str]) -> Type[BaseModel]:
    """
    Creates a Pydantic model dynamically based on the input schema.

    Args:
        schema (str): A string representing field names and their types.

    Returns:
        type: The dynamically created Pydantic model.
    """
    try:
        if not isinstance(schema, dict):
            raise ValueError(
                "Invalid schema format. Expected a dictionary-like string.",
            )
        # Create a list of field tuples (field_name, field_type, ...)
        fields = []
        for field_name, field_type in schema.items():
            required = not field_type.startswith("*")  # Check if field is required
            if not required:
                # Remove the asterisk if present
                field_type = field_type.lstrip("*")
            fields.append(
                (
                    field_name,
                    (
                        (ast.literal_eval(field_type), ...)
                        if required
                        else (ast.literal_eval(field_type))
                    ),
                ),
            )

        # Create the Pydantic model dynamically
        return create_model("DynamicModel", **dict(fields))
    except Exception as exc:
        raise ValueError(f"Error creating Pydantic model: {str(exc)}")

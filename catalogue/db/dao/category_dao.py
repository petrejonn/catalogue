from typing import Any, Dict, List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from catalogue.db.dependencies import get_db_session
from catalogue.db.models.category_model import AttributeOptionModel, CategoryModel


class CategoryDAO:
    """Class for accessing category table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, **kwargs: Dict[str, Any]) -> CategoryModel:
        """Create a new category."""
        category = CategoryModel(**kwargs)  # type: ignore
        if kwargs.get("parent_id") is not None:
            # Execute the query and fetch the parent category
            parent_result = await self.session.execute(
                select(CategoryModel).filter_by(id=kwargs["parent_id"]),
            )
            parent_category = parent_result.scalars().first()
            parent_result.close()  # Close the result explicitly

            if not parent_category:
                raise HTTPException(status_code=404, detail="Parent category not found")

            # Set the parent and combine allowed attributes
            category.parent = parent_category
            category.allowed_attributes = (
                parent_category.allowed_attributes | category.allowed_attributes
            )

        # Add the new category to the session and commit
        self.session.add(category)
        await self.session.commit()
        return category

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[CategoryModel]:
        """Get all categories."""
        res = await self.session.execute(
            select(CategoryModel).limit(limit).offset(offset),
        )
        return list(res.scalars().fetchall())

    async def get(self, category_id: int) -> CategoryModel:
        """Get a category by id."""
        res = await self.session.execute(
            select(CategoryModel).filter_by(id=category_id),
        )
        category = res.scalars().first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def delete(self, category_id: int) -> None:
        """Delete a category by id."""
        query = await self.session.execute(
            select(CategoryModel).filter_by(id=category_id),
        )
        category = query.scalars().first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.session.delete(category)


class AttributeOptionDAO:
    """Class for accessing attribute option table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, category_id: int, attribute_name: str, value: str) -> None:
        """Create a new attribute option."""
        option = AttributeOptionModel(
            category_id=category_id,
            attribute_name=attribute_name,
            value=value,
        )
        self.session.add(option)

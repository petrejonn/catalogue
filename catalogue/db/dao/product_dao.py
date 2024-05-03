from typing import Any, Dict, List

from fastapi import Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from catalogue.db.dependencies import get_db_session
from catalogue.db.models.category_model import CategoryModel
from catalogue.db.models.product_model import ProductModel
from catalogue.db.utils import create_pydantic_model


class ProductDAO:
    """Class for accessing product table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, **kwargs: Dict[str, Any]) -> ProductModel:
        """Create a new product."""
        # get the category allowed attributes
        category_result = await self.session.execute(
            select(CategoryModel).filter_by(id=kwargs["category_id"]),
        )
        category = category_result.scalars().first()
        category_result.close()  # Close the result explicitly

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # validate the attributes
        product_attributes: Dict[str, Any] = kwargs.get("product_attributes", {})
        try:
            category_attribute_model = create_pydantic_model(
                category.allowed_attributes,
            )
            category_attribute_model(**product_attributes)
        except ValidationError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        # create the product
        product = ProductModel(**kwargs)  # type: ignore
        product.category = category
        self.session.add(product)
        try:
            await self.session.commit()
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to create product")

        return product

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[ProductModel]:
        """Get all products."""
        # get all products with related categories
        res = await self.session.execute(
            select(ProductModel).limit(limit).offset(offset),
        )
        return list(res.scalars().all())

    async def get(self, product_id: int) -> ProductModel:
        """Get a product by id."""
        res = await self.session.execute(
            select(ProductModel).filter_by(id=product_id),
        )
        product = res.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def get_by_category(
        self,
        category_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> List[ProductModel]:
        """Get products by category id."""
        res = await self.session.execute(
            select(ProductModel)
            .filter_by(category_id=category_id)
            .limit(limit)
            .offset(offset),
        )
        return list(res.scalars().all())

    async def delete(self, product_id: int) -> None:
        """Delete a product by id."""
        query = await self.session.execute(
            select(ProductModel).filter_by(id=product_id),
        )
        product = query.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await self.session.delete(product)

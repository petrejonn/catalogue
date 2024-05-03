from typing import List

import strawberry
from strawberry.types import Info

from catalogue.db.dao.product_dao import ProductDAO
from catalogue.web.gql.context import Context
from catalogue.web.gql.product.schema import Product


@strawberry.type
class Query:
    """Query to interact with product."""

    @strawberry.field(description="Get all products")
    async def get_products(
        self,
        info: Info[Context, None],
        limit: int = 10,
        offset: int = 0,
    ) -> List[Product]:
        """
        Retrieves all products from the database.

        Args:
            info (Info[Context, None]): The GraphQL resolver info.
            limit (int, optional): The maximum number of products to retrieve. Defaults to 10.
            offset (int, optional): The number of products to skip. Defaults to 0.

        Returns:
            List[Product]: A list of Product objects representing the retrieved products.
        """
        dao = ProductDAO(info.context.db_connection)
        instances = await dao.get_all(limit, offset)
        return [Product.from_instance(instance) for instance in instances]

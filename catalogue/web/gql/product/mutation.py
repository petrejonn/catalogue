import strawberry
from strawberry.types import Info

from catalogue.db.dao.product_dao import ProductDAO
from catalogue.web.gql.context import Context
from catalogue.web.gql.product.schema import Product, ProductInput


@strawberry.type
class Mutation:
    """Mutations for product."""

    @strawberry.mutation(description="Add a new product")
    async def add_product(
        self,
        info: Info[Context, None],
        product: ProductInput,
    ) -> Product:
        """
        Add a new product.

        Args:
            self: The object itself.
            info (Info[Context, None]): Information about the context.
            product (ProductInput): The product input data.

        Returns:
            Product: The newly added product.
        """
        dao = ProductDAO(info.context.db_connection)
        instance = await dao.create(**strawberry.asdict(product))  # type: ignore
        return Product.from_instance(instance)

    @strawberry.mutation(description="Delete a product")
    async def delete_product(
        self,
        info: Info[Context, None],
        product_id: int,
    ) -> None:
        """
        Delete a product.

        Args:
            self: The object itself.
            info (Info[Context, None]): Information about the context.
            id (int): The ID of the product to delete.

        Returns:
            None
        """
        dao = ProductDAO(info.context.db_connection)
        await dao.delete(product_id)

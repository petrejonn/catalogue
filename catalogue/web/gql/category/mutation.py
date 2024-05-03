import strawberry
from strawberry.types import Info

from catalogue.db.dao.category_dao import CategoryDAO
from catalogue.web.gql.category.schema import Category, CategoryInput
from catalogue.web.gql.context import Context


@strawberry.type
class Mutation:
    """Mutations for category."""

    @strawberry.mutation(description="Add a new category")
    async def add_category(
        self,
        info: Info[Context, None],
        category: CategoryInput,
    ) -> Category:
        """
        Add a new category.

        Args:
            self: The object itself.
            info (Info[Context, None]): Information about the context.
            category (CategoryInput): The category input data.

        Returns:
            Category: The newly added category.
        """
        dao = CategoryDAO(info.context.db_connection)
        instance = await dao.create(**strawberry.asdict(category))  # type: ignore
        return Category.from_instance(instance)

    @strawberry.mutation(description="Delete a category")
    async def delete_category(
        self,
        info: Info[Context, None],
        category_id: int,
    ) -> None:
        """
        A description of the entire function, its parameters, and its return types.
        """
        dao = CategoryDAO(info.context.db_connection)
        await dao.delete(category_id)

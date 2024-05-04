from typing import List

import strawberry
from strawberry.types import Info

from catalogue.db.dao.category_dao import CategoryDAO
from catalogue.web.gql.category.schema import Category
from catalogue.web.gql.context import Context


@strawberry.type
class Query:
    """Query to interact with category."""

    @strawberry.field(description="Get all categories")
    async def categories(
        self,
        info: Info[Context, None],
        limit: int = 10,
        offset: int = 0,
    ) -> List[Category]:
        """
        Retrieves all categories from the database.

        Args:
            info (Info[Context, None]): The GraphQL info object.
            limit (int, optional): The maximum number of categories to retrieve. Defaults to 10.
            offset (int, optional): The number of categories to skip. Defaults to 0.

        Returns:
            List[Category]: A list of Category objects representing the retrieved categories.
        """
        dao = CategoryDAO(info.context.db_connection)
        instances = await dao.get_all(limit, offset)
        return [Category.from_instance(instance) for instance in instances]

    @strawberry.field(description="Get a category by id")
    async def category(
        self,
        info: Info[Context, None],
        category_id: int,
    ) -> Category:
        """
        Get a category by id.

        :param info: The GraphQL info object.
        :type info: Info[Context, None]
        :param category_id: The id of the category to retrieve.
        :type category_id: int
        :return: A Category object representing the retrieved category.
        :rtype: Category
        """
        dao = CategoryDAO(info.context.db_connection)
        instance = await dao.get(category_id)
        return Category.from_instance(instance)

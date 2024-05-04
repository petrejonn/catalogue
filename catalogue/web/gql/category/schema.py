from dataclasses import field
from typing import List, Optional

import strawberry
from strawberry.scalars import JSON
from strawberry.types import Info

from catalogue.db.dao.category_dao import CategoryDAO
from catalogue.db.dao.product_dao import ProductDAO
from catalogue.db.models.category_model import CategoryModel
from catalogue.web.gql.context import Context
from catalogue.web.gql.product.schema import Product


@strawberry.type
class Category:
    """Category type."""

    id: int
    parent_id: Optional[int]
    name: str
    allowed_attributes: JSON
    seo_title: str
    seo_description: str
    seo_keywords: str
    description: str
    category_img_url: str
    requires_shipping: bool
    is_deleted: bool
    instance: strawberry.Private[CategoryModel]

    @strawberry.field
    async def products(
        self,
        info: Info[Context, None],
        limit: int = 10,
        offset: int = 0,
    ) -> List[Product]:
        """
        Retrieves a list of products associated with the current category.

        Args:
            info (Info[Context, None]): The GraphQL resolver info.
            limit (int, optional): The maximum number of products to retrieve. Defaults to 10.
            offset (int, optional): The number of products to skip. Defaults to 0.

        Returns:
            List[Product]: A list of Product objects representing the retrieved products.
        """
        dao = ProductDAO(info.context.db_connection)
        products = await dao.get_by_category(self.id, limit, offset)
        return [Product.from_instance(product) for product in products]

    @strawberry.field
    async def subcategories(
        self,
        info: Info[Context, None],
        limit: int = 10,
        offset: int = 0,
    ) -> List["Category"]:
        """
        Retrieves a list of subcategories associated with the current category.

        Args:
            info (Info[Context, None]): The GraphQL resolver info.
            limit (int, optional): The maximum number of subcategories to retrieve. Defaults to 10.
            offset (int, optional): The number of subcategories to skip. Defaults to 0.

        Returns:
            List[Category]: A list of Category objects representing the retrieved subcategories.
        """
        dao = CategoryDAO(info.context.db_connection)
        categories = await dao.get_children(self.id, limit, offset)
        return [Category.from_instance(category) for category in categories]

    @classmethod
    def from_instance(cls, instance: CategoryModel) -> "Category":
        """
        Creates a new instance of the Category class from a given CategoryModel instance.

        :param instance: The CategoryModel instance to create a new Category instance from.
        :type instance: CategoryModel
        :return: The newly created Category instance.
        :rtype: Category
        """
        return cls(
            id=int(instance.id),
            parent_id=(
                int(instance.parent_id) if instance.parent_id is not None else None
            ),
            name=str(instance.name),
            allowed_attributes=dict(instance.allowed_attributes),
            seo_title=str(instance.seo_title),
            seo_description=str(instance.seo_description),
            seo_keywords=str(instance.seo_keywords),
            description=str(instance.description),
            category_img_url=str(instance.category_img_url),
            requires_shipping=bool(instance.requires_shipping),
            is_deleted=bool(instance.is_deleted),
            instance=instance,
        )


@strawberry.input
class CategoryInput:
    """Category input type."""

    name: str
    parent_id: Optional[int] = None
    allowed_attributes: Optional[JSON] = field(default_factory=dict)
    seo_title: Optional[str] = ""
    seo_description: Optional[str] = ""
    seo_keywords: Optional[str] = ""
    description: str
    category_img_url: Optional[str] = ""
    requires_shipping: Optional[bool] = True


@strawberry.type
class CategoryAttributes:
    """Category attribute type."""

    attributes: JSON

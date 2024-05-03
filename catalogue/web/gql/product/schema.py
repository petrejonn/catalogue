from typing import Optional

import strawberry
from strawberry.scalars import JSON

from catalogue.db.models.product_model import ProductModel


@strawberry.type
class Product:
    """Product type."""

    id: int
    name: str
    product_attributes: JSON
    seo_title: str
    seo_description: str
    seo_keywords: str
    description: str
    product_img_url: str
    category_id: int

    instance: strawberry.Private[ProductModel]

    @classmethod
    def from_instance(cls, instance: ProductModel) -> "Product":
        """
        Creates a new instance of the Product class from a given ProductModel instance.

        :param instance: The ProductModel instance to create a new Product instance.
        :type instance: ProductModel
        :return: The newly created Product instance.
        :rtype: Product
        """
        return cls(
            id=int(instance.id),
            name=str(instance.name),
            product_attributes=dict(instance.product_attributes),
            seo_title=str(instance.seo_title),
            seo_description=str(instance.seo_description),
            seo_keywords=str(instance.seo_keywords),
            description=str(instance.description),
            product_img_url=str(instance.product_img_url),
            category_id=int(instance.category_id),
            instance=instance,
        )


@strawberry.input
class ProductInput:
    """Product input type."""

    name: str
    category_id: int
    product_attributes: JSON
    seo_title: Optional[str] = ""
    seo_description: Optional[str] = ""
    seo_keywords: Optional[str] = ""
    description: str
    product_img_url: Optional[str] = ""

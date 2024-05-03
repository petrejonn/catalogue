from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_keyed_dict

from catalogue.db.base import Base

if TYPE_CHECKING:
    from catalogue.db.models.product_model import ProductModel


class CategoryModel(MappedAsDataclass, Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    allowed_attributes: Mapped[dict[str, str]] = mapped_column(
        type_=JSONB,
        nullable=False,
    )
    seo_title: Mapped[str] = mapped_column(String(255), nullable=False)
    seo_description: Mapped[str] = mapped_column(String(255), nullable=False)
    seo_keywords: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_img_url: Mapped[str] = mapped_column(String(255), nullable=False)
    requires_shipping: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        init=False,
    )
    parent: Mapped[Optional["CategoryModel"]] = relationship(
        "CategoryModel",
        remote_side=[id],
        back_populates="children",
        default=None,
    )
    children: Mapped[Dict[str, "CategoryModel"]] = relationship(
        "CategoryModel",
        cascade="all, delete-orphan",
        back_populates="parent",
        collection_class=attribute_keyed_dict("slug"),
        init=False,
        repr=False,
    )
    attribute_options: Mapped[List["AttributeOptionModel"]] = relationship(
        "AttributeOptionModel",
        cascade="all, delete-orphan",
        back_populates="category",
        init=False,
        repr=False,
    )
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        cascade="all, delete-orphan",
        back_populates="category",
        init=False,
        repr=False,
    )


class AttributeOptionModel(MappedAsDataclass, Base):
    __tablename__ = "attribute_options"
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        primary_key=True,
    )
    attribute_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    value: Mapped[str] = mapped_column(String(50), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        init=False,
    )
    category: Mapped[CategoryModel] = relationship(
        "CategoryModel",
        back_populates="attribute_options",
        init=False,
    )

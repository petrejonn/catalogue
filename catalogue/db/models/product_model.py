from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from catalogue.db.base import Base
from catalogue.db.models.category_model import CategoryModel


class ProductModel(MappedAsDataclass, Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    product_attributes: Mapped[Dict[str, Any]] = mapped_column(
        type_=JSONB,
        nullable=False,
    )
    seo_title: Mapped[str] = mapped_column(String(255), nullable=False)
    seo_description: Mapped[str] = mapped_column(String(255), nullable=False)
    seo_keywords: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    product_img_url: Mapped[str] = mapped_column(String(255), nullable=False)
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
    category: Mapped[Optional["CategoryModel"]] = relationship(
        "CategoryModel",
        remote_side=[CategoryModel.id],
        back_populates="products",
        default=None,
    )

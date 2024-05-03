# Catalogue Documentation

---

## Project structure

```bash
$ tree "catalogue"
catalogue
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

```bash
type AttributeOption {
  categoryId: ID!
  value: ID
  attrName: ID
  createdAt: String
  updatedAt: String
  category: Category
}

type Category {
  id: ID!
  slug: String!
  name: String!
  allowedAttributes: String!
  seoTitle: String!
  seoDescription: String!
  # list of keywords
  seoKeywords: String!
  description: String
  level: Int!
  parentId: Int
  categoryImgUrl: String
  requiresShipping: Boolean!
  createdAt: String!
  updatedAt: String!
  category: Category
  attributeOptionList: [AttributeOption!]!
  categoryList: [Category!]!
  productList: [Product!]!
}

type Product {
  id: ID!
  slug: String!
  name: String!
  seoTitle: String!
  seoDescription: String!
  # list of keywords
  seoKeywords: String!
  description: String
  categoryId: Int!
  defaultVariantId: String
  rating: String
  createdAt: String!
  updatedAt: String!
  category: Category
  productVariationList: [ProductVariation!]!
}

type ProductVariation {
  id: ID!
  slug: String
  name: String!
  attributes: String!
  productId: Int!
  price: String
  imageUrl: String
  quantity: String
  product: Product
}
```

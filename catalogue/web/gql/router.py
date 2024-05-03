import strawberry
from strawberry.fastapi import GraphQLRouter

from catalogue.web.gql import category, product
from catalogue.web.gql.context import Context, get_context


@strawberry.type
class Query(category.Query, product.Query):  # noqa: WPS215
    """Main query."""


@strawberry.type
class Mutation(category.Mutation, product.Mutation):  # noqa: WPS215
    """Main mutation."""


schema = strawberry.Schema(
    Query,
    Mutation,
)

gql_router: GraphQLRouter[Context, None] = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_context,
)

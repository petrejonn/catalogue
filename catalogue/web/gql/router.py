import strawberry
from strawberry.fastapi import GraphQLRouter

from catalogue.web.gql.context import Context, get_context


@strawberry.type
class Query:  # noqa: WPS215
    """Main query."""


@strawberry.type
class Mutation:  # noqa: WPS215
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

import graphene

from crm.schema import Mutation as CRMMutation, Query as CRMQuery


class Query(CRMQuery, graphene.ObjectType):
    hello = graphene.String(required=True)

    def resolve_hello(root, info):
        """Return a greeting for the hello field."""
        return "Hello, GraphQL!"


class Mutation(CRMMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

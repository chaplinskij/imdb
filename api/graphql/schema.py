import graphene
from apps.imdb.views.graphql import *

class Query(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
import graphene
from apps.imdb.views.graphql import *

class Query(IMDBQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
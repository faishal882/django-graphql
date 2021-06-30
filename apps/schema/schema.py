from graphene_django import DjangoObjectType
import graphene
# new
import graphql_jwt
from graphql_jwt.decorators import login_required

from apps.users.models import User
from apps.decks.models import Deck
from apps.cards.models import Card

from apps.decks.schema import (DeckType, CreateDeck)
from apps.cards.schema import ( CardType, CreateCard, UpdateCard )


class UserType(DjangoObjectType):
    class Meta:
        model = User


# Mutation Class
class Mutation(graphene.ObjectType):
    create_card = CreateCard.Field()
    create_deck = CreateDeck.Field()
    update_card = UpdateCard.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    # delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()
    # delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()


# Query class
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    decks = graphene.List(DeckType)
    deck_by_id = graphene.List(DeckType, id=graphene.Int())
    cards = graphene.List(CardType)
    deck_cards = graphene.List(CardType, deck=graphene.Int())

    def resolve_users(self, info):
        # return User.objects.all()
        # new
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        return User.objects.all()

    @login_required
    def resolve_decks(self, info):
        return Deck.objects.all()

    def resolve_cards(self, info):
        return Card.objects.all()

    # Filtering for req. data
    def resolve_deck_cards(self, info, deck):
        return Card.objects.filter(deck=deck)

    def resolve_decks_by_id(self, info, id):
      return Deck.objects.get(pk=id)


schema = graphene.Schema(query=Query, mutation=Mutation)

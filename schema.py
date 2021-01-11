from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models import User as UserModel, ToDoList as ToDoListModel
from mutation import Mutations

import graphene

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

        
class ToDoList(SQLAlchemyObjectType):
    class Meta:
        model = ToDoListModel


class Query(graphene.ObjectType):
    node = relay.Node.Field()
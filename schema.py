from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models import User as UserModel, ToDoList as ToDoListModel
from mutation import Mutations

import graphene

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
        

class UserCon(relay.Connection):
    class Meta:
        node = User

        
class ToDoList(SQLAlchemyObjectType):
    class Meta:
        model = ToDoListModel
        interface = (relay.Node, )
        

class ToDoListCon(relay.Connection):
    class Meta:
        node = ToDoList


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserCon)
    all_to_do_lists = SQLAlchemyConnectionField(ToDoListCon)
    
schema = graphene.Schema(query = Query, mutation = Mutations)
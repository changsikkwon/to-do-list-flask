import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models import User as UserModel, Tag as TagModel, ToDoList as ToDoListModel

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
        

class UserCon(relay.Connection):
    class Meta:
        node = User

        
class Tag(SQLAlchemyObjectType):
    class Meta:
        model = TagModel
        interface = (relay.Node, )
        

class TagCon(relay.Connection):
    class Meta:
        node = Tag
        
        
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
    all_tags = SQLAlchemyConnectionField(TagCon)
    all_to_do_lists = SQLAlchemyConnectionField(ToDoListCon )
    
schema = graphene.Schema(query = Query)
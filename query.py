from graphene_sqlalchemy import SQLAlchemyObjectType
from flask import g

from models import User as UserModel, ToDoList as ToDoListModel
from utils import login_required

import graphene

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

        
class ToDoList(SQLAlchemyObjectType):
    class Meta:
        model = ToDoListModel


class Query(graphene.ObjectType):
    to_do_list = graphene.List(ToDoList)
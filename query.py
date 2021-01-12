from graphene_sqlalchemy import SQLAlchemyObjectType
from flask import g

from models import User as UserModel, ToDoList as ToDoListModel
from utils import login_required, master_required

import graphene

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

        
class ToDoList(SQLAlchemyObjectType):
    class Meta:
        model = ToDoListModel


class Query(graphene.ObjectType):
    to_do_list_by_user = graphene.List(ToDoList)
    to_do_list_by_master = graphene.List(ToDoList, user_id=graphene.Int(required=True))
    user_list_by_master = graphene.List(User, offset=graphene.Int(required=True))
    
    # 유저가 자신의 to do list를 확인하는 qeury
    @login_required
    def resolve_to_do_list_by_user(self, info):
        user_id = g.user_id['user_id']
        to_do_query = ToDoList.get_query(info).filter(ToDoListModel.user_id.contains(user_id))
        
        return to_do_query
    
    # 관리자가 특정 유저의 to do list를 확인하는 qeury
    @master_required
    def resolve_to_do_list_by_master(self, info, user_id):
        to_do_query = ToDoList.get_query(info).filter(ToDoListModel.user_id.contains(user_id))
        
        return to_do_query
    
    # 관리자가 유저 list를 확인하는 query
    @master_required
    def resolve_user_list_by_master(self, info, offset):
        user_query = User.get_query(info).filter(UserModel.is_master==0).limit(10).offset(offset)
        
        return user_query
        
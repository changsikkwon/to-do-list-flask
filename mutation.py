from graphql import GraphQLError
from sqlalchemy import func
from flask import g

from models import User, ToDoList, Session
from config import SECRET_KEY, ALGORITHM
from utils import login_required

import schema
import graphene
import bcrypt
import jwt

# 유저 정보 저장 Mutation
class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        account = graphene.String(required=True)
        password = graphene.String(required=True)
        is_master = graphene.Boolean(default_value=False)
                 
    user = graphene.Field(lambda: schema.User)
    
    def mutate(self, info, name, account, password, is_master):
        user = User(
            name = name,
            account = account,
            password = password,
            is_master = is_master
        )
        
        # account 중복 확인 중복시 에러메세지
        if Session.query(User).filter_by(account=user.account).first():
            raise GraphQLError('Alredy Exist Account')
        
        user.password = bcrypt.hashpw(user.password.encode('utf-8'),
                                    bcrypt.gensalt()).decode('utf-8')
        
        Session.add(user)
        Session.commit()
        
        return CreateUser(user=user)
    

# 유저 정보 인증 Mutation
class AuthUser(graphene.Mutation):
    class Arguments:
        account = graphene.String(required=True)
        password = graphene.String(required=True)
        
    access_token = graphene.Field(graphene.String)
    
    def mutate(self, info, account, password):
        user = Session.query(User).filter_by(account=account).first()
        
        try:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
                return AuthUser(access_token=access_token)
            raise GraphQLError('Invalid_Password')
        
        except AttributeError:
            raise GraphQLError('Invalid_Account')
    

# 유저 정보 수정 Mutation
class UpdateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        account = graphene.String()
        password = graphene.String()
        is_master = graphene.Boolean()
        
    update_user = graphene.Field(lambda: schema.User)
    
    @login_required    
    def mutate(self, info, **kwargs):
        user_id = g.user_id['user_id']
        user = Session.query(User).filter_by(id=user_id).first()
        
        # password 수정시 새로운 비밀번호 암호화
        if 'password' in kwargs:
            kwargs['password'] = bcrypt.hashpw(kwargs['password'].encode('utf-8'),
                                        bcrypt.gensalt()).decode('utf-8')
        # account 수정시 중복 확인 중복시 에러메세지
        if 'account' in kwargs:
            if Session.query(User).filter_by(account=kwargs['account']).first():
                raise GraphQLError('Alredy Exist Account')
        
        kwargs['updated_at'] = func.now()
        
        for key, value in kwargs.items():
            setattr(user, key, value)
        
        Session.commit()
        
        return UpdateUser(user)
    

# 할 일 정보 저장 Mutation     
class CreateToDoList(graphene.Mutation):
    class Arguments:
        tag = graphene.String(default_value='ToDo')
        content = graphene.String(required=True)
        target_date = graphene.Date()
        
    to_do = graphene.Field(lambda: schema.ToDoList)

    @login_required
    def mutate(self, info, **kwargs):
        user_id = g.user_id['user_id']
        
        to_do = ToDoList(
            user_id = user_id,
            tag = kwargs.get('tag'),
            content = kwargs.get('content'),
            target_date = kwargs.get('target_date')
        )
        
        Session.add(to_do)
        Session.commit()
        
        return CreateToDoList(to_do=to_do)
    

# 할 일 정보 수정 Mutation
class UpdateToDoList(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        tag = graphene.String()
        content = graphene.String()
        target_date = graphene.Date()
        is_completed = graphene.Boolean()
        
    update_to_do = graphene.Field(lambda: schema.ToDoList)
    
    @login_required
    def mutate(self, info, **kwargs):
        user_id = g.user_id['user_id']
        to_do = Session.query(ToDoList).filter_by(id=kwargs['id'], user_id=user_id).first()
        
        # 일치하는 데이터 없을시 에러메세지
        if not to_do:
            raise GraphQLError('Data does not exist')
        # 완료된 일 수정시 에러메세지
        if to_do.is_completed == 1 and kwargs['is_completed'] != 0:
            raise GraphQLError('It cannot be modified')
        # 완료 처리시 완료일 기록
        if to_do.is_completed == 0 and kwargs['is_completed'] == 1:
            to_do.complete_date = func.now()
        # 완료 취소 처리 시 완료일 초기화
        if to_do.is_completed == 1 and kwargs['is_completed'] == 0:
            to_do.complete_date = None
        
        
        kwargs['updated_at'] = func.now()
        
        for key, value in kwargs.items():
            setattr(to_do, key, value)
        
        Session.commit()
        
        return UpdateToDoList(to_do)


# 할 일 정보 삭제 Mutation
class DeleteToDoList(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        
    delete_to_do = graphene.Field(graphene.String)
    
    @login_required
    def mutate(self, info, id):
        user_id = g.user_id['user_id']
        to_do = Session.query(ToDoList).filter_by(id=id, user_id=user_id).first()
        
        # 일치하는 데이터 없을시 에러메세지
        if not to_do:
            raise GraphQLError('Data does not exist')
        
        Session.delete(to_do)
        Session.commit()
        
        return DeleteToDoList()    
        
class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    auth_user = AuthUser.Field()
    create_to_do_list = CreateToDoList.Field()
    update_to_do_list = UpdateToDoList.Field()
    delete_to_do_list = DeleteToDoList.Field()
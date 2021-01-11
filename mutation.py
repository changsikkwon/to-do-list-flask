from graphql import GraphQLError
from sqlalchemy import func
from flask import g

from models import User, Session
from config import SECRET_KEY, ALGORITHM
from utils import login_required

import schema
import graphene
import bcrypt
import jwt

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        account = graphene.String(required=True)
        password = graphene.String(required=True)
        is_master = graphene.Boolean(default_value=False)
                 
    user = graphene.Field(lambda: schema.User)
    
    def mutate(self, info, name, account, password, is_master):
        data = User(
            name = name,
            account = account,
            password = password,
            is_master = is_master
        )
        
        if Session.query(User).filter_by(account=data.account).first():
            raise GraphQLError('Alredy Exist Account')
        
        data.password = bcrypt.hashpw(data.password.encode('utf-8'),
                                    bcrypt.gensalt()).decode('utf-8')
        
        Session.add(data)
        Session.commit()
        
        return CreateUser(user = data)
    

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
        
        if 'password' in kwargs:
            kwargs['password'] = bcrypt.hashpw(kwargs['password'].encode('utf-8'),
                                        bcrypt.gensalt()).decode('utf-8')
        if 'account' in kwargs:
            if Session.query(User).filter_by(account=kwargs['account']).first():
                raise GraphQLError('Alredy Exist Account')
        
        kwargs['updated_at'] = func.now()
        
        for key, value in kwargs.items():
            setattr(user, key, value)
        
        Session.commit()
        
        return UpdateUser(user)
    
        
class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    auth_user = AuthUser.Field()
from graphql import GraphQLError
from sqlalchemy import func

from models import User, Session

import schema
import graphene
import bcrypt

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        account = graphene.String(required = True)
        password = graphene.String(required = True)
        is_master = graphene.Boolean(default_value = False)
                 
    user = graphene.Field(lambda: schema.User)
    
    def mutate(self, info, name, account, password, is_master):
        data = User(
            name = name,
            account = account,
            password = password,
            is_master = is_master
        )
        
        if Session.query(User).filter_by(account = data.account).first():
            raise GraphQLError('Alredy Exist Account')
        
        data.password = bcrypt.hashpw(data.password.encode('utf-8'),
                                    bcrypt.gensalt()).decode('utf-8')
        
        Session.add(data)
        Session.commit()
        
        return CreateUser(user = data)
    

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        account = graphene.String()
        password = graphene.String()
        is_master = graphene.Boolean()
        
    update_user = graphene.Field(lambda: schema.User)
    
    def mutate(self, info, **kwargs):
        user = Session.query(User).filter_by(id = kwargs.get('id')).first()
        
        if 'password' in kwargs:
            kwargs['password'] = bcrypt.hashpw(kwargs['password'].encode('utf-8'),
                                        bcrypt.gensalt()).decode('utf-8')
        if 'account' in kwargs:
            if Session.query(User).filter_by(account = kwargs['account']).first():
                raise GraphQLError('Alredy Exist Account')
        
        kwargs['updated_at'] = func.now()
        
        for key, value in kwargs.items():
            setattr(user, key, value)
        
        Session.commit()
        
        return UpdateUser(user)
        
        
class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
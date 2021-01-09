from graphql import GraphQLError

from models import User, Session

import graphene
import bcrypt

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        account = graphene.String(required = True)
        password = graphene.String(required = True)
        is_master = graphene.Boolean(default_value = False)
         
    user = graphene.Field(graphene.String)
    
    def mutate(self, info, name, account, password, is_master):
        user = User(
            name = name,
            account = account,
            password = password,
            is_master = is_master
        )
        
        if Session.query(User).filter_by(account = user.account).first():
            raise GraphQLError('Alredy Exist Account')
        
        user.password = bcrypt.hashpw(user.password.encode('utf-8'),
                                    bcrypt.gensalt()).decode('utf-8')
        
        Session.add(user)
        Session.commit()
        
        return CreateUser(
            user = user
        )
        

class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
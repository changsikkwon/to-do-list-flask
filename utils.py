from flask import request, g
from graphql import GraphQLError
from functools import wraps

from config import SECRET_KEY, ALGORITHM
from models import Session, User

import jwt

def login_required(func):      
    @wraps(func)                   
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:  
            try:
                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            except jwt.InvalidTokenError:
                 payload = None

            if payload is None:
                raise GraphQLError('Invalid_Token')

            user_id = payload
            g.user_id = user_id
            
        else:
            raise GraphQLError('Invalid_Token')

        return func(*args, **kwargs)
    return decorated_function

def master_required(func):      
    @wraps(func)                   
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:  
            try:
                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            except jwt.InvalidTokenError:
                 payload = None

            if payload is None:
                raise GraphQLError('Invalid_Token')
            
            user_id = payload
            master = Session.query(User).filter_by(id=user_id['user_id']).first()
            
            if master.is_master == 1:
                g.master_id = user_id
                
            else:
                raise GraphQLError('Not_Master_Token')
            
        else:
            raise GraphQLError('Invalid_Token')

        return func(*args, **kwargs)
    return decorated_function
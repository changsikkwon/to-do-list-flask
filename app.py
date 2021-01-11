from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from models import Session
from schema import Query
from mutation import Mutations

import graphene

def create_app():
    app = Flask(__name__)

    app.add_url_rule(
        '/graphql',
        view_func = GraphQLView.as_view(
            'graphql',
            schema = graphene.Schema(query = Query, mutation = Mutations),
            graphiql = True,
            get_context = lambda : { 'session' : Session }))
    
    CORS(app, resources = {r'*' : {'origins': '*'}})
    
    return app
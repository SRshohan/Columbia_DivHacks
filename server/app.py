from flask import Flask
from flask_restful import Resource, Api
from chat_endpoint import Chatbot

# Set up Flask application
app = Flask(__name__)
api = Api(app)

api.add_resource(Chatbot, '/')

if __name__ == '__main__':
    app.run(debug=True)
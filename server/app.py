from flask import Flask
from flask_restful import Api
from chat_endpoint import Chatbot  # Adjust this import based on your file structure

app = Flask(__name__)
api = Api(app)

# Register the Chatbot resource with the API
api.add_resource(Chatbot, '/')

if __name__ == '__main__':
    app.run(debug=True)

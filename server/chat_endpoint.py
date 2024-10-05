from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse


class Chatbot(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_input', type=str, required=True, help="Name cannot be blank!")
        args = parser.parse_args()

        return {'message': f'{args["user_input"]}!'}
        # data = request.get_json()
        # user_input = data.get("user_input", "")
        
        # memory = {}  # Initialize a memory dictionary to store user context
        # # response = generate_response(user_input, memory)
        
        # return jsonify({"response": "response"})

    


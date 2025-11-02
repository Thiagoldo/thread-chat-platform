from flask_restx import Namespace, Resource
from . import mongo
from bson.objectid import ObjectId

chat_bp = Namespace('chats', path='/', description='Chat related operations')

@chat_bp.route('/')
class ChatList(Resource):
    def get(self):
        """List all chats."""
        # Logic to get all chats for the current user
        # Example: chats = mongo.db.chats.find({"participants": current_user_id})
        return {"message": "List all chats"}, 200

    def post(self):
        """Create a new chat."""
        # Logic to create a new chat room
        # Example: mongo.db.chats.insert_one({'name': 'New Chat', 'participants': []})
        return {"message": "Create a new chat"}, 201

@chat_bp.route('/<string:chat_id>/messages')
class Messages(Resource):
    def get(self, chat_id):
        """Get messages for a specific chat."""
        # Logic to get messages for a specific chat
        # Example: messages = mongo.db.messages.find({'chat_id': chat_id})
        return {"message": f"Get messages for chat {chat_id}"}, 200

    def post(self, chat_id):
        """Post a new message to a chat."""
        # Logic to post a new message to a chat
        # This would also likely publish to RabbitMQ for the websocket-service
        # Example: mongo.db.messages.insert_one({'chat_id': chat_id, 'text': 'Hello'})
        return {"message": f"Post message to chat {chat_id}"}, 201

@chat_bp.route('/<string:chat_id>/participants')
class Participants(Resource):
    def get(self, chat_id):
        """Get participants of a specific chat."""
        # Logic to get participants of a specific chat
        # Example: chat = mongo.db.chats.find_one({'_id': ObjectId(chat_id)})
        return {"message": f"Get participants for chat {chat_id}"}, 200

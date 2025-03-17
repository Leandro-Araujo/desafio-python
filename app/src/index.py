from flask import Flask, jsonify, request

from repositories.user_repository import UserRepository
from exceptions.custom_exception import DataBaseException, UserRepositoryException

app = Flask(__name__)

@app.errorhandler(DataBaseException)
def handle_database_exception(e):
    return jsonify({"error": str(e)}), 500


@app.errorhandler(UserRepositoryException)
def handle_user_repository_exception(e):
    return jsonify({"error": str(e)}), 400


@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e)
    }
    if hasattr(e, 'code'):
        return jsonify(response), e.code
    return jsonify(response), 500

@app.route('/users-batch', methods=['POST'])
def post_user_batch():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        user_repository = UserRepository()
        user_repository.save_users_batch(file)

        return jsonify({"message": "File received"}), 200
    except Exception as e:
        return handle_exception(e)

# Controller GET
@app.route('/users', methods=['GET'])
def get_user():
    try:
        user_repository = UserRepository()
        users = user_repository.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return handle_exception(e)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user_repository = UserRepository()
        users = user_repository.get_user_by_id(user_id)
        return jsonify(users), 200
    except Exception as e:
        return handle_exception(e)

@app.route('/users/<int:user_id>/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(user_id, order_id):
    try:
        user_repository = UserRepository()
        order = user_repository.get_order_by_id(user_id, order_id)
        if order:
            return jsonify(order), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return handle_exception(e)

if __name__ == '__main__':
    app.run(debug=True)


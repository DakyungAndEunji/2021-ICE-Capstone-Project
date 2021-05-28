from flask import jsonify

def ok(item, message):
    response_object = {
        "status": "success",
        "message": message,
    }
    if item:
        response_object["result"] = item
    return jsonify(response_object), 200

def created():
    response_object = {
        "status": "success",
        "message": "Successfully created."
    }
    return jsonify(response_object), 201

def bad_request(message):
    response_object = {
        "status": "Bad request",
        "message": message
    }
    return jsonify(response_object), 400

def not_found(message):
    response_object = {
        "status": "Not Found",
        "message": message
    }
    return jsonify(response_object), 404

def conflict(message):
    response_object = {
        "status": "Conflict",
        "message": message
    }
    return jsonify(response_object), 409
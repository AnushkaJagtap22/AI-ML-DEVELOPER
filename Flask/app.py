from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Temporary database
users = [
    {
        "id": 1,
        "name": "Anushka",
        "email": "anushka@gmail.com"
    },
    {
        "id": 2,
        "name": "Rahul",
        "email": "rahul@gmail.com"
    }
]


# ---------------------------------------
# FRONTEND PAGE
# ---------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------
# GET ALL USERS
# ---------------------------------------

@app.route("/api/users", methods=["GET"])
def get_users():

    return jsonify(users)


# ---------------------------------------
# GET SINGLE USER
# ---------------------------------------

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    for user in users:

        if user["id"] == user_id:
            return jsonify(user)

    return jsonify({
        "error": "User not found"
    }), 404


# ---------------------------------------
# CREATE USER
# ---------------------------------------

@app.route("/api/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    if not data.get("name") or not data.get("email"):
        return jsonify({
            "error": "Name and email are required"
        }), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)

    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201


# ---------------------------------------
# UPDATE USER
# ---------------------------------------

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    for user in users:

        if user["id"] == user_id:

            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])

            return jsonify({
                "message": "User updated successfully",
                "user": user
            })

    return jsonify({
        "error": "User not found"
    }), 404


# ---------------------------------------
# DELETE USER
# ---------------------------------------

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    for user in users:

        if user["id"] == user_id:

            users.remove(user)

            return jsonify({
                "message": "User deleted successfully"
            })

    return jsonify({
        "error": "User not found"
    }), 404


# ---------------------------------------
# RUN SERVER
# ---------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
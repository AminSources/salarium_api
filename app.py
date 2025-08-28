from flask import Flask, request, jsonify
import requests

# * Create the flask app
app = Flask(__name__)

# * api url
apiUrl = "https://retoolapi.dev/7gdAXu/salarium-account-data-api/"


# ? settings route
@app.route("/settings", methods=["GET"])
def settings():
    setting = (request.args.get("setting"),)
    email = (request.args.get("email"),)
    apiData = requests.get(apiUrl).json()

    # * get api all items
    if setting[0] == "getAll":
        return jsonify(apiData), 200

    # * get api item by email
    if setting[0] == "getByEmail":
        user = next((u for u in apiData if u.get("email") == email[0]), None)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found"}), 404

    # * get app version
    if setting[0] == "ver":
        return jsonify({"api_ver": "1.0.0", "app_ver": "1.0.0"}), 200


# ? login route
@app.route("/login", methods=["POST"])
def login():
    # * get email and password from request args (query parameters)
    email = (request.args.get("email"),)
    password = request.args.get("password")

    # * api data list
    apiData = requests.get(apiUrl).json()

    try:
        # * check if user exists
        if (u for u in apiData if u.get("email") == email[0]):
            # * check if password matches
            if (u for u in apiData if u.get("password") == password[0]):
                user = next((u for u in apiData if u.get("email") == email[0]), None)
                return jsonify(user), 200

            else:
                return jsonify({"message": "Incorrect password"}), 401

        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ? register route
@app.route("/register", methods=["POST"])
def register():
    # * get email and password from request args (query parameters)
    email = (request.args.get("email"),)
    password = (request.args.get("password"),)
    fullname = (request.args.get("fullname"),)
    nickname = (request.args.get("nickname"),)
    monthly_salary = (request.args.get("monthly_salary"),)
    salary_per_hour = (request.args.get("salary_per_hour"),)

    # * api data list
    apiData = requests.get(apiUrl).json()

    try:
        # * check if user already exists
        existing = next((u for u in apiData if u.get("email") == email[0]), None)

        if existing:
            return jsonify({"message": "User already exists"}), 409

        # * register new user
        else:
            new_user = {
                "email": email[0],
                "fullname": fullname[0],
                "nickname": nickname[0],
                "password": password[0],
                "salaries": [],
                "monthly_salary": monthly_salary[0],
                "salary_per_hour": salary_per_hour[0],
            }

            # ? post new user to main api
            response = requests.post(apiUrl, json=new_user)
            if response.status_code == 201:
                return (
                    jsonify(
                        {"message": "User registered successfully", "user": new_user}
                    ),
                    201,
                )
            else:
                return jsonify({"message": "Failed to register user"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ? update route
@app.route("/update", methods=["POST"])
def update():
    # * get email and password from request args (query parameters)
    email = (request.args.get("email"),)
    password = (request.args.get("password"),)
    fullname = (request.args.get("fullname"),)
    nickname = (request.args.get("nickname"),)
    salaries = (request.args.get("salaries"),)
    monthly_salary = (request.args.get("monthly_salary"),)
    salary_per_hour = (request.args.get("salary_per_hour"),)

    # * api data list
    apiData = requests.get(apiUrl).json()

    try:
        # * check if user exists
        existing = next((u for u in apiData if u.get("email") == email[0]), None)

        if existing:
            updated_user = {
                "email": email[0] if email[0] else existing.get("email"),
                "fullname": fullname[0] if fullname[0] else existing.get("fullname"),
                "nickname": nickname[0] if nickname[0] else existing.get("nickname"),
                "password": password[0] if password[0] else existing.get("password"),
                "salaries": salaries[0] if salaries[0] else existing.get("salaries"),
                "monthly_salary": (
                    monthly_salary[0]
                    if monthly_salary[0]
                    else existing.get("monthly_salary")
                ),
                "salary_per_hour": (
                    salary_per_hour[0]
                    if salary_per_hour[0]
                    else existing.get("salary_per_hour")
                ),
            }

            # ? put updated user to main api
            response = requests.put(f"{apiUrl}{existing.get('id')}", json=updated_user)
            if response.status_code == 200:
                return (
                    jsonify(
                        {"message": "User updated successfully", "user": updated_user}
                    ),
                    200,
                )
            else:
                return jsonify({"message": "Failed to update user"}), 500

        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ? delete route
@app.route("/delete", methods=["POST"])
def delete():
    # * get email from request args (query parameters)
    email = (request.args.get("email"),)

    # * api data list
    apiData = requests.get(apiUrl).json()

    try:
        # * check if user exists
        existing = next((u for u in apiData if u.get("email") == email[0]), None)

        if existing:
            # ? delete user from main api
            response = requests.delete(f"{apiUrl}{existing.get('id')}")
            if response.status_code == 200:
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"message": "Failed to delete user"}), 500

        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# * run app
if __name__ == "__main__":
    app.run(debug=True)

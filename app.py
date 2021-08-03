import sqlite3
import hmac
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
import re


class User(object):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


class Products(object):
    def __init__(self, product_name, product_type, product_price, product_description, product_image):
        self.product_name = product_name
        self.product_type = product_type
        self.product_price = product_price
        self.product_description = product_description
        self.product_image = product_image


def create_users():
    conn = sqlite3.connect('products.db')
    print("Database Created Successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "first_name TEXT NOT NULL,"
                 "last_name TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "cell_num INTEGER NOT NULL,"
                 "password TEXT NOT NULL)")
    print("User Table Created Successfully")
    conn.close()


def create_bank():
    conn = sqlite3.connect('products.db')

    conn.execute("CREATE TABLE IF NOT EXISTS banks (bank_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "acc_holder TEXT NOT NULL,"
                 "acc_num INTEGER NOT NULL,"
                 "branch_code INTEGER NOT NULL,"
                 "bank_ref TEXT NOT NULL,"
                 "FOREIGN KEY (bank_id) REFERENCES user (user_id))")
    print("Bank Table Created Successfully")
    conn.close()


def create_products():
    conn = sqlite3.connect('products.db')

    conn.execute("CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_name TEXT NOT NULL,"
                 "product_type TEXT NOT NULL,"
                 "product_price INTEGER NOT NULL,"
                 "product_description TEXT NOT NULL)")
    print("Products Table Created Successfully")
    conn.close()


def create_login():
    conn = sqlite3.connect('products.db')

    conn.execute("CREATE TABLE IF NOT EXISTS login (log_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "email TEXT NOT NULL,"
                 "password TEXT NOT NULL,"
                 "date_created TEXT NOT NULL)")
    print("Login Table Created Successfully")
    conn.close()


create_users()
create_bank()
create_products()
create_login()


def fetch_users():
    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[3], data[5]))
    return new_data


users = fetch_users()

username_table = {u.email: u for u in users}
user_id_table = {u.id: u for u in users}


def authenticate(email, password):
    user = username_table.get(email, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(number):
    user_id = number['identity']
    return user_id_table.get(user_id, None)


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/register/', methods=['POST'])
def register():
    response = {}

    email = request.form['email']
    # regular expression for validating email
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if re.search(regex, email):
        pass
    else:
        raise Exception("Invalid Email Address, Please Try Again!")

    try:
        name = str(request.form['first_name'])
        surname = str(request.form['last_name'])
        number = int(request.form['cell_num'])

        if type(name) == int or surname == int:
            raise TypeError("Use Characters Only For Your Name Please")
        elif type(number) == str:
            raise TypeError("Use Digits Only For Your Cell Number Please")
        else:
            pass
    except ValueError:
        raise TypeError("Please Use The Correct Value For Each Section")

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        cell_num = request.form['cell_num']
        password = request.form['password']

        with sqlite3.connect('products.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (first_name,"
                           "last_name,"
                           "email,"
                           "cell_num,"
                           "password) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, email, cell_num, password))
            conn.commit()

            response["message"] = "Success"
            response["status_code"] = 201

        return response


@app.route('/user-profile/<int:user_id>')
def user_profile(user_id):
    response = {}

    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id =" + str(user_id))
        users = cursor.fetchone()

        response['data'] = users
        response['status_code'] = 200
        response['message'] = "Successfully Viewed Profile"
    return response


@app.route('/update-products/<int:product_id>', methods=['PUT'])
# @jwt_required()
def update_profile(product_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('products.db') as conn:
            incoming_data = dict(request.json)
            put_data = {}
            print(incoming_data)
            # print(put_data)

            if incoming_data.get('product_name') is not None:
                put_data['product_name'] = incoming_data.get('product_name')
                print(put_data)
                with sqlite3.connect('products.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET product_name = ? WHERE product_id = ?",
                                   (put_data['product_name'], product_id))
                    conn.commit()

                    response['message'] = "Updated Product Name"
                    response['status_code'] = 200

                # return response

            if incoming_data.get('product_type') is not None:
                put_data['product_type'] = incoming_data.get('product_type')
                with sqlite3.connect('products.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET product_type = ? WHERE product_id = ?",
                                   (put_data['product_type'], product_id))
                    conn.commit()

                    response['message'] = "Updated Product Type"
                    response['status_code'] = 200

                # return response

            if incoming_data.get('product_price') is not None:
                put_data['product_price'] = incoming_data.get('product_price')
                print(put_data)
                with sqlite3.connect('products.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET product_price = ? WHERE product_id = ?",
                                   (put_data['product_price'], product_id))
                    conn.commit()

                    response['message'] = "Updated Product Price"
                    response['status_code'] = 200

                # return response

            if incoming_data.get('product_description') is not None:
                put_data['product_description'] = incoming_data.get('product_description')
                with sqlite3.connect('products.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET product_description = ? WHERE product_id = ?",
                                   (put_data['product_description'], product_id))
                    conn.commit()

                    response['message'] = "Updated Product Description"
                    response['status_code'] = 200

            return response


@app.route('/add-products', methods=["POST"])
def add_products():
    response = {}

    if request.method == "POST":
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        product_price = request.form['product_price']
        product_description = request.form["product_description"]

        with sqlite3.connect('products.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (product_name, "
                           "product_type, "
                           "product_price,"
                           "product_description) VALUES (?, ?, ?, ?)",
                           (product_name, product_type, product_price, product_description))
            conn.commit()

            response['status_code'] = 200
            response['message'] = "Product Added Successfully"

        return response


@app.route('/view-products/')
def view_products():
    response = {}

    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()

        response['status_code'] = 200
        response['data'] = products

        return response


@app.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    response = {}

    with sqlite3.connect('products.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE product_id =" + str(product_id))
        conn.commit()

        response['status_code'] = 200
        response['message'] = "Product Deleted Successfully"

    return response


if __name__ == '__main__':
    app.run(debug=True)

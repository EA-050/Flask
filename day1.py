
from flask import Flask, request 
from flask import jsonify
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

conn = psycopg2.connect(
    host = "localhost",
    database = "flask_products",
    user = "postgres",
    password = "Arsenal05."
)
cur = conn.cursor(cursor_factory = RealDictCursor)

products = []

@app.route("/products", methods = ["POST"])
def create_products():
    
    
    data = request.get_json(silent = True)
    if data is None:
        return jsonify({"error" : "invalid json"}) , 400
    if "name" not in data:
        return jsonify({"error" : "name not in data"}),400
    if "price" not in data:
        return jsonify({"error" : "price not in data"}),400
    cur.execute("""
        INSERT INTO products(name,price)
        VALUES (%s,%s)
    """, (data["name"],data["price"]))
    conn.commit()
        
    
    
    return jsonify({"message":"Products created"})

@app.route("/products", methods = ["GET"])
def get_all():
    cur.execute("""
        SELECT * FROM products
    """)

    products = cur.fetchall()

    return jsonify(products)


@app.route("/products/<int:id>" , methods = ["GET"])
def get_products(id):
    cur.execute("""SELECT * from products WHERE id = %s""", (id,))

    product = cur.fetchone()
    if product == None:
        return jsonify({"error : product not found"}) , 404

    return jsonify(product)
@app.route("/products/<int:id>", methods = ["DELETE"])
def delete(id):
    for product in products:
        if id == product["id"]:
            products.remove(product)
            return jsonify({"message":"Product Deleted"})
    return jsonify({"error" : "product not found"}),404
@app.route("/products/<int:id>" , methods = ["PUT"])
def replace(id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error" : "invalid json"}) , 400
    if "name" not in data:
            return jsonify({"error" : "no name found"}),400
    if "price" not in data:
            return jsonify({"error" : "no price found"}),400
    for product in products:
        if product["id"] == id:
            product["name"] = data["name"]
            product["price"] = data["price"]
            return jsonify({"message":"Product updated"})

    return jsonify({"error" : "id not found"}) , 404

@app.route("/products/<int:id>", methods = ["PATCH"])
def update(id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify ({"error" : "invalid Json"}) ,400
    for product in products:
        if product["id"] == id:
            if "name" in data:
                product["name"] = data["name"]
            if "price" in data:
                product["price"] = data["price"]
            return jsonify(product)
    return jsonify({"error" : "Product not found"}), 404




if __name__ == "__main__":
    app.run()
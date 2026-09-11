import os
from dotenv import load_dotenv
from flask import Flask, request 
from flask import jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()


app = Flask(__name__)

conn = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
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
    if product is None:
        return jsonify({"error : product not found"}) , 404

    return jsonify(product)
@app.route("/products/<int:id>", methods = ["DELETE"])
def delete(id):
    cur.execute("""DELETE FROM Products WHERE id = %s""",(id,))
    if cur.rowcount == 0:
         return jsonify({"error" : "product not found"}),404
    conn.commit()
    return jsonify({"message":"Product Deleted"})
   
@app.route("/products/<int:id>" , methods = ["PUT"])
def update(id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error" : "invalid json"}) , 400
    if "name" not in data:
            return jsonify({"error" : "no name found"}),400
    if "price" not in data:
            return jsonify({"error" : "no price found"}),400
    cur.execute("""Update Products
    SET name = %s , price = %s
    WHERE id = %s""",(data["name"],data["price"],id))
    conn.commit()
    if cur.rowcount == 0:
        return jsonify ({"error" : "product not found"}), 404
    
    return jsonify({"message" : "product update"})

@app.route("/products/<int:id>", methods = ["PATCH"])
def update_one(id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify ({"error" : "invalid Json"}) ,400
    if "name" in data and "price" in data:
         cur.execute("""UPDATE Products
         SET name = %s , price = %s
         WHERE id = %s""", (data["name"],data["price"],id))
    elif "name" in data:
         cur.execute("""UPDATE Products
         SET name = %s
         WHERE id = %s""",(data["name"],id))
    elif "price" in data:
         cur.execute("""UPDATE Products
         SET price = %s
         WHERE id = %s""",(data["price"] , id))
    else:
         return jsonify({"error" : "nothing to update"}),400
    conn.commit()
    if cur.rowcount == 0:
         return jsonify({"error": "product not found"}), 404
    
    return jsonify({"message" : "Product altered"})


if __name__ == "__main__":
    app.run()
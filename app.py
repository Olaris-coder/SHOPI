import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
app = Flask(__name__)
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key) if url and key else None

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/products")
def get_products():
    if not supabase:
        return jsonify({"error": "Configure SUPABASE_URL and SUPABASE_KEY in .env"}), 503
    try:
        result = supabase.table("products").select("*").eq("is_active", True).execute()
        return jsonify(result.data)
    except Exception:
        app.logger.exception("Product query failed")
        return jsonify({"error": "Could not load products from Supabase"}), 500

@app.post("/api/orders")
def create_order():
    if not supabase:
        return jsonify({"error": "Supabase is not configured"}), 503
    data = request.get_json(silent=True) or {}
    customer, items = data.get("customer", {}), data.get("items", [])
    if not customer.get("name") or not customer.get("email") or not items:
        return jsonify({"error": "Name, email, and at least one cart item are required"}), 400
    try:
        ids = [int(x["product_id"]) for x in items]
        quantities = [max(1, min(99, int(x["quantity"]))) for x in items]
        result = supabase.table("products").select("id,name,price").in_("id", ids).eq("is_active", True).execute()
        by_id = {int(p["id"]): p for p in result.data}
        order_lines, total = [], 0
        for pid, qty in zip(ids, quantities):
            product = by_id.get(pid)
            if not product:
                return jsonify({"error": "A product is unavailable. Refresh and try again."}), 400
            price = float(product["price"])
            line = round(price * qty, 2)
            total += line
            order_lines.append({"product_id": pid, "product_name": product["name"],
                                "quantity": qty, "unit_price": price, "line_total": line})
        saved = supabase.table("orders").insert({
            "customer_name": customer["name"].strip(),
            "customer_email": customer["email"].strip(),
            "customer_phone": customer.get("phone", "").strip(),
            "total": round(total, 2), "status": "Pending"
        }).execute()
        order_id = saved.data[0]["id"]
        supabase.table("order_items").insert(
            [{**line, "order_id": order_id} for line in order_lines]).execute()
        return jsonify({"message": "Order received", "order_id": order_id, "total": round(total, 2)}), 201
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid order details"}), 400
    except Exception:
        app.logger.exception("Order creation failed")
        return jsonify({"error": "Could not save order"}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")

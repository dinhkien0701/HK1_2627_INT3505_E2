from flask import Flask, jsonify
ORDERS = {} # Gia lap DB
# DELETE /order/<id>
@app.route("/order/<id>", methods = ["DELETE"])
def delete_order(order_id):
    order = ORDERS.get(order_id)
    # 404 - ko tim thay
    if order is None:
        return {"error":"not found"}, 404
    # 409 - business rule
    if order["status"] in ("shipped","delivered"):
        return {"error":"connot delete"}, 409
    ORDERS.pop(order_id, None)
    # 204 - thanh cong, no body
    return "", 204

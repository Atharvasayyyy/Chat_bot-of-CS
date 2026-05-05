# test_tools.py

from tools.db_user_tool import get_user_info
from tools.db_order_tool import get_user_orders
from tools.db_verification_tool import verify_purchase
from tools.db_update_tool import increment_complaint

# 🔹 TEST USER INFO
print("---- USER INFO ----")
print(get_user_info.run("U001"))

# 🔹 TEST USER ORDERS
print("\n---- USER ORDERS ----")
print(get_user_orders.run("U001"))

# 🔹 TEST VERIFY PURCHASE (VALID)
print("\n---- VERIFY PURCHASE (VALID) ----")
print(verify_purchase.run({
    "user_id": "U001",
    "product_name": "Fan"
}))

# 🔹 TEST VERIFY PURCHASE (INVALID)
print("\n---- VERIFY PURCHASE (INVALID) ----")
print(verify_purchase.run({
    "user_id": "U001",
    "product_name": "TV"
}))

# 🔹 TEST COMPLAINT INCREMENT
print("\n---- INCREMENT COMPLAINT ----")
print(increment_complaint.run("U001"))
print(get_user_info.run("U001"))
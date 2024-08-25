import streamlit as st
import pandas as pd
from collections import deque
import os

# Initialize CSV file paths
BUY_ORDERS_CSV = "buy_orders.csv"
SELL_ORDERS_CSV = "sell_orders.csv"

# Function to save orders to CSV
def save_orders_to_csv(order, order_type):
    if order_type == "Buy":
        df = pd.DataFrame([order])
        if os.path.exists(BUY_ORDERS_CSV):
            df.to_csv(BUY_ORDERS_CSV, mode='a', header=False, index=False)
        else:
            df.to_csv(BUY_ORDERS_CSV, index=False)
    else:
        df = pd.DataFrame([order])
        if os.path.exists(SELL_ORDERS_CSV):
            df.to_csv(SELL_ORDERS_CSV, mode='a', header=False, index=False)
        else:
            df.to_csv(SELL_ORDERS_CSV, index=False)

# Function to load orders from CSV
def load_orders_from_csv(order_type):
    if order_type == "Buy" and os.path.exists(BUY_ORDERS_CSV):
        return deque(pd.read_csv(BUY_ORDERS_CSV).fillna("").to_dict('records'))
    elif order_type == "Sell" and os.path.exists(SELL_ORDERS_CSV):
        return deque(pd.read_csv(SELL_ORDERS_CSV).fillna("").to_dict('records'))
    else:
        return deque()

# Load existing orders from CSV
buy_orders = load_orders_from_csv("Buy")
sell_orders = load_orders_from_csv("Sell")

# Function to match orders
def match_orders():
    global buy_orders, sell_orders
    matched_orders = []

    while buy_orders and sell_orders:
        buy_order = buy_orders[0]
        sell_order = sell_orders[0]

        if buy_order['price'] >= sell_order['price']:
            match_quantity = min(buy_order['quantity'], sell_order['quantity'])

            matched_orders.append({
                'buy_order_id': buy_order['order_id'],
                'sell_order_id': sell_order['order_id'],
                'price': sell_order['price'],
                'quantity': match_quantity
            })

            # Update quantities
            buy_order['quantity'] -= match_quantity
            sell_order['quantity'] -= match_quantity

            if buy_order['quantity'] == 0:
                buy_orders.popleft()
            if sell_order['quantity'] == 0:
                sell_orders.popleft()
        else:
            break

    return matched_orders

# Streamlit UI
st.title("Simplified Matching Engine")

# Input form for new orders
st.subheader("Enter a New Order")
order_type = st.selectbox("Order Type", ["Buy", "Sell"])
price = st.number_input("Price", min_value=0.0, format="%.2f")
quantity = st.number_input("Quantity", min_value=1)
submit = st.button("Submit Order")

if submit:
    order_id = len(buy_orders) + len(sell_orders) + 1
    new_order = {
        'order_id': order_id,
        'price': price,
        'quantity': quantity,
        'time': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if order_type == "Buy":
        buy_orders.append(new_order)
        # Sort buy orders by price (highest first), then time (earliest first), then quantity (highest first)
        buy_orders = deque(sorted(buy_orders, key=lambda x: (-x['price'], x['time'], -x['quantity'])))
    else:
        sell_orders.append(new_order)
        # Sort sell orders by price (lowest first), then time (earliest first), then quantity (highest first)
        sell_orders = deque(sorted(sell_orders, key=lambda x: (x['price'], x['time'], -x['quantity'])))

    # Save the new order to CSV
    save_orders_to_csv(new_order, order_type)

    st.success(f"{order_type} order submitted!")

# Match orders
matched_orders = match_orders()

# Display the order book
st.subheader("Order Book")
col1, col2 = st.columns(2)

with col1:
    st.write("### Buy Orders")
    st.table(pd.DataFrame(list(buy_orders), columns=['order_id', 'price', 'quantity', 'time']))

with col2:
    st.write("### Sell Orders")
    st.table(pd.DataFrame(list(sell_orders), columns=['order_id', 'price', 'quantity', 'time']))

# Display matched orders
if matched_orders:
    st.subheader("Matched Orders")
    st.table(pd.DataFrame(matched_orders))

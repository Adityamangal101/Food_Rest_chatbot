import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
global conn

# Read credentials from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
    "connect_timeout": 10
}


def get_connection():
    """Create and return a fresh MySQL connection, reconnecting if needed."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        # 🔥 Ping ensures the connection is alive before returning it
        conn.ping(reconnect=True)
        return conn
    except Exception as e:
        print("❌ DB Connection Error:", e)
        return None


def get_order_status(order_id: int):
    """Return the status of an order by ID."""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()

    query=("SELECT status FROM order_tracking WHERE order_id = %s")

    cursor.execute(query,(order_id,))

    result = cursor.fetchone()

    return result["status"] if result else None

    conn.close()


def get_next_order_id():
    """Generate new order id."""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()

    query=("SELECT MAX(order_id) as max_id FROM orders")

    cursor.execute(query)

    result = cursor.fetchone()
    # result is a dict like: {"max_id": 5}
    max_id =result['max_id'] if result['max_id'] else 0
    return max_id +1 

    conn.close()

def insert_order_item(food_item, quantity, order_id):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        conn.ping(reconnect=True)
        with conn.cursor() as cursor:
            cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        conn.commit()
        print("✅ Order item inserted successfully")
        return 1

    except pymysql.MySQLError as err:
        print(f"❌ Error inserting order item: {err}")
        conn.rollback()
        return -1

    finally:
        conn.close()



def get_total_order_price(order_id):
    """Call the MySQL user-defined function get_total_order_price(order_id) and return the result."""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    
    # To get total order price
    query=f"SELECT get_total_order_price({order_id}) AS total"
    cursor.execute(query)

    result=cursor.fetchone()

    return result['total'] if  result and result['total'] else 0.0

    conn.close()


def insert_order_tracking(order_id,status):
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()

    # Inserting the record into the order_tracking table
    insert_query="INSERT INTO order_tracking(order_id,status) VALUES (%s,%s)"
    cursor.execute(insert_query,(order_id,status))

    #Commiting the changes
    conn.commit()

    # Closing the cursor
    conn.close()



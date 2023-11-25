import mysql.connector
from flask import Flask, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'secretkey'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure your MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pass',
    'database': 'apmc_2'
}

class User(UserMixin):
    def __init__(self, user_id, f_name, l_name, role):
        self.id = user_id
        self.first_name = f_name
        self.last_name = l_name
        self.role = role

#This guy is called internally whenever login_user(user) is called
@login_manager.user_loader
def load_user(user_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute(f"SELECT * from users where id = %s",(user_id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    if (user_data):
        return User(*user_data)
    pass

# TO make sure is_authenticated is available globally
@app.context_processor
def inject_is_authenticated():
    return {'is_authenticated': current_user.is_authenticated}

def get_cols(table_name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    query = f"""SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s
    ORDER BY ORDINAL_POSITION"""
    cur.execute(query, (table_name, 'apmc'))
    cols = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return cols

def get_rows(table_name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    #print(cols)
    cur.close()
    conn.close()
    return rows, cols

def verify_user(f_name, l_name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    query = f"select * from users where first_name = %s and last_name = %s;"
    cur.execute(query,(f_name,l_name))
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res

# functions.py

import mysql.connector

def place_bid(market_id,trader_id, commodity_id, bid_amount, bid_quantity,bid_date=None):
    if bid_date is None:
        bid_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Replace with your MySQL connection details
        # Establish a connection to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Assuming you have a "bids" table with appropriate columns
        # Replace with the actual table and column names in your database
        query = """
            INSERT INTO bid (market_id, trader_id,commodity_id, bid_amount, bid_quantity,bid_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (market_id, trader_id, commodity_id, bid_amount, bid_quantity,bid_date)

        cursor.execute(query, values)

        conn.commit()

    except Exception as e:
        # Handle exceptions appropriately (e.g., log the error)
        print(f"Error placing bid: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def get_traders_and_commodities_for_market(market_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    query = """
    SELECT t.idtrader, t.first_name, t.last_name, c.idcommodity, c.commodity_name, c.description, COALESCE(SUM(tr.quantity), 0) AS available_quantity
    FROM trader t
    LEFT JOIN transaction tr ON t.idtrader = tr.trader_id
    LEFT JOIN commodity c ON tr.commodity_id = c.idcommodity
    WHERE t.market_id = %s
    GROUP BY t.idtrader, c.idcommodity;
    """

    cur.execute(query, (market_id,))
    traders_commodities = cur.fetchall()

    cur.close()
    conn.close()

    return traders_commodities

def get_available_commodities():
    try:
        # Establish a connection to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to fetch available commodities
        query = """
            SELECT
                c.idcommodity,
                c.commodity_name,
                c.description AS commodity_description,
                COALESCE(SUM(t.quantity), 0) AS available_quantity
            FROM commodity c
            LEFT JOIN transaction t ON c.idcommodity = t.commodity_id
            WHERE t.status = 'Completed'  # Assuming you have a status field indicating completed transactions
            GROUP BY c.idcommodity, c.commodity_name, c.description
        """
        
        cursor.execute(query)
        available_commodities = cursor.fetchall()

        return available_commodities

    except Exception as e:
        # Handle exceptions appropriately (e.g., log the error)
        print(f"Error fetching available commodities: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def display_commodities(commodity_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch commodities with their highest bid
    query = """
        SELECT commodity_name, highest_bid
        FROM commodity where idcommodity = %s ;
    """
    cursor.execute(query,(commodity_id,))
    commodities = cursor.fetchall()

    cursor.close()
    conn.close()

    return commodities

def get_payment_info(trader_id):

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    query = """
    SELECT 
    t.idtransaction, 
    c.commodity_name, 
    t.quantity,  
    p.amount,
    t.transaction_date,
    p.payment_date
    FROM transaction t
    LEFT JOIN commodity c ON t.commodity_id = c.idcommodity
    LEFT JOIN payment p ON t.idtransaction = p.transaction_id
    WHERE t.trader_id = %s;
    """

    cur.execute(query, (trader_id,))
    payments = cur.fetchall()
    
    cur.close()
    conn.close()

    return payments
    
def delete_payment_from_database(transaction_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        # Assuming your payment table has a primary key named idtransaction
        delete_query = "DELETE FROM payment WHERE transaction_id = %s"
        cur.execute(delete_query, (transaction_id,))

        # Commit the changes
        conn.commit()

    except Exception as e:
        # Handle exceptions, log errors, or return an error response
        print(f"Error deleting payment: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()    



def insert_transaction(farmer_name, commodity_id,commodity_name,quantity, quality, description, market_id, trader_id, transaction_date=None):
    if transaction_date is None:
        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = mysql.connector.connect(**db_config)
    cur = None

    try:
        cur = conn.cursor()
        query = """
        INSERT INTO transaction (farmer_name, commodity_id,commodity_name, quantity, quality, description, market_id, trader_id, transaction_date)
        VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s) 
        """
        values = (farmer_name, commodity_id,commodity_name, quantity, quality, description, market_id, trader_id, transaction_date)

        cur.execute(query, values)
        conn.commit()

    except Exception as e:
        print(f"Error inserting transaction: {e}")

    finally:
        if cur:
            cur.close()
        conn.close()

# DSL.py
def delete_transaction_by_id(transaction_id):
    conn = mysql.connector.connect(**db_config)
    cur = None

    try:
        cur = conn.cursor()
        query = """
        DELETE FROM transaction
        WHERE idtransaction = %s
        """
        values = (transaction_id,)

        cur.execute(query, values)
        conn.commit()

        return True

    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False

    finally:
        if cur:
            cur.close()
        conn.close()


def insert_commodities(commodity_id,commodity_name, description):
        
        conn = mysql.connector.connect(**db_config)
        cur = None
        error_message = None

        try:
            cur = conn.cursor()
            query_commodity_check = "SELECT * FROM commodity WHERE idcommodity = %s"
            cur.execute(query_commodity_check, (commodity_id,))
            existing_commodity = cur.fetchone()

            if existing_commodity:
                query_commodity_update = """
                UPDATE commodity
                SET commodity_name = %s, description = %s
                WHERE idcommodity = %s
                """
                values_commodity_update = (commodity_name, description, commodity_id)
                cur.execute(query_commodity_update, values_commodity_update)
            else:
                query_commodity_insert = """
                INSERT INTO commodity (idcommodity, commodity_name, description)
                VALUES (%s, %s, %s)
                """
                values_commodity = (commodity_id, commodity_name, description)
                cur.execute(query_commodity_insert, values_commodity)

            conn.commit()

        except Exception as e:
            error_message = f"Error inserting commodity: {e}"

        finally:
                if cur:
                    cur.close()
                conn.close()

                return error_message


def get_quality_assessment():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT * FROM quality_assessment
        """
        cursor.execute(query)
        quality_assessment = cursor.fetchall()

    except Exception as e:
        print(f"Error fetching quality assessment: {e}")
        quality_assessment = None

    finally:
        cursor.close()
        conn.close()

    return quality_assessment


def update_commodity_price(commodity_id, commodity_price):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    try:
        # Get the current commodity information
        select_query = "SELECT * FROM commodity WHERE idcommodity = %s"
        cur.execute(select_query, (commodity_id,))
        current_commodity = cur.fetchone()

        # Update the commodity price in the database
        update_query = "UPDATE commodity SET pricing_trend = %s WHERE idcommodity = %s"
        cur.execute(update_query, (commodity_price, commodity_id))

        # Insert a new record in the commodity_price_history table
        insert_query = "INSERT INTO commodity_price_history (commodity_id, old_price, new_price, change_date) VALUES (%s, %s, %s, %s)"
        cur.execute(insert_query, (commodity_id, current_commodity[3], commodity_price, datetime.now()))

        # Commit the changes to the database
        conn.commit()

        # Optionally, you can return the updated commodity
        return cur.rowcount  # This will return the number of rows affected

    except Exception as e:
        # Handle the exception, log it, or return an error message
        return str(e)
    
def get_transactions(trader_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    query = """
    SELECT idtransaction,farmer_name,commodity_id,commodity_name,quantity, quality, description,transaction_date FROM transaction
    WHERE trader_id = %s
    ORDER BY transaction_date DESC
    """
    
    cur.execute(query, (trader_id,))
    transactions = cur.fetchall()
    
    cur.close()
    conn.close()

    return transactions


#integrating other queries

def get_market_details(id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    query = f"""select tr.idtrader, tr.first_name, tr.last_name, rght.commodity_name, rght.quantity
                from trader tr
                left join
                (select C.commodity_name, T.quantity, T.trader_id
                from transaction T
                left join commodity C
                on T.commodity_id = C.idcommodity) as rght
                on tr.idtrader = rght.trader_id
                where tr.market_id = %s;"""
    cur.execute(query, (id,))
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows, cols


# @app.route('/')
# def index():
#     # Your application logic, including database operations, goes here
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for,flash
from DSL import app, login_manager, verify_user, get_cols, get_rows,get_market_details,get_traders_and_commodities_for_market,place_bid,insert_transaction,get_available_commodities, insert_commodities,get_transactions,get_payment_info,display_commodities,get_quality_assessment,delete_payment_from_database,delete_transaction_by_id,User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
# app = Flask(__name__)

@app.route('/')
def home():
    data = 'This is the home page'
    return render_template('home.html', value = data)

@app.route('/login', methods = ['GET','POST'])
def login():
    if(request.method == 'POST'):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_data = verify_user(first_name,last_name)
        if(user_data):
            user = User(*user_data)
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'bidder':
                return redirect(url_for('bidder'))
            elif user.role == 'trader':
                return redirect(url_for('trader'))
            
    return render_template('login.html')


@app.route('/place_bid', methods=['POST'])
def place_bid_route():
    market_id = request.form.get('market_id')
    commodity_id = request.form.get('commodity_id')
    trader_id = request.form.get('trader_id')  # Assuming you have a function to get the current user

    bid_amount = request.form.get('bid_amount')
    bid_quantity = request.form.get('bid_quantity')
    bid_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(market_id,trader_id,commodity_id,bid_amount,bid_quantity)
    
    # Assuming you have a function to place a bid
    place_bid(market_id,trader_id, commodity_id, bid_amount,bid_quantity,bid_date)
    # The place_bid function should execute a SQL query to update the bid information in the database
    # ...

    # Redirect to the bidder route or any other route after placing the bid
    return redirect(url_for('bidder'))



from flask_login import current_user


@app.route('/bidder', methods=['GET', 'POST'])
def bidder():
    traders_commodities = None
    if request.method == 'POST':
        market_id = request.form['market_id']
        
        traders_commodities = get_traders_and_commodities_for_market(market_id)

        return render_template('bidder.html', traders_commodities=traders_commodities, market_id=market_id)
    
    return render_template('bidder.html', traders_commodities=None, market_id=None)

@app.route('/trader', methods=['GET', 'POST'])
@login_required
def trader():

    inserted_transaction = None  # Initialize the variable outside of the conditional block
    
    if request.method == 'POST':
        farmer_name = request.form.get('farmer_name')
        commodity_id = request.form.get('commodity_id')
        quantity = request.form.get('quantity')
        quality = request.form.get('quality')
        print(quality)
        description = request.form.get('description')
        market_id = request.form.get('market_id')  # Assuming market_id is associated with the current trader
        trader_id = current_user.id  # Assuming you have a trader ID associated with the current user
        commodity_name = request.form.get('commodity_name')
        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_commodities(commodity_id,commodity_name, description)
        # Assuming you have a function to insert the transaction in your DSL module
        inserted_transaction = insert_transaction(farmer_name, commodity_id,commodity_name, quantity, quality, description, market_id, trader_id,transaction_date )
        
        
    

    return render_template('trader_3.html', inserted_transaction=inserted_transaction)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    # Implement your logic to delete the transaction with the given ID
    # For example, you might have a function like delete_transaction_by_id(transaction_id)
    # Make sure to add proper error handling

    # Assuming you have a function to delete the transaction
    success = delete_transaction_by_id(transaction_id)

    if success:
        # Redirect to the transactions page after successful deletion
        return redirect(url_for('view_transactions'))
    else:
        # Handle the case where deletion fails
        return render_template('error.html', message='Failed to delete transaction.')

@app.route('/quality_assessment',methods=['GET','POST'])
@login_required
def quality_assessment():
    quality_assessment = None
    
   
    quality_assessment = get_quality_assessment()
    return render_template('quality_assessment.html', quality_assessment = quality_assessment)

@app.route('/delete_payment', methods=['POST'])
def delete_payment():
    if request.method == 'POST':
        transaction_id = request.form.get('transaction_id')
        print(f"Deleting transaction with ID: {transaction_id}")
        # Perform the deletion in the database using the transaction_id
        delete_payment_from_database(transaction_id)

        # Redirect to the payments page or wherever appropriate
        print("Redirecting to payment_info route")
        return redirect(url_for('payment_info'))

    # Handle other cases if needed
    return render_template('error.html', message='Invalid request')


@app.route('/transactions',methods=['GET', 'POST'])
@login_required
def view_transactions():
    trader_id = current_user.id
    
    transactions = get_transactions(trader_id)
    
    return render_template('transactions.html', transactions=transactions)

@app.route('/payment',methods=['GET','POST'])
@login_required
def payment_info():
    trader_id = current_user.id
    payments = get_payment_info(trader_id)

    
    return render_template('payment.html', payments=payments)

@app.route('/commodities', methods = ['GET','POST'])
def highest_commodity():
    commodity_id = request.form.get('commodity_id_in_another_form')
    
    commodities = display_commodities(commodity_id)
    return render_template('commodities.html', commodities=commodities)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',role = current_user.role, fname = current_user.first_name, lname = current_user.last_name)
    # return f"Welcome, {current_user.first_name} {current_user.last_name}! You are logged in as {current_user.role}."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/table_<table_name>')
# def list_values(table_name):
#     table_rows = get_rows(table_name)
#     #print(table_rows)
#     table_cols = get_cols(table_name)
#     #print(table_cols)
#     return render_template('print_table_base.html',table_name = table_name,cols = table_cols, rows = table_rows)

#integrating other functions.

@app.route('/admin_dashboard', methods = ['GET','POST'])
@login_required
def admin_dashboard():
    selected_table = None
    if request.method == 'POST':
        selected_table = request.form.get('selected_table')
    return render_template('admin_dashboard.html',role=current_user.role, fname=current_user.first_name, lname=current_user.last_name, selected_table=selected_table, get_table = get_table)

@app.route('/market_details',methods = ['GET','POST'])
def market_details():
    selected_market = None
    if request.method == 'POST':
        selected_market = request.form.get('selected_market')
    rows,cols = get_market_details(selected_market) 
    print(cols,rows)
    return render_template('market_details.html', get_table = get_table, get_market_details = get_market_details,selected_market = selected_market)

def get_table(table_name):
    table_rows, table_cols = get_rows(table_name)
    return render_template('print_table_base_2.html', table_name=table_name, cols=table_cols, rows=table_rows)

if __name__ == '__main__':
    app.run(debug=True)

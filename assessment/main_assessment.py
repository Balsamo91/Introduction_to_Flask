from flask import Flask, render_template, request, redirect
import datetime

app = Flask(__name__)

warehouse_list = [
    {
        'name': 'Bike',
        'price': 300,
        'quantity': 12
    },
    {
        'name': 'Electric scooter',
        'price': 350,
        'quantity': 7
    },
    {
        'name': 'Coke',
        'price': 2,
        'quantity': 100
    }
]

account = 12500

operations_recorded = [
        {
        'type': 'purchase action',
        'name': 'fanta',
        'price': 1,
        'quantity': 100,
        'timestamp': '2024-06-03 12:22:49',
    },
    {
        'type': 'sale action',
        'name': 'coke',
        'price': 5,
        'quantity': 99,
        'timestamp': '2024-06-05 12:22:49',
    }
]

@app.route('/')
def index():
    return render_template("index.html", warehouse=warehouse_list, balance=account)


@app.route('/purchase')
def purchase():
    return render_template('purchase.html', balance=account)

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    global account
    # Get the name, breed and age from the form submission
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    if account > price:
    # If user enters the same item, this will catch it and it will add the quantity, if not it will add the dict to the list warehouse_list[] 
        item_exist = False
        for p in warehouse_list:
            if p["name"] == name:
                p["quantity"] += quantity
                item_exist = True
                break
        if not item_exist:
            warehouse_list.append({"name" : name, "price" : price, "quantity" : quantity})
        account -= price * quantity # substract the purchased items from the account
    
        operations_recorded.append({
            'type': 'purchase action',
            'name': name,
            'price': price,
            'quantity': quantity,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # Redirect me to the main page
    return redirect('/') 


@app.route('/sale')
def sale():
    return render_template("sale.html", balance=account)

@app.route('/submit_sale', methods=['POST'])
def submit_sale():
    global account
    # Get the name, breed and age from the form submission
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    # Append the dog to the list of dogs 
    for s in warehouse_list:
            if s["name"] == name and (s["price"] <= price or s["price"] >= price) and s["quantity"] >= quantity:
                s["quantity"] -= quantity
                account += price * quantity
                if s['quantity'] <= 0:
                    warehouse_list.remove(s)

                operations_recorded.append({
                    'type': 'sale action',
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                break

    # Redirect me to the main page
    return redirect('/') 

@app.route('/balance')
def balance():
    return render_template("balance.html", balance=account)

@app.route('/submit_balance', methods=['POST'])
def submit_balance():
    global account
    amount = float(request.form['money']) # 'money' is the name found in the balance.html
    operation = request.form['balance'] # 'balance' is the name found in the balance.html

    if operation == 'Add':
        account += amount
        operations_recorded.append({
            'type': 'balance action',
            'name': 'Add',
            'price': amount,
            'quantity': 'N/A',
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    elif operation == 'Withdraw' and account >= amount:
        account -= amount
        operations_recorded.append({
            'type': 'balance action',
            'name': 'Withdraw',
            'price': amount,
            'quantity': 'N/A',
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Redirect me to the main page
    return redirect('/') 


@app.route('/history')
def history():
    return render_template("history.html", operations_recorded=operations_recorded, balance=account)

app.run(debug=True)




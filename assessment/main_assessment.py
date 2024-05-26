from flask import Flask, render_template, request, redirect

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

@app.route('/')
def index():
    return render_template("index.html", warehouse=warehouse_list, balance=account)


@app.route('/purchase')
def purchase():
    return render_template('purchase.html', balance=account)

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    # Get the name, breed and age from the form submission
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    # Append the dog to the list of dogs 
    warehouse_list.append({
        'name': name,
        'price': price,
        'quantity': quantity
    })
    
    # Redirect me to the main page
    return redirect('/') 


@app.route('/sale')
def sale():
    return render_template("sale.html", balance=account)

@app.route('/submit_sale', methods=['POST'])
def submit_sale():
    # Get the name, breed and age from the form submission
    name = request.form['name']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    # Append the dog to the list of dogs 
    for s in warehouse_list:
            if s["name"] == name:
                s["quantity"] -= quantity
                if s['quantity'] <= 0:
                    warehouse_list.remove(s)
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
    elif operation == 'Withdraw' and account >= amount:
        account -= amount

    # Redirect me to the main page
    return redirect('/') 


@app.route('/history')
def history():
    return render_template("history.html")

app.run(debug=True)




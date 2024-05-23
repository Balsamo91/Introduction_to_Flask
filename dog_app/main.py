from flask import Flask, render_template, request, redirect

app = Flask(__name__)

dogs = [
    {
        'name': 'Fido',
        'breed': 'Golden Retriever',
        'age': 5
    },
    {
        'name': 'Rex',
        'breed': 'German Shepherd',
        'age': 3
    },
    {
        'name': 'Spot',
        'breed': 'Dalmatian',
        'age': 2
    }
]

@app.route('/')
def index():
    return render_template("index.html", dogs_list=dogs) 
    # The dogs_list=dogs we are calling the dogs list in the render templete to be shown in the website

@app.route('/add_dog')
def add_dog():
    return render_template('add_dog.html')

@app.route('/submit_dog', methods=['POST'])
def submit_dog():
    # Get the name, breed and age from the form submission
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']

    # Append the dog to the list of dogs 
    dogs.append({
        'name': name,
        'breed': breed,
        'age': age
    })
    
    # Redirect me to the main page
    return redirect('/') 

app.run(debug=True)
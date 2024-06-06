from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dog_app.db'
db = SQLAlchemy(app)



# dogs = [
#     {
#         'name': 'Fido',
#         'breed': 'Golden Retriever',
#         'age': 5
#     },
#     {
#         'name': 'Rex',
#         'breed': 'German Shepherd',
#         'age': 3
#     },
#     {
#         'name': 'Spot',
#         'breed': 'Dalmatian',
#         'age': 2
#     }
# ]

class Dogs(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Uniques ID for each entry primary_key = True
    name = db.Column(db.String(20), nullable=False) # nullable=False means that it cannot be empty is set to True then can be empty. the string(20) means maximum of 20 characters
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, server_default=db.func.now()) # Take time and take the current time



@app.route('/')
def index():
    dogs = Dogs.query.all()
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
    # dogs.append({
    #     'name': name,
    #     'breed': breed,
    #     'age': age
    # })
    new_dog = Dogs(name=name, breed=breed, age=age)
    db.session.add(new_dog)
    db.session.commit()
    
    # Redirect me to the main page
    return redirect('/') 

@app.route('/update_dog')
def update_dog():
    return render_template('update_dog.html')

@app.route('/submit_update_dog', methods=['POST'])
def submit_update_dog():
    entry_id = request.form['id']
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']

    dog = Dogs.query.filter_by(id=entry_id).first() # query the db and filter by the ID and first() means getting only 1 id.
    dog.name = name if name else dog.name 
    dog.breed = breed if breed else dog.breed 
    dog.age = age if age else dog.age

    db.session.commit()

    return redirect('/')

@app.route('/delete_dog/<dog_id>', methods=['GET','POST'])
def delete_dog(dog_id):
    dog = Dogs.query.filter_by(id=dog_id).first()
    db.session.delete(dog)
    db.session.commit()

    return redirect('/')



with app.app_context():
    db.create_all()


app.run(debug=True)
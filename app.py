from flask import Flask, render_template, request, redirect, url_for, flash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a secure key

# Dummy user database for demonstration
users = {}

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Results page route
@app.route('/results', methods=['POST'])
def results():
    city = request.form['city']
    routes = []

    # Read routes from CSV file
    with open('data/routes.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0].lower() == city.lower():
                routes.append(row[1:])

    return render_template('results.html', city=city, routes=routes)

# Feedback page route
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route to handle feedback submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']

    # Write feedback data to CSV file
    with open('data/feedback.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email, feedback])

    return render_template('thank_you.html')

# Route to view feedback with delete option
@app.route('/view_feedback')
def view_feedback():
    feedback_data = []

    # Read feedback data from CSV file
    with open('data/feedback.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        feedback_data = list(reader)

    return render_template('view_feedback.html', feedback_data=feedback_data)

# Route to handle feedback deletion
@app.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    feedback_data = []

    # Read feedback data from CSV file
    with open('data/feedback.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        feedback_data = list(reader)

    # Remove the feedback entry with the given ID
    if 0 <= feedback_id < len(feedback_data):
        del feedback_data[feedback_id]

    # Write the updated feedback data back to the CSV file
    with open('data/feedback.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(feedback_data)

    return redirect(url_for('view_feedback'))

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials
        if username in users and users[username] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Signup page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Register new user
        if username not in users:
            users[username] = password
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User already exists', 'danger')
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()
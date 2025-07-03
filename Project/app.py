from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import bcrypt


app = Flask(__name__)
app.secret_key = os.urandom(24)
 
# AWS Configuration
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
user_table = dynamodb.Table('Users')
orders_table = dynamodb.Table('Orders')


# Email Configuration
EMAIL_ADDRESS = 'susmithaghantasala7@gmail.com'
EMAIL_PASSWORD = 'hvop ohwp vtku ihuu' 



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/veg-pickles')
def veg_pickles():
    return render_template('veg_pickles.html')

@app.route('/non-veg-pickles')
def non_veg_pickles():
    return render_template('non_veg_pickles.html')

@app.route('/snacks')
def snacks():
    return render_template('snacks.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        return redirect(url_for('success'))
    return render_template('checkout.html')

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Get user from DynamoDB
        response = user_table.get_item(Key={'username': username})
        user = response.get('Item')

        if user:
            hashed_password = user['password'].value if hasattr(user['password'], 'value') else user['password']
            if bcrypt.checkpw(password, hashed_password.encode('utf-8')):
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('User not found', 'danger')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Check if user already exists
        response = user_table.get_item(Key={'username': username})
        if 'Item' in response:
            flash('Username already exists!', 'danger')
            return render_template('signup.html')

        # Hash the password
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        # Save user to DynamoDB
        user_table.put_item(
            Item={
                'username': username,
                'email': email,
                'password': hashed.decode('utf-8')  # Store as string
            }
        )

        # Send welcome email
        send_email(email, 'Welcome to Home made Pickles!', 'Thank you for signing up!')

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_content = request.form['message']

        # Combine the message
        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message_content}"

        # Send email to yourself
        send_email(EMAIL_ADDRESS, 'New Contact Us Message', body)

        flash('Your message has been sent! Thank you for contacting us.', 'success')
        return redirect(url_for('contact_us'))

    return render_template('contact_us.html')


# Email Sending Function
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=5000)


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

# Set the secret key
app.secret_key = 'your_secret_key_here'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dhruv@123987'
app.config['MYSQL_DB'] = 'flask1'

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'dhruvsharmano2@gmail.com'
# app.config['MAIL_PASSWORD'] = 'mercil123987'

# mail = Mail(app)

mysql = MySQL(app)

# def send_registration_email(email):
#     msg = Message('Welcome to Our Website!', sender='dhruvsharmano2@gmail.com', recipients=[email])
#     mail.send(msg)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s \
			AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('home.html', msg=msg)
		else:
			msg = 'Incorrect username or password !'
	return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z]+', username):
			msg = 'name must contain only characters !'
		elif not re.search(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
			msg = 'Invalid password !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',(username, password, email,organisation, address, city,state, country, postalcode, ))
			mysql.connection.commit()
			# send_registration_email(email)
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("home.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("profile.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			postalcode = request.form['postalcode']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM accounts WHERE username = % s',(username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z]+', username):
				msg = 'Name must contain only characters !'
			else:
				cursor.execute('UPDATE accounts SET username =% s,\
				password =% s, email =% s, organisation =% s, \
				address =% s, city =% s, state =% s, \
				country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation,address, city, state, country, postalcode,(session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update1.html", msg=msg)
	return redirect(url_for('login'))

@app.route("/about")
def about():
	if 'loggedin' in session:
		return render_template("about.html")
	return redirect(url_for('login'))

@app.route("/profile", methods=['GET', 'POST'])
def profile():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("profile.html", account=account)
	return redirect(url_for('login'))

@app.route("/contact")
def contact():
	if 'loggedin' in session:
		return render_template("contact.html")
	return redirect(url_for('login'))

@app.route("/courses")
def courses():
	if 'loggedin' in session:
		return render_template("courses.html")
	return redirect(url_for('login'))

@app.route("/teachers")
def teachers():
	if 'loggedin' in session:
		return render_template("teachers.html")
	return redirect(url_for('login'))

@app.route("/playlist")
def playlist():
	if 'loggedin' in session:
		return render_template("playlist.html")
	return redirect(url_for('login'))



if __name__ == "__main__":
	app.run(host="localhost", port=int("5000"))

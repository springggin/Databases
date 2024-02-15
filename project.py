#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime, timedelta


print(datetime.now())
#Initialize the app from Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '2f3d45e6c1b9f87a59d5e7c8a28bfe4d'


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='aironline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#search for future flights
@app.route('/search',methods=['GET','POST'])
def search():
    # grabs information from the forms
	dep_airport = request.form.get('dep_airport')
	arr_airport = request.form.get('arr_airport')
	dep_date = request.form.get('dep_date')
	return_date = request.form.get('return_date',None)
	print(return_date)
	cursor = conn.cursor()
	query1 = '''
			SELECT Airline_name, flight.ID as flight_num, dep_date, dep_time, arr_date,arr_time
			FROM flight, airplane 
			WHERE Airplane_ID = airplane.ID 
			AND dep_airport = %s 
			AND arr_airport = %s 
			AND dep_date = %s;'''	
	cursor.execute(query1, (dep_airport, arr_airport, dep_date)) 
	data1 = cursor.fetchall()
	
	
	if return_date and return_date != '':
		query2 = '''
        SELECT  flight.ID as flight_num, dep_date, dep_time, arr_date, arr_time, Airline_name
        FROM flight, airplane 
        WHERE Airplane_ID = airplane.ID 
        AND dep_airport = %s 
        AND arr_airport = %s 
        AND dep_date = %s;'''
		cursor.execute(query2, (arr_airport, dep_airport , return_date)) 
		data2 = cursor.fetchall()
		cursor.close()
		return render_template('index.html', dep_airport=dep_airport, arr_airport=arr_airport, dep_date=dep_date, 
							return_date=return_date, flights=data1, flights2=data2)

	else: 
		cursor.close()
		return render_template('index.html', dep_airport=dep_airport, arr_airport=arr_airport, dep_date=dep_date, 
							return_date=return_date, flights=data1)
	

#flights status
@app.route('/flight_status',methods=['GET','POST'])
def flight_status():
    # grabs information from the forms
	dep_airport = request.form.get('dep_airport',None)
	arr_airport = request.form.get('arr_airport',None)
	dep_date = request.form.get('dep_date',None)
	return_date = request.form.get('return_date',None)

	cursor = conn.cursor()
	query = '''
			SELECT Airline_name, flight.ID as flight_num, dep_date, dep_time, arr_date,arr_time, status 
			FROM flight, airplane 
			WHERE Airplane_ID = airplane.ID 
			AND dep_airport = %s 
			AND arr_airport = %s 
			AND dep_date = %s;'''
			
	cursor.execute(query, (dep_airport, arr_airport, dep_date)) #
	data = cursor.fetchall() 
	cursor.close()
	return render_template('flight_status.html', flights=data)

#Define route for register
@app.route('/regcustomer')
def regcustomer():
	return render_template('register_customer.html')

@app.route('/regstaff')
def regstaff():
	return render_template('register_staff.html')

@app.route('/customerregAuth', methods=['GET', 'POST'])
def customerregAuth():
	#grabs information from the forms
	fname = request.form['fname']
	lname = request.form['lname']
	email = request.form['email']
	password = request.form['password']
	dob = request.form['dob']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_customer.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(ins, (fname, lname, email, password, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')
	
@app.route('/staffregAuth', methods=['GET', 'POST'])
def staffregAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	airline = request.form['airline']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airlinestaff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_staff.html', error = error)
	else:
		ins = 'INSERT INTO airlinestaff VALUES(%s, %s, %s)'
		cursor.execute(ins, (username, password, airline))
		conn.commit()
		cursor.close()
		return render_template('index.html')
	
#login auth
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()

	# 고객 테이블에서 이메일과 비밀번호 확인
	cursor.execute("SELECT * FROM customer WHERE email=%s AND password=%s", (username, password))
	customer = cursor.fetchone()

	if customer:
		session['username'] = username
		return redirect('/customer_dashboard')  # 고객용 대시보드로 리다이렉트
	else:
		# 직원 테이블에서 사용자명과 비밀번호 확인
		cursor.execute("SELECT * FROM airlinestaff WHERE username=%s AND password=%s", (username, password))
		staff = cursor.fetchone()

		if staff:
			# 세션에 직원 정보 저장
			session['username'] = username
			#airline도 
			session['airline_name'] = staff['airline_name']
			return redirect('/staff_dashboard')  # 직원용 대시보드로 리다이렉트
		else:
			error = 'Invalid email/username or password'
			return render_template('login.html', error=error)

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'username' in session:
        return render_template('customer_dashboard.html', username = session['username'])
    else:
        return redirect('/login')


@app.route('/staff_dashboard')
def staff_dashboard():
	today = datetime.today().strftime('%Y-%m-%d')
	future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')


	if 'username' in session:
		cursor = conn.cursor()
		query = '''
		SELECT  flight.ID as flight_num, dep_date, dep_time, arr_date, arr_time, Airline_name, status
		FROM flight
		INNER JOIN airplane ON flight.Airplane_ID = airplane.ID
		WHERE Airline_name IN (
			SELECT airline_name 
			FROM airlinestaff
			WHERE username = %s  
		) and dep_date between %s and %s;
	'''
		cursor.execute(query, (session['username'],today, future_date))
		data = cursor.fetchall() 
		cursor.close()
		return render_template('staff_dashboard.html', username = session['username'],airline_name = session['airline_name'], flights=data)
	else:
		return redirect('/login')
	
#customer page
#view my flights
@app.route('/view_myflights', methods=['GET', 'POST'])
def view_myflights():
	today = datetime.today().strftime('%Y-%m-%d')
	future_date = (datetime.today() + timedelta(days = 180)).strftime('%Y-%m-%d')

	start_date = request.form.get('start_date',today)
	end_date = request.form.get('end_date',future_date)

	cursor = conn.cursor()
	query = '''
		SELECT  ticket.id as ticket_num, flight.ID as flight_num, dep_date, dep_time, arr_date, arr_time, status
		FROM flight INNER JOIN ticket
        where customer_email = %s
        and ticket.flight_id = flight.id
		and dep_date between %s and %s;

	'''
	cursor.execute(query, (session.get('username'),start_date, end_date))
	data = cursor.fetchall() 
	cursor.close()
	return render_template('myflight.html', username = session['username'], flights=data)

#book a flight
@app.route('/get_flights', methods=['GET', 'POST'])
def get_flights():
	dep_airport = request.args.get('dep_airport')
	arr_airport = request.args.get('arr_airport')
	dep_date = request.args.get('dep_date')
	return_date = request.args.get('return_date',None)
	print(return_date)

	cursor = conn.cursor()
	query1 = '''
			SELECT  flight.ID as flight_num, dep_date, dep_time, arr_date,arr_time, Airline_name
			FROM flight, airplane 
			WHERE Airplane_ID = airplane.ID 
			AND dep_airport = %s 
			AND arr_airport = %s 
			AND dep_date = %s;'''	
	cursor.execute(query1, (dep_airport, arr_airport, dep_date)) 
	data1 = cursor.fetchall()
	
	
	if return_date and return_date != '':
		query2 = '''
        SELECT  flight.ID as flight_num, dep_date, dep_time, arr_date, arr_time, Airline_name
        FROM flight, airplane 
        WHERE Airplane_ID = airplane.ID 
        AND dep_airport = %s 
        AND arr_airport = %s 
        AND dep_date = %s;'''
		cursor.execute(query2, (arr_airport, dep_airport , return_date)) 
		data2 = cursor.fetchall()
		cursor.close()
		return render_template('book_ticket.html', dep_airport=dep_airport, arr_airport=arr_airport, dep_date=dep_date, 
							return_date=return_date, flights=data1, flights2=data2, username=session['username'])

	else: 
		cursor.close()
		return render_template('book_ticket.html', dep_airport=dep_airport, arr_airport=arr_airport, dep_date=dep_date, 
							return_date=return_date, flights=data1, username=session['username'])
#book button
@app.route('/book_clicked', methods=['GET', 'POST'])
def book_clicked():
	flight_id = request.args.get('flight_num')

	cursor = conn.cursor()
	query = '''SELECT 
				CASE
					WHEN (COUNT(ticket.id) / seats) >= 0.7 THEN 1.25 * baseprice
					ELSE baseprice
				END AS price
			FROM flight
			INNER JOIN airplane ON flight.airplane_id = airplane.id
			LEFT JOIN ticket ON flight.id = ticket.flight_id
			WHERE flight.id = %s 
			GROUP BY flight.id;'''
	cursor.execute(query, (flight_id))
	data = cursor.fetchall() 
	price = int(data[0].get('price', None))

	conn.commit()
	cursor.close()

	return render_template('checkout.html',flight_id = flight_id, price = price)

#after selecting ticket
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	flight_id = request.form['flight_id']
	price = request.form['price']
	customer_email = session['username']
	fname = request.form['fname']
	lname = request.form['lname']
	dob = request.form['dob']
	card_type = request.form['card_type']
	card_num = request.form['card_num']
	exp_date = request.form['exp_date']
	purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print((flight_id, customer_email, fname, lname, dob, card_type, card_num, exp_date, purchase_date))
	
	cursor = conn.cursor()
	ins = '''INSERT INTO ticket (flight_id, customer_email, fname, lname, dob, price, card_type, card_num, exp_date, purchase_date) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

	cursor.execute(ins, (flight_id, customer_email, fname, lname, dob, price, card_type, card_num, exp_date, purchase_date) )
	conn.commit()
	cursor.close()
	return render_template('checkout.html')

#define route for my flights
@app.route('/my_flights', methods=['GET', 'POST'])
def my_flights():
	return redirect(url_for('view_myflights'))



#cancel page
@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
	#only cancellable that is after 24hours from now
	cursor = conn.cursor()
	query = """SELECT  ticket.id as ticket_id, flight.ID as flight_num, dep_date, dep_time, arr_date, arr_time, fname, lname
		FROM flight INNER JOIN ticket
        where customer_email = %s
        and ticket.flight_id = flight.id
		and TIMESTAMP(dep_date, dep_time) > NOW() + INTERVAL 24 HOUR;"""
	cursor.execute(query,session['username'])
	data = cursor.fetchall() 
	cursor.close()
	return render_template('cancel.html', username = session['username'], tickets=data)

#cancel ticket  아아ㅏ아아아작동안대
@app.route('/cancel_confirm', methods=['GET', 'POST'])
def cancel_confirm():
	ticket_id = request.args.get('ticket_num')
	print(ticket_id)
	cursor = conn.cursor()
	query = "delete from ticket where id = %s;"
	cursor.execute(query,(ticket_id))
	conn.commit()
	cursor.close()
	return "Your ticket is canceled"

#rating cancel 이랑 똑같이 

#log out	
@app.route('/logout')
def index():
	session['username']=None
	return render_template('login.html')

#staff page
#view flights
@app.route('/view_flights', methods=['GET', 'POST'])
def view_flights():
	today = datetime.today().strftime('%Y-%m-%d')
	future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')

	dep_airport = request.form.get('dep_airport')
	arr_airport = request.form.get('arr_airport')
	start_date = request.form.get('start_date')
	end_date = request.form.get('end_date')

	if not start_date:
		start_date = today

	if not end_date:
		end_date = future_date

	cursor = conn.cursor()
	query = '''
		SELECT  flight.ID as flight_num, dep_date, dep_time, arr_date, arr_time, status, Airline_name
		FROM flight
		INNER JOIN airplane ON flight.Airplane_ID = airplane.ID
		WHERE Airline_name IN (
			SELECT airline_name 
			FROM airlinestaff
			WHERE username = %s and
			dep_date BETWEEN %s AND %s
		)
	'''
	params = (session.get('username'),start_date, end_date,)

	if dep_airport and arr_airport :
		query += 'AND dep_airport = %s AND arr_airport = %s;'
		params += (dep_airport, arr_airport)
	else:
		query += ';'

	cursor.execute(query, params)

	data = cursor.fetchall() 
	cursor.close()
	return render_template('staff_dashboard.html', username = session['username'], airline_name = session['airline_name'], flights=data)

#view customers of a particular flight
@app.route('/view_customers', methods=['GET', 'POST'])
def view_customers():
	flight_num = request.args.get('flight_num')

	cursor = conn.cursor()

	query = """SELECT fname, lname, email FROM customer
				WHERE email IN ( SELECT Customer_email FROM ticket
								WHERE flight_id = %s);"""
	
	cursor.execute(query, (flight_num))
	customers = cursor.fetchall()

	cursor.close()
	return render_template('view_customers.html', customers=customers)

#view airplanes
@app.route('/view_airplanes', methods=['GET', 'POST'])
def view_airplanes():
	
	cursor = conn.cursor()
	query = '''
		SELECT ID,seats, manufacturing_company, model_num, manufacturing_date, age
		FROM airplane
		WHERE Airline_name IN (
			SELECT airline_name 
			FROM airlinestaff
			WHERE username = %s
		);
	'''
	cursor.execute(query, session['username'])

	data = cursor.fetchall() 
	cursor.close()
	return render_template('view_airplanes.html', username = session['username'], airplanes=data)

#create flight
@app.route('/create_flights_clicked')
def create_flights_clicked():
	return render_template('create_flights.html',airline_name = session['airline_name'])

@app.route('/create_flights', methods=['GET', 'POST'])
def create_flights():
	flight_num = request.form['flight_num']
	dep_airport = request.form['dep_airport']
	dep_date = request.form['dep_date']
	dep_time = request.form['dep_time']
	arr_airport = request.form['arr_airport']
	arr_date = request.form['arr_date']
	arr_time = request.form['arr_time']
	base_price = request.form['base_price']
	status = request.form['status']
	airplane = request.form['airplane']

	cursor = conn.cursor()

	ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (flight_num,dep_airport,dep_date,dep_time,
					  arr_airport,arr_date,arr_time,base_price,status,airplane))
	conn.commit()
	cursor.close()
	return redirect(url_for('view_flights'))
#change status
@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
	id = request.args.get('flight_num')
	print(id)
	cursor = conn.cursor()
	ins = '''
		UPDATE flight
		SET status =
			CASE
				WHEN status = 'delayed' THEN 'on-time'
				ELSE 'delayed'
			END
		WHERE ID = %s;'''

			
	cursor.execute(ins,(id))
	conn.commit()
	cursor.close()
	return redirect(url_for('view_flights'))

#add airplane
@app.route('/add_airplane_clicked')
def add_airplane_clicked():
	return render_template('add_airplane.html')

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	id = request.form['id']
	seats = request.form['seats']
	airline_name = request.form['airline_name']
	manufacturing_company = request.form['manufacturing_company']
	model_num = request.form['model_num']
	manufacturing_date = request.form['manufacturing_date']
	age = request.form['age']

	if airline_name != session['airline_name']:
		return "You are not authorized to add airplanes for this airline."
	
	cursor = conn.cursor()

	ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (id,seats,airline_name,manufacturing_company,model_num,manufacturing_date,age))
	conn.commit()
	cursor.close()
	return redirect(url_for('view_airplanes'))

#add airport
@app.route('/add_airport_clicked')
def add_airport_clicked():
	return render_template('add_airport.html')
@app.route('/view_airport', methods=['GET', 'POST'])
def view_airport():
    cursor = conn.cursor()
    query = '''
        SELECT code, name, city, country, terminal, type
        FROM airport;
    '''
    cursor.execute(query)

    data = cursor.fetchall()
    cursor.close()
    return render_template('view_airport.html', username=session['username'], airports=data)


@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	code = request.form['code']
	name = request.form['name']
	city = request.form['city']
	country = request.form['country']
	terminal = request.form['terminal']
	airport_type = request.form['type']

	cursor = conn.cursor()
	ins = 'INSERT INTO airport (code, name, city, country, terminal, type) VALUES (%s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (code, name, city, country, terminal, airport_type))
	conn.commit()
	cursor.close()

	return redirect(url_for('view_airport'))



	
	

		
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
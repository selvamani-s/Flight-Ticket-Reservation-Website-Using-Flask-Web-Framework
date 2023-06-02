from flask import Flask,flash,redirect,render_template,session,request,url_for
# import mysql.connector
import sqlite3
import flightTicket

app = Flask(__name__)
app.secret_key = '123'

# mydb = mysql.connector.connect(host='localhost',user='selvamani',passwd='selv@maniS2002',database='selvamani')
mydb = sqlite3.connect('database.db')
mycur = mydb.cursor()
mycur.execute("create table if not exists customer(name varchar(50), email varchar(50) unique,password varchar(50));")
mydb.close()

@app.route("/",methods = ['GET','POST'])
def index():
    return render_template("login.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # mydb = mysql.connector.connect(host='localhost',user='selvamani',passwd='selv@maniS2002',database='selvamani')
        mydb = sqlite3.connect('database.db')
        mycur = mydb.cursor()
        mycur.execute('SELECT * FROM customer WHERE email=? AND password=?;',(email,password))
        data = mycur.fetchone()
        print(data)
        print(type(data))
        if data:
            session['name']=data[0]
            print(session['name'])
            flash('Login Successfully!','success')
            return redirect("base")
        else:
            flash("Username and Password are Mismatch",'danger')

    return redirect(url_for('index'))

@app.route("/base")
def base():
    return render_template("base1.html")

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            # mydb = mysql.connector.connect(host='localhost',user='selvamani',\
                                        #    passwd='selv@maniS2002',database='selvamani')
            mydb = sqlite3.connect('database.db')
            mycur = mydb.cursor()
            mycur.execute('INSERT INTO customer VALUES (?,?,?);',(name,email,password))
            mydb.commit()
            flash("Sign Up Successfully!","success")
        except:
            print("Error insert into database")
            flash("Error in insert operation",'danger')
        finally:
            mydb.close()
            return redirect(url_for("login"))
            
    return render_template("signup.html")

@app.route("/logout")
def logout():
    flash("Logout Successfully",'success')
    return redirect(url_for("index"))

@app.route("/booking", methods = ['GET','POST'])
def booking():
    return render_template("booking.html", flightname = flight_dict)


@app.route('/booking2',methods = ['GET','POST'])
def booking2():
    if request.method == "POST":
        global flight_ID
        flightid = int(request.form.get('flightid'))
        No_of_ticket = int(request.form.get('Noofticket'))
        flight_ID = flightid
        print("integer flight id is",int(flightid))
        if (flight_ID == 0 or flight_ID == 1 ) and (No_of_ticket <= flight_details[flight_ID].Available_Ticket):
            flight_details[int(flight_ID)].booking(flight_ID,No_of_ticket)
            Index = flight_details[flight_ID].PassengerID_arr.index( flight_details[flight_ID].PassengerID )
            saving_details = {
                "currentFlight" : flight_ID,
                "passengerId": flight_details[flight_ID].PassengerID,
                "require_ticket" : No_of_ticket,
                "totalAmount" : flight_details[flight_ID].cost_arr[Index]
            }
            flash('Ticket Booked Successfully!','success')
            return render_template('booking2.html',Available_Ticket = flight_details[flight_ID].Available_Ticket , \
                                   currentAmount = flight_details[flight_ID].currentAmount,\
                                      details = saving_details)
        else:
            flash("Please Enter the correct Flight ID or No of ticket should be <=50 ","danger")
    else:
        print("not yet get booking2 POst methods")
    
    return redirect(url_for('booking'))

@app.route("/cancel")
def cancel():
    return render_template('cancel.html',flightname = flight_dict)

@app.route('/cancel2',methods = ['GET','POST'])
def cancel2():
    if request.method == "POST":
        global flight_ID
        cancel_flight_id = int(request.form.get('flightid'))
        flight_ID = cancel_flight_id
        if cancel_flight_id >= 2:
            flash("Please Enter the Correct Flight ID Not > 2",'danger')
            return render_template('cancel.html',flightname = flight_dict)
        else:
            passengerID_arr = flight_details[cancel_flight_id].PassengerID_arr
            flightID_arr = flight_details[cancel_flight_id].FlightID
            No_of_ticket_arr = flight_details[cancel_flight_id].require_ticket
            length = len(passengerID_arr)
            return render_template('cancel2.html',passengerID_arr = passengerID_arr,\
                                flightID_arr=flightID_arr,No_of_ticket_arr=No_of_ticket_arr, \
                                    length = length)
            
    return redirect(url_for('cancel'))

@app.route("/cancel3",methods = ['GET','POST'])
def cancel3():
    if request.method == 'POST':
        cancel_passenger_id = int(request.form.get('passengerid'))
        if cancel_passenger_id not in flight_details[flight_ID].PassengerID_arr:
            flash("Passenger ID not found Please Enter correct Passenger ID",'danger')
            return render_template('cancel.html',flightname = flight_dict)
        else:
            removeIndex = flight_details[flight_ID].PassengerID_arr.index(cancel_passenger_id)
            refund_amount = flight_details[flight_ID].cost_arr[removeIndex]
            flight_details[flight_ID].cancel(cancel_passenger_id)
            flash("Ticket Cancel Successfully!",'success')
            return render_template('cancel3.html',refund_amount = refund_amount)
    return redirect(url_for('cancel'))

@app.route('/display')
def display():
    return render_template('display.html',flightname = flight_dict)

@app.route('/display2',methods = ['GET','POST'])
def display2():
    if request.method == 'POST':
        global flight_ID
        flightid = int(request.form.get('flightid'))
        flight_ID = flightid 
        if flightid >=2:
            flash("Enter correct Flight ID (0 or 1)",'danger')
            return redirect(url_for('display'))
        passengerID_arr = flight_details[flight_ID].PassengerID_arr
        flightID_arr = flight_details[flight_ID].FlightID
        No_of_ticket_arr = flight_details[flight_ID].require_ticket
        Available_Ticket = flight_details[flight_ID].Available_Ticket 
        currentAmount = flight_details[flight_ID].currentAmount
        length = len(passengerID_arr)
            
        if len(flight_details[flight_ID].PassengerID_arr) == 0:
            flash('No Records Found!','warning')
            return render_template('display2.html',Available_Ticket = Available_Ticket,currentAmount = currentAmount,\
                passengerID_arr = passengerID_arr,flightID_arr = flightID_arr,No_of_ticket_arr = No_of_ticket_arr, \
                length = length)
        else:
            return render_template("display2.html", Available_Ticket = Available_Ticket,currentAmount = currentAmount,\
            passengerID_arr = passengerID_arr,flightID_arr = flightID_arr,No_of_ticket_arr = No_of_ticket_arr, \
            length = length)

if __name__ == "__main__":
    global flight_ID 
    flight_ID = None
    flight_details = []
    flight_dict = {0:"Indigo",
                   1:"Air India"}
    for i in flight_dict.values():
        i = flightTicket.FlightTicket()
        flight_details.append(i)
    app.run(debug=True)
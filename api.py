from flask import jsonify, Flask, request, render_template
from flask_cors import CORS
from datetime import datetime, timedelta
import pymysql

# MySQL configurations
app = Flask(__name__)
CORS(app)
app.config['MYSQL_DATABASE_USER'] = 'dbuser'
app.config['MYSQL_PASSWORD'] = 'dbpass'
app.config['MYSQL_DB'] = 'db'
app.config['MYSQL_HOST'] = 'localhost'

# These credentials are only useful on the database server, which is only accessible over the air by this api

# This API Utilises the CRUD method for data management

#Create

@app.route('/api/newVehicle', methods=['POST'])
def createVehicle():
    connection = None
    try:
        data = request.json
        vin = data["vin"]
        year = data["year"]
        color = data["color"]
        mileage = data["mileage"]
        make = data["make"]
        model = data["model"]
        typee = data["type"]
        mpg_city = data["mpg-city"]
        mpg_hwy = data["mpg-hwy"]
        msrp = data["msrp"]
        photos = data.get("photos", [])
        features = data.get("features", [])

        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (vin, year, color, mileage, make, model, typee, mpg_city, mpg_hwy, msrp))
            
            for photo in photos:
                cursor.execute("INSERT INTO vehicle_photos (vehicle_vin, photo) VALUES (%s, %s);", (vin, photo))

            for feature in features:
                cursor.execute("INSERT INTO vehicle_features (vehicle_vin, feature) VALUES (%s, %s);", (vin, feature))

        connection.commit()

        return jsonify({'success': 'Vehicle added successfully'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/newCustomer', methods=['POST'])
def createCustomer():
    connection = None
    try:
        # Parse JSON payload
        data = request.json
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        street_name = data.get("street_name")
        street_number = data.get("street_number")
        city = data.get("city")
        state = data.get("state")
        zip_code = data.get("zip_code")
        phone_numbers = data.get("phone_numbers", [])
        phone_types = data.get("phone_types", [])

        # Validate required fields
        if not email or not first_name or not last_name or not street_name or not street_number or not city or not state or not zip_code:
            return jsonify({'error': 'Missing required fields'}), 400

        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # Insert customer information into the database
            cursor.execute("INSERT INTO customer (email, first_name, last_name, street_name, street_number, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (email, first_name, last_name, street_name, street_number, city, state, zip_code))
            customer_id = cursor.lastrowid

            # Insert phone numbers with corresponding types
            for phone_number, phone_type in zip(phone_numbers, phone_types):
                cursor.execute("INSERT INTO customer_phones (customer_id, phone_number, phone_type) VALUES (%s, %s, %s);", (customer_id, phone_number, phone_type))

        connection.commit()

        return jsonify({'success': 'Customer added successfully'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/newOrder', methods=['POST'])
def createOrder():
    connection = None
    try:
        data = request.json
        vin = data["vin"]
        customer_id = data["customer_id"]
        street_name = data["street_name"]
        street_number = data["street_number"]
        apartment_number = data["apartment_number"]
        city = data["city"]
        state = data["state"]
        zipcode = data["zip"]

        current_date = datetime.now().date()
        current_time = datetime.now().time()

        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer WHERE id = %s;", (customer_id,))
            customerExists = cursor.fetchone()
            cursor.execute("SELECT * FROM vehicle WHERE vin = %s;", (vin,))
            vehicleExists = cursor.fetchone()
            
            if customerExists and vehicleExists:
                try:
                    cursor.execute("INSERT INTO orders (customer_id, vehicle_vin, street_name, street_number, apartment_number, city, state, zip, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (customer_id, vin, street_name, street_number, apartment_number, city, state, zipcode, current_date, current_time))
                except Exception as e:
                    print("Error:", e)
                    return jsonify({'error': 'Internal Server Error'}), 500

            else:
                return jsonify({'error': 'Vehicle or Customer not found'}), 404
            
        connection.commit()
        return jsonify({'success': 'Order made successfully'}), 200
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    
    finally:
        if connection:
            connection.close()

#Read

@app.route('/api/getAllVehicles')
def getVehicles():
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicle;")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/getVehicle/<vin>')
def getVehicle(vin):
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicle WHERE vin = %s;", (vin,))
            rows = cursor.fetchone()
            if rows:
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                return jsonify({'error': 'Vehicle not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/getVehicleFeatures/<vin>')
def getVehicleFeatures(vin):
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT feature FROM vehicle_features WHERE vehicle_vin = %s;", (vin,))
            rows = cursor.fetchall()
            if rows:
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                return jsonify({'error': 'Features not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/getVehiclePhotos/<vin>')
def getVehiclePhotos(vin):
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT photo FROM vehicle_photos WHERE vehicle_vin = %s;", (vin,))
            rows = cursor.fetchall()
            if rows:
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                return jsonify({'error': 'Features not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

#Maybe combine getVehicle, getVehicleFeatures, and getVehiclePhotos
@app.route('/api/getCustomer/<id>')
def getCustomer(id):
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer WHERE id = %s;", (id,))
            rows = cursor.fetchone()
            if rows:
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                return jsonify({'error': 'Customer not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/getAllCustomers')
def getCustomers():
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer;")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/getOrder/<id>')
def getOrder(id):
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE id = %s;", (id,))
            row = cursor.fetchone()
            if row:
                row['date'] = str(row['date'])
                row['time'] = str(row['time'])
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/getAllOrders')
def getOrders():
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orders;")
            rows = cursor.fetchall()
            for row in rows:
                row['date'] = str(row['date'])
                row['time'] = str(row['time'])
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

#Update

#UpdateCustomerPhoneNumber
#UpdateCustomerAddress
#UpdateVehicle
#UpdateOrder

#Delete

@app.route('/api/deleteVehicle/<vin>')
def deleteVehicle(vin):
    connection = None
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicle WHERE vin = %s;", (vin,))
            rows = cursor.fetchone()
            if rows:
                try:
                    cursor.execute("DELETE FROM vehicle_features WHERE vehicle_vin = %s;", (vin,))
                    cursor.execute("DELETE FROM vehicle_photos WHERE vehicle_vin = %s;", (vin,))
                    cursor.execute("DELETE FROM vehicle WHERE vin = %s;", (vin,))
                    connection.commit()
                    return jsonify({'success': 'Vehicle removed successfully'}), 200
                except Exception as e:
                    print("Error:", e)
                    return jsonify({'error': 'Internal Server Error'}), 500
            else:
                return jsonify({'error': 'Vehicle not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        if connection:
            connection.close()

#Delete Customer
#Delete Order

#Base endpoints

@app.route('/')
def welcome():
    return render_template('index.html'), 200
    # return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(host='192.168.50.138', port=5004)
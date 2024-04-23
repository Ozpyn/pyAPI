from flask import jsonify, Flask, request, render_template
from flask_cors import CORS
from datetime import datetime, timedelta
import pymysql
import requests

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

@app.route('/api/newOwner', methods=['POST'])
def createOwner():
    connection = None
    try:
        data = request.json
        vehicle_vin = data["vin"]
        customer_id = data["customer_id"]

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
            cursor.execute("SELECT * FROM vehicle WHERE vin = %s;", (vehicle_vin,))
            vehicleExists = cursor.fetchone()
            
            if customerExists and vehicleExists:
                try:
                    cursor.execute("INSERT INTO `ownership` VALUES (%s, %s);", (customer_id, vehicle_vin))
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

#getVehicleDetails combines getVehicle, getVehicleFeatures, and getVehiclePhotos.
# hopefully to reduce the number of api calls
@app.route('/api/getVehicleDetails/<vin>')
def getVehicleDetails(vin):
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
            # Fetch vehicle details
            cursor.execute("SELECT * FROM vehicle WHERE vin = %s;", (vin,))
            vehicle_data = cursor.fetchone()
            if not vehicle_data:
                return jsonify({'error': 'Vehicle not found'}), 404

            # Fetch vehicle features if available
            cursor.execute("SELECT feature FROM vehicle_features WHERE vehicle_vin = %s;", (vin,))
            features_data = [row['feature'] for row in cursor.fetchall()]

            # Fetch vehicle photos if available
            cursor.execute("SELECT photo FROM vehicle_photos WHERE vehicle_vin = %s;", (vin,))
            photos_data = [row['photo'] for row in cursor.fetchall()]

            # Combine data into a single response
            vehicle_details = {
                "vin": vehicle_data['vin'],
                "year": vehicle_data['year'],
                "color": vehicle_data['color'],
                "mileage": vehicle_data['mileage'],
                "make": vehicle_data['make'],
                "model": vehicle_data['model'],
                "type": vehicle_data['type'],
                "mpg-city": vehicle_data['mpg-city'],
                "mpg-hwy": vehicle_data['mpg-hwy'],
                "msrp": vehicle_data['msrp'],
            }

            # Add photos and features if available
            if photos_data:
                vehicle_details["photos"] = photos_data
            if features_data:
                vehicle_details["features"] = features_data

            resp = jsonify(vehicle_details)
            resp.status_code = 200
            return resp

    except Exception as e:
        print("Error:", e)  # Debug print statement
        return jsonify({'error': str(e)}), 500  # Return the actual error message
    finally:
        if connection:
            connection.close()


# searchForVehicles searches for vehicles based on user inputted search
# Use the searchQuery from the URL 
@app.route('/api/searchForVehicles')
def searchForVehicles():
    connection = None
    try:
        search_query = request.args.get('q')

        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:

            # Query to retreive the vins of each vehicle
            sql_query_for_vehicle_vins = ("SELECT vin FROM vehicle WHERE make LIKE %s OR model LIKE %s;")
            cursor.execute(sql_query_for_vehicle_vins, ('%' + search_query + '%', '%' + search_query + '%'))
            vin_data = cursor.fetchall()
            vins = [row['vin'] for row in vin_data]

            search_results = []

            # Iterate over each vin
            for vin in vins:
                # Use getVehicleDetails enpoint to retreive all vehicle details of each vin
                vehicle_response = requests.get(f"http://174.104.199.92:5004/api/getVehicleDetails/{vin}")

                if vehicle_response.status_code == 200:
                    vehicle_details = vehicle_response.json()
                    search_results.append(vehicle_details) 

            # Check if no vehicles found
            if not search_results:
                return jsonify({'error': 'Vehicles not found'}), 404

            resp = jsonify(search_results)
            resp.status_code = 200
            return resp

    except Exception as e:
        print("Error:", e)  # Debug print statement
        return jsonify({'error': str(e)}), 500  # Return the actual error message
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

@app.route('/api/getAllOwnership')
def getAllOwnership():
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
            cursor.execute("SELECT * FROM ownership;")
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

@app.route('/api/getOwnership/<customer_id>')
def getOwnership(customer_id):
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
            cursor.execute("SELECT id, vehicle_vin FROM ownership where customer_id = %s;", (customer_id,))
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
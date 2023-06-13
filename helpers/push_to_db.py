import psycopg2
import configparser

# importing details from config.ini
config = configparser.ConfigParser()
config.read('configuration\config_db.ini')  # reading the config file
host = config.get('postgresql', 'host')  # getting host id
database = config.get('postgresql','database')
user = config.get('postgresql','user')
password_db = config.get('postgresql','password')
port = config.get('postgresql', 'port')  # getting port number

############## url table code
def write(name, url, boo,site_type): # Write to URL Table
    try:
        # connect to the database
        conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
        # create a cursor object
        cur = conn.cursor()
        # create a table
        cur.execute("CREATE TABLE IF NOT EXISTS URLtable (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, url VARCHAR NOT NULL, is_active BOOLEAN DEFAULT true, site_type VARCHAR)")
        cur.execute(
            "INSERT INTO URLtable (name, url, is_active, site_type) VALUES (%s,%s,%s,%s)", (name, url, boo,site_type))
        # commit the changes
        conn.commit()
        # close the cursor and connection
        cur.close()
        conn.close()
        return "Added to database successfully."
    except Exception as e:
        return "Not able to write to DB due to "+str(e)


def del_db(id): # Delete from URL Table
    # connect to the database
    try:
        conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
        cur = conn.cursor()
        query = "DELETE FROM URLtable WHERE id = %s"
        cur.execute(query, (id,))
        conn.commit()
        cur.close()
        conn.close()
        return 'Success'+id
    except Exception as e:
        return e

def updates(id, name, url, boo,site_type): # Update URL Table
    try:
        # connect to the database
        conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
        # create a cursor object
        cur = conn.cursor()

        # create a table
        cur.execute("CREATE TABLE IF NOT EXISTS URLtable (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, url VARCHAR NOT NULL, is_active BOOLEAN DEFAULT true, site_type VARCHAR)")
        cur.execute(
            "UPDATE URLtable SET name= %s, url=%s, is_active=%s, site_type =%s WHERE id= %s", (name, url, boo, site_type, id ))
        # commit the changes
        conn.commit()

        # close the cursor and connection
        cur.close()
        conn.close()
        return "Added to database successfully."
    except Exception as e:
        return "Not able to write to DB due to "+str(e)

def get_db(): # Fetch data from URL Table
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS URLtable (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, url VARCHAR NOT NULL, is_active BOOLEAN DEFAULT true, site_type VARCHAR)")
    # execute the SQL query
    cur.execute("SELECT id,name, url, is_active, site_type FROM URLtable")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def get_Url_name_db(id): # Fetch data from URL Table for specific id
    # connect to the database
        # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS URLtable (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, url VARCHAR NOT NULL, is_active BOOLEAN DEFAULT true, site_type VARCHAR)")
    # execute the SQL query
    cur.execute("SELECT name, url FROM URLtable where id=%s",(id,))
    # fetch all rows
    rows = cur.fetchone()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

############################# SSL Table db code #########################################
def get_ssl1_db(id): # Fetch secific data from ssl table for specific url 
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SSL_table (id SERIAL PRIMARY KEY, SSL_expiry VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    # execute the SQL query
    cur.execute("SELECT SSL_expiry,  URL_id FROM SSL_table where URL_id = %s",(id,))
    # fetch all rows
    rows = cur.fetchone()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def get_ssl_db(): # Get all data from SSL Table
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SSL_table (id SERIAL PRIMARY KEY, SSL_expiry VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    # execute the SQL query
    cur.execute("SELECT SSL_expiry,  URL_id FROM SSL_table")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def update_ssl_db(ss,url_id): # Update SSL Table
    try:
        # connect to the database
        conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
        # create a cursor object
        cur = conn.cursor()
        # create a table
        cur.execute("CREATE TABLE IF NOT EXISTS SSL_table (id SERIAL PRIMARY KEY, SSL_expiry VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
        cur.execute(
            "UPDATE SSL_table SET SSL_expiry= %s, WHERE URL_id= %s", (ss, url_id ))
        # commit the changes
        conn.commit()
        # close the cursor and connection
        cur.close()
        conn.close()
        return "Uppdated to database successfully."
    except Exception as e:
        return "Not able to write to DB due to "+str(e)
    
def write_to_ssl_db(ssl,url_id): # Write in SSL Table
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SSL_table (id SERIAL PRIMARY KEY, SSL_expiry VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    # execute the SQL query
    cur.execute(
            "INSERT INTO SSL_table ( SSL_expiry,URL_id) VALUES (%s,%s)", (ssl,  url_id))
    # commit the changes
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()
    return "Success"


################################ Status DB Code #########################
def get_status1_db(url_id):# get data from status db by id
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Status_table (id SERIAL PRIMARY KEY, Dead_Alive VARCHAR NOT NULL, recent_status_code INTEGER NOT NULL, status_code_updated_time INTEGER, last_checked_time INTEGER, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    # execute the SQL query
    cur.execute("SELECT Dead_Alive,recent_status_code, status_code_updated_time,last_checked_time FROM Status_table where  URL_id =%s",(url_id,))
    # fetch all rows
    rows = cur.fetchone()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def update_status_db(DA, code, time1, time2,url_id): # update status db by url id
    try:
        # connect to the database
        conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
        # create a cursor object
        cur = conn.cursor()

        # create a table
        cur.execute("CREATE TABLE IF NOT EXISTS Status_table (id SERIAL PRIMARY KEY, Dead_Alive VARCHAR NOT NULL, recent_status_code INTEGER NOT NULL, status_code_updated_time INTEGER, last_checked_time INTEGER, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
        cur.execute(
            "UPDATE Status_table SET Dead_Alive= %s, recent_status_code=%s, status_code_updated_time=%s, last_checked_time =%s WHERE URL_id= %s", (DA, code, time1, time2,url_id ))
        # commit the changes
        conn.commit()
        # close the cursor and connection
        cur.close()
        conn.close()
        return "Uppdated to database successfully."
    except Exception as e:
        return "Not able to write to DB due to "+str(e)

def get_status_db(): # get all data from status db
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Status_table (id SERIAL PRIMARY KEY, Dead_Alive VARCHAR NOT NULL, recent_status_code INTEGER NOT NULL, status_code_updated_time INTEGER, last_checked_time INTEGER, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    # execute the SQL query
    cur.execute("SELECT Dead_Alive,recent_status_code, status_code_updated_time,last_checked_time, URL_id FROM Status_table")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def write_to_status_db(DA, status_code, updated, checked,url_id): # write to status db
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Status_table (id SERIAL PRIMARY KEY, Dead_Alive VARCHAR NOT NULL, recent_status_code INTEGER NOT NULL, status_code_updated_time INTEGER, last_checked_time INTEGER, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    # execute the SQL query
    cur.execute(
            "INSERT INTO Status_table (Dead_Alive, recent_status_code, status_code_updated_time, last_checked_time, URL_id) VALUES (%s,%s,%s,%s,%s)", (DA,status_code, updated,checked, url_id))
    # commit the changes
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()
    return "Success"

##################### Server table codes ##################################################### 

def get_serverdb():# get all from server db
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS servertable (id SERIAL PRIMARY KEY, timestamp INTEGER, url VARCHAR NOT NULL, status_code VARCHAR NOT NULL,ssl_expiry VARCHAR, description VARCHAR)")
    # execute the SQL query
    cur.execute("SELECT url, status_code, ssl_expiry FROM servertable ORDER BY timestamp DESC")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def getalltime_serverdb(): # group by timestamp from serverdb
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS servertable (id SERIAL PRIMARY KEY, timestamp INTEGER, url VARCHAR NOT NULL, status_code VARCHAR NOT NULL,ssl_expiry VARCHAR, description VARCHAR)")
    # execute the SQL query
    cur.execute("SELECT timestamp FROM servertable GROUP BY timestamp")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def getcharttime_serverdb(): # fetching data from server table to make charts
    # connect to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS servertable (id SERIAL PRIMARY KEY, timestamp INTEGER, url VARCHAR NOT NULL, status_code VARCHAR NOT NULL,ssl_expiry VARCHAR, description VARCHAR)")
    # execute the SQL query
    cur.execute("SELECT timestamp, url, status_code FROM servertable ")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows

def write_to_server_db(t,url,res,exp,res_t):# Writing to server db
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    # create a table
    cur.execute("CREATE TABLE IF NOT EXISTS servertable (id SERIAL PRIMARY KEY, timestamp INTEGER, url VARCHAR NOT NULL, status_code VARCHAR NOT NULL,ssl_expiry VARCHAR, description VARCHAR)")
    cur.execute("INSERT INTO servertable (timestamp, url, status_code,ssl_expiry, description) VALUES (%s,%s,%s,%s, %s)",
                 (t,url,res,exp,res_t))
    # commit the changes
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()

############################# SSL Grade table ##############################

def write_ssl_grade_db(id,grade):# writing to sslgrade table
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    # create a table
    cur.execute("CREATE TABLE IF NOT EXISTS ssl_gradetable (id SERIAL PRIMARY KEY, url_grade VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    cur.execute("INSERT INTO ssl_gradetable (url_grade,URL_id) VALUES (%s,%s)",
                 (grade,id))
    # commit the changes
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()

def update_ssl_grade_db(id,grade): # Updating SSl grade table
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    # create a table
    cur.execute("CREATE TABLE IF NOT EXISTS ssl_gradetable (id SERIAL PRIMARY KEY, url_grade VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    cur.execute("UPDATE ssl_gradetable SET url_grade= %s where URL_id=%s",
                 (grade,id))
    # commit the changes
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()

def fetch_ssl_grade_db(): # Fetching data from SSL grade table
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password_db,
        port=port
    )
    # create a cursor object
    cur = conn.cursor()
    # create a table
    cur.execute("CREATE TABLE IF NOT EXISTS ssl_gradetable (id SERIAL PRIMARY KEY, url_grade VARCHAR NOT NULL, URL_id INTEGER,  FOREIGN KEY (URL_id) REFERENCES URLtable(id) ON DELETE CASCADE)")
    cur.execute("SELECT * from ssl_gradetable")
    # fetch all rows
    rows = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return rows
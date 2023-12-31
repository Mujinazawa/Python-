import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k = 30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt,'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256',b_pw,b_salt,1000).hex()
    return hashed_password

def insert_user(user_name, password):
    sql = 'INSERT INTO user_list VALUES(default, %s, %s, %s)'
    
    salt = get_salt()
    password = get_hash(password, salt)
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(user_name,password, salt))
        count = cursor.rowcount 
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
        
    finally :
        cursor.close()
        connection.close()
        
    return count    
        
def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM user_list WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, ))
        user = cursor.fetchone()

        if user != None:
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally :
        cursor.close()
        connection.close()    
    return flg


def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = 'SELECT id, title, author, publisher, pages FROM books_sample'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def insert_book(title, author, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = 'INSERT INTO books_sample VALUES (default, %s, %s, %s, %s)'
    
    cursor.execute(sql, (title, author, publisher, pages))
    
    connection.commit()
    cursor.close()
    connection.close()
       
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def insert_book(title, author, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO books_sample VALUES (default,%s, %s, %s, %s)"
    
    cursor.execute(sql,(title, author, publisher, pages))
    
    connection.commit()
    cursor.close()
    connection.close()

def delete_book(id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = 'DELETE FROM books_sample WHERE id = %s'

    cursor.execute(sql, (id,))

    connection.commit()
    cursor.close()
    connection.close()
    
def edit_book(id, title, author, publisher, pages):
    sql = 'UPDATE books_sample SET title=%s, author=%s, publisher=%s, pages=%s, WHERE id=%s;'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (title,author,publisher,pages,id))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count
db = {
    'user' : 'root',
    'password' : '1234',
    'host' : 'localhost',
    'port' : 3306,
    'database' : 'to_do_list'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
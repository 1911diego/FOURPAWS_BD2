import psycopg2

#Método que crea la conexión con PostgreSQL
def createConnection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='12345',
            database='fourPaws'
        )
        print("Conexión exitosa")
        return connection
    except Exception as ex:
        print(ex)
        return "No hay conexión"


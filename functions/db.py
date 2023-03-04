import pymysql.cursors
from config import DB_USER, DB_PASSWORD
def get_connect(database='bot'):
    return pymysql.connect(host='localhost',
                             user=DB_USER,
                             password=DB_PASSWORD,
                             database=database,
                             cursorclass=pymysql.cursors.DictCursor,
                            )


def sql(query:str, database='scraper', commit=False):
    try:
        with get_connect(database) as con:
            cursor = con.cursor()
            cursor.execute(query)

            if commit:
                con.commit()
                return True
            else:
                return cursor.fetchall()
                
    except Exception as ex:
        return False


def insert_into(table:str, **kwargs):

    params = [i for i in kwargs.keys()]
    values = [f'"{i}"' for i in kwargs.values()]

    query_params = ', '.join(params)
    query_values = ', '.join(values)

    if len(params) == len(values):
        
        return sql(f'''INSERT INTO `{table}`({query_params}) VALUES ({query_values})''', commit=True)
    print('Не соответствие в insert_into')
    return False














































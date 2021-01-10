import pymysql
import credentials


def create_connection():
    try:
        conn = pymysql.connect(host=credentials.Host,
                               port=credentials.Port,
                               user=credentials.User,
                               password=credentials.Passwd,
                               database=credentials.DB)
        print("Connected")
    except Exception as e:
        print("Error Connecting to DB")
        print(e)
    finally:
        return conn

def create_table(con,sql):
    try:
        myCursor = con.cursor()
        myCursor.execute(sql)
        con.commit()
        myCursor.close()
    except Exception as e:
        print(e)


def insert_table(con,table_name, **params):
    sql = ''' INSERT INTO {} VALUES('''.format(table_name)
    for param in params.values():
        sql += "'"+str(param) +"',"
    sql=sql[0:-1] + ");"
    results = query(con,sql)
    return results
    

def delete_item(con, table_name, **params):
    sql = ''' DELETE FROM {} WHERE '''.format(table_name)
    for column, param in params.items():
        sql += str(column) + "=" +"'"+str(param) +"' AND " 
    sql=sql[0:-4] + ";"
    results = query(con,sql)
    return results


def view_table(con, table_name):
    column_names = get_column_names(con,table_name)
    sql = """SELECT * FROM {}""".format(table_name)
    query_results = query(con, sql)
    return column_names,query_results


def view_selected_rows(con, table_name, id):
    column_names = get_column_names(con,table_name)
    sql = """SELECT * FROM {} WHERE id={}""".format(table_name, int(id))
    query_results = query(con, sql)
    return column_names,query_results


def get_column_names(con, table_name):
    sql = """select COLUMN_NAME
     from information_schema.columns
      where table_schema = 'project_db20_up1057600' 
      AND TABLE_NAME='{}' 
      order by table_name,ordinal_position""".format(
        table_name)
    query_results = query(con, sql)
    return query_results


def query(con, sql):
    results = tuple()
    try:
        myCursor = con.cursor()
        myCursor.execute(sql)
        results = myCursor.fetchall()
        #print(results)
        con.commit()
        myCursor.close()
    except Exception as e:
        print(e)
    finally:
        return results

def find_table_name(query):
    start_table_name = query.find("from") + 5
    table_name = query[start_table_name:]
    end_table_name = table_name.find(' ')
    if end_table_name == -1:
        pass
    else:
        table_name = table_name[0:end_table_name]
    return table_name

def get_table_names(conn):
    sql = """select table_name
            from information_schema.tables
            where TABLE_SCHEMA = 'project_db20_up1057600'
            order by table_schema, table_name """
    table_names = query(conn,sql)
    return table_names





#if __name__ == "__main__":
    #conn = create_connection()
    #get_insert_query(conn, "articles", id=11, name="asdfsdf", body="dsfsdaf")
    #get_column_names(conn, "articles")
    #create_table(conn)
    #insert_table(conn, "articles14",id=3)
    #delete_item(conn, "articles14", id=6)
    #x,y = view_table(conn, "ΕΠΙΣΚΕΨΗ")
    #print(x,y)
    #x,y = view_selected_rows(conn, "articles", 11)
    #print(x,y)
    # x,y=query2(conn,"articles","select * from articles")
    # print(x,y)

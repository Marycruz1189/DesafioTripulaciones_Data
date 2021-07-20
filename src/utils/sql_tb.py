import os,sys
import pandas as pd
    
path = os.path.dirname(__file__)
dir = os.path.dirname
src_path = dir(os.path.abspath(__file__))

import utils.tools as tools
from utils.mysql_driver import MySQL
import utils.mysql_driver as drv

def insert_sqlList (df_sql):
    # lectura de los datos de conexión a la base de datos y generación de las variables para conectarse
    json_readed = tools.read_json_to_dict("utils" + os.sep + "sql_settings.json")
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]

    # generación de la instancia de BDD y lanzamiento de conexión
    mysql_db = MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
    mysql_db.connect()

    # se generan los elementos necesarios para crear la tabla de la base de datos
    valores = df_sql.dtypes

    sql_create_columns = ""
    for i in range(len(valores)):
        row = drv.replace_guion(valores.index[i].upper()) + ' ' + drv.define_SQL_type(str(valores.values[i])) + ' NOT NULL,'
        sql_create_columns += row

    # Create table as per requirement
    # Erase table if exiting already 
    mysql_db.execute_interactive_sql(sql="DROP TABLE IF EXISTS miguel_barquero_delpozo")

    # Create the table to hold the data from the data set
    # Create the table with the columns automatically
    create_table_sql = f"""CREATE TABLE miguel_barquero_delpozo(
        ID INT(11) NOT NULL AUTO_INCREMENT,
        MOMENTO TIMESTAMP NOT NULL,
        {sql_create_columns}
        PRIMARY KEY (ID))"""

    mysql_db.execute_interactive_sql(sql=create_table_sql)

    # create the loop to insert automatically all the rows in the dataframe
    sql_insert_columns = ""
    for i in range(len(valores)):
        row =',' +  drv.replace_guion(valores.index[i].upper())
        sql_insert_columns += row

    for i in range (len (df_sql)):
        values_list = df_sql.iloc[i].to_list()
        sql_insert_values = ""
        for elem in values_list:
            sql_insert_values += ", '" + str(elem) + "'"

        insert_row_sql = f"""INSERT INTO miguel_barquero_delpozo 
        (MOMENTO{sql_insert_columns})
                    VALUES 
        (NOW(){sql_insert_values})"""

        mysql_db.execute_interactive_sql(sql=insert_row_sql)
    
    # cierre de la conexión a la base de datos
    mysql_db.close()

def get_data_sql (current_cols):
    # lectura de los datos de conexión a la base de datos y generación de las variables para conectarse
    json_readed = tools.read_json_to_dict("utils" + os.sep + "sql_settings.json")
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]

    # generación de la instancia de BDD y lanzamiento de conexión
    mysql_db = MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
    mysql_db.connect()
    list_ = mysql_db.execute_get_sql("SELECT * FROM miguel_barquero_delpozo")
    df_sql = pd.DataFrame(list_, columns= current_cols)
    
    # cierre de la conexión a la base de datos
    mysql_db.close()

    return df_sql

def insert_sqlModels (df_sql):
    # lectura de los datos de conexión a la base de datos y generación de las variables para conectarse
    json_readed = tools.read_json_to_dict("utils" + os.sep + "sql_settings.json")
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]

    # generación de la instancia de BDD y lanzamiento de conexión
    mysql_db = MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
    mysql_db.connect()

    # se generan los elementos necesarios para crear la tabla de la base de datos
    valores = df_sql.dtypes

    sql_create_columns = ""
    for i in range(len(valores)):
        row = drv.replace_guion(valores.index[i].upper()) + ' ' + drv.define_SQL_type(str(valores.values[i])) + ' NOT NULL,'
        sql_create_columns += row

    # Create table as per requirement
    # Erase table if exiting already 
    mysql_db.execute_interactive_sql(sql="DROP TABLE IF EXISTS model_comparison")

    # Create the table to hold the data from the data set
    # Create the table with the columns automatically
    create_table_sql = f"""CREATE TABLE model_comparison(
        ID INT(11) NOT NULL AUTO_INCREMENT,
        MOMENTO TIMESTAMP NOT NULL,
        {sql_create_columns}
        PRIMARY KEY (ID))"""

    mysql_db.execute_interactive_sql(sql=create_table_sql)

    # create the loop to insert automatically all the rows in the dataframe
    sql_insert_columns = ""
    for i in range(len(valores)):
        row =',' +  drv.replace_guion(valores.index[i].upper())
        sql_insert_columns += row

    for i in range (len (df_sql)):
        values_list = df_sql.iloc[i].to_list()
        sql_insert_values = ""
        for elem in values_list:
            sql_insert_values += ", '" + str(elem) + "'"

        insert_row_sql = f"""INSERT INTO model_comparison 
        (MOMENTO{sql_insert_columns})
                    VALUES 
        (NOW(){sql_insert_values})"""

        mysql_db.execute_interactive_sql(sql=insert_row_sql)
    
    # cierre de la conexión a la base de datos
    mysql_db.close()

def get_compmodels_sql (current_cols):
    # lectura de los datos de conexión a la base de datos y generación de las variables para conectarse
    json_readed = tools.read_json_to_dict("utils" + os.sep + "sql_settings.json")
    IP_DNS = json_readed["IP_DNS"]
    USER = json_readed["USER"]
    PASSWORD = json_readed["PASSWORD"]
    BD_NAME = json_readed["BD_NAME"]
    PORT = json_readed["PORT"]

    # generación de la instancia de BDD y lanzamiento de conexión
    mysql_db = MySQL(IP_DNS=IP_DNS, USER=USER, PASSWORD=PASSWORD, BD_NAME=BD_NAME, PORT=PORT)
    mysql_db.connect()
    list_ = mysql_db.execute_get_sql("SELECT * FROM model_comparison")
    df_sql = pd.DataFrame(list_, columns= current_cols)
    
    # cierre de la conexión a la base de datos
    mysql_db.close()

    return df_sql

if __name__ == '__main__':
    get_data_sql([])
import cx_Oracle
import config
import creacion_tablas
import sub1
import sub2
import sub4
import sqlscript


# Conexión con la base de datos
conn = cx_Oracle.connect(config.userid +'/'+ config.userid +'@'+ config.host +':1521/'+ config.service)

# Cursor para hacer transacciones
aux = conn.cursor()

# creacion_tablas.borrar_tablas(conn)

creacion_tablas.borrar_tablas(conn)
creacion_tablas.crear_tablas(conn)
creacion_tablas.insertar_tuplas_iniciales(conn)

print('Creando funcionalidades sql')
sqlscript.run_sql_script(conn, "plsqlsub1",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")

sqlscript.run_sql_script(conn, "plsqlsub2",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234"
                          edition_name="bof")

sqlscript.run_sql_script(conn, "plsqlsub3",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")
sqlscript.run_sql_script(conn, "plsqlsub4",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")

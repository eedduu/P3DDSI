import cx_Oracle
import config
import creacion_tablas
import sub4.py


# Conexión con la base de datos
conn = cx_Oracle.connect(config.userid +'/'+ config.userid +'@'+ config.host +':1521/'+ config.service)

# Cursor para hacer transacciones
aux = conn.cursor()

# creacion_tablas.borrar_tablas(conn)
creacion_tablas.crear_tablas(conn)
creacion_tablas.insertar_tuplas_iniciales(conn)

# Hasta salir del menú
while True:

    # Opción del menú
    print('##################################################')
    print('# Escoge una opción:                             #')
    print('# 1.Gestion de empleados                         #')
    print('# 2.Gestión de historiales médicos de pacientes  #')
    print('# 3.Gestión de inventario del hospital           #')
    print('# 4.Gestion de consultas                         #')
    print('# 5.Salir del programa                           #')
    print('##################################################')
    opc = int(input('\n Entrada: '))


    # Gestion de empleados
    if opc==1:
    	print('Funcionalidad en construccion (:')
    # Gestión de historiales médicos de pacientes
    elif opc==2:
    	print('Funcionalidad en construccion ):')
    # Gestión de inventario del hospital
    elif opc==3:
    	print('Funcionalidad en construccion D:')
    # Gestion de consultas
    elif opc==4:
    	sub4.menuConsulta()
    # Sale del menú
    elif opc==5:
    	break
    # Opcion no valida
    else:
    	print('Opcion no valida, vuelva a elegir.\n')

creacion_tablas.borrar_tablas(conn)

# Nos desconectamos 
print('Desconectandose de la bases de datos...')
conexion.close()
print('Se ha desconectado satisfactoriamente.\n')

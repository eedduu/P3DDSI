import cx_Oracle

def consultarStockMed(conexion, idMed):
    cursor = conexion.cursor()

    try:
        cant = cursor.callfunc('FUNCTION1', int ,[idMed])
        return cant
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)

def reservar_maquinas(conexion, idmaq, idconsulta):
    cursor = conexion.cursor()

    try:
        cursor.callproc('reservar_maquinas',(idmaq, idconsulta))
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)


def asignarMedicamentos(conexion, idmed, idtrat, cantidad):
    cursor = conexion.cursor()

    try:
        cursor.callproc('asignar_med',(idmed, idtrat, cantidad))
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)

def añadirStock(conexion, idmed, cantidad):
    cursor = conexion.cursor()

    try:
        cursor.callproc('añadirStock',(idmed, cantidad))
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)


def menuInventario(conexion):
    while True:
        # Opción del menú
       print('##################################################')
       print('# Escoge una opción:                             #')
       print('# 1.Consultar stock de un medicamento            #')
       print('# 2.Reservar maquinas para una consutla          #')
       print('# 3.Asignar medicamentos a un tratamiento        #')
       print('# 4.Añadir stock a un medicamento ya existente   #')
       print('# 5.Salir del subsistema                         #')
       print('##################################################')
       opc = int(input('\n Entrada: '))




       if opc==1:
           idMed = input('ID del medicamento: ')
           row = consultarStockMed(conexion, idMed)
           if (row!=None):
            print('La cantidad disponible del medicamento con identificador', idMed ,'es ', row)


       elif opc==2:
           idmaquina = input('ID de la maquina')
           idconsulta = input('ID de la consulta')
           reservar_maquinas(conexion, idmaquina, idconsulta)

       elif opc==3:
           id= input('ID del medicamento')
           idtrat= input('ID del tratamiento')
           cant=input('Cantidad del medicamento')
           asignarMedicamentos(conexion, id, idtrat, cant)

       elif opc==4:
           idmed = input('ID del medicamento')
           cantidad = input('Cantidad del medicamento')
           añadirStock(conexion, idmed, cantidad)
       elif opc==5:
           break

       else:
           print('Opcion no valida, vuelva a elegir')

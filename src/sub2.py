import cx_Oracle
import datetime

def addHistorial(conexion,dni,telefono,pya,gs,dniempleado):
    cursor = conexion.cursor()

    try:
        cursor.callproc('addHistorial',(dni,telefono,pya,gs,dniempleado))
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)

def modHistorial(conexion,dni,telefono,pya,gs):
    cursor = conexion.cursor()

    try:
        cursor.callproc('modHistorial',(dni,telefono,pya,gs))
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)


def getHistorial(conexion,dni):
    cursor = conexion.cursor()

    try:
        cursor.execute("select * from HistorialAsigna where DNIpaciente = (:1)", [dni])
        row = cursor.fetchone()
        return row
    except cx_Oracle.IntegrityError as error:
        print( (error.args[0].message).split('\n')[0] )
    except cx_Oracle.DatabaseError as error:
        print( (error.args[0].message).split('\n')[0] )
    except Error as error:
        print('ERROR desconocido')
        print(error)

def addTratamiento(conexion):
    cursor = conexion.cursor()
    idtratamiento   = input('ID del tratamiento: ')
    
    print('Fecha de inicio del tratamiento: \n')
    dia = int(input('   Día: '))
    mes = int(input('   Mes: '))
    anyo = int(input('   Año: '))
    fecha_correcta1 = True
    try:
    	fechaInicio = datetime.date(anyo,mes,dia).__str__()
    except:
        print("Fecha inválida.")
        fecha_correcta1 = False
	
    print('Fecha de fin del tratamiento: \n')
    dia = int(input('   Día: '))
    mes = int(input('   Mes: '))
    anyo = int(input('   Año: '))
    fecha_correcta2 = True
    try:
        fechaFinal = datetime.date(anyo,mes,dia).__str__()
    except:
        print("Fecha inválida.")
        fecha_correcta2 = False
    
    datos           = input('Información asociada al tratamiento: ')
    dniempleado     = input('DNI del médico que ha puesto el tratamiento: ')

    if (fecha_correcta1 and fecha_correcta2):
        try:
            cursor.callproc('addTratamiento',(idtratamiento,fechaInicio,fechaFinal,descripcion,empleado))
        except cx_Oracle.IntegrityError as error:
            print( (error.args[0].message).split('\n')[0] )
        except cx_Oracle.DatabaseError as error:
            print( (error.args[0].message).split('\n')[0] )
        except Error as error:
            print('ERROR desconocido')
            print(error)

def menuHistorial(conexion):

	while True:

       	 # Opción del menú
		print('##################################################')
		print('# Escoge una opción:                             #')
		print('# 1.Añadir un nuevo historial                    #')
		print('# 2.Modificar un historial                       #')
		print('# 3.Imprimir el historial                        #')
		print('# 4.Añadir tratamiento                           #')
		print('# 5.Salir del subsistema                         #')
		print('##################################################')
		opc = int(input('\n Entrada: '))


	    # Crear un nuevo historial de salud
		if opc==1:
			dni         = input('DNI del paciente: ')
			telefono    = int(input('Teléfono: '))
			pya         = input('Patologías y alergias: ')
			gs          = input('Grupo sanguíneo: ')
			dniempleado = input('DNI del médico de cabecera: ')
			addHistorial(conexion,dni,telefono,pya,gs,dniempleado)

	    # Modificación de un historial
		elif opc==2:
			dni         = input('DNI del paciente cuyo historial se quiere modificar: ')
			telefono    = input('Teléfono si se quiere modificar: ')
			pya         = input('Patologías y alergias si se quieren modificar: ')
			gs          = input('Grupo sanguíneo si se quieren modficar: ')
			print('Si quiere dejarlo como esta pulse intro')
			if (dni != ''):
                            historialant = getHistorial(conexion,dni)
                            if (telefono == ''):
                                telefono = historialant[1]
                            if (pya == ''):
                                pya = historialant[2]
                            if (gs == ''):
                                gs = historialant[3]

                            modHistorial(conexion,dni,telefono,pya,gs)
			else:
				print('Introduzca un DNI')

	
	    # Imprimir el historial 
		elif opc==3:
			dni = input('DNI del paciente asociado  al historial: ')
			row = getHistorial(conexion,dni)
			print('DNI: ',row[0])
			print('Telefono',row[1])
			print('Patologías y alergías: ',row[2])
			print('Grupo sanguíneo: ',row[3])
			print('DNI médico de cabecera: ',row[4])
        

	    	
	    # Añadir un tratamiento
		elif opc==4:
			addTratamiento(conexion)

	    # Sale del menú
		elif opc==5:
			break
	    # Opcion no valida
		else:
			print('Opcion no valida, vuelva a elegir.\n')




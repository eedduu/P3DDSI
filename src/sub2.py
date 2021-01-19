import cx_Oracle
import datetime

def addHistorial(conexion,dni,telefono,pya,gs,dniempleado):
    cursor = conexion.cursor()

    try:
        cursor.callproc('addHistorial',(dni,telefono,pya,gs,dniempleado))
    except cx_Oracle.IntegrityError as error:
        codigo = error.args[0].code
		
        if (codigo == 1):
            print('ERROR: Ya existe un historial asociado a ese DNI')
        else:
            print('ERROR desconocido')
            print(error)
    except cx_Oracle.DatabaseError as error:
        codigo = error.args[0].code
        if (codigo == 20101):
            print('ERROR: Grupo sanguíneo no válido')
        elif (codigo == 12899):
            print('ERROR: Mucho texto en el DNI o en patologías y algergias');
        else:
            print('ERROR desconocido')
            print(error)
    except Error as error:
        print('ERROR desconocido')
        print(error)


def modHistorial(conexion,dni,telefono,pya,gs,dniempleado):
    cursor = conexion.cursor()

    try:
        cursor.callproc('modHistorial',(dni,telefono,pya,gs))
    except cx_Oracle.IntegrityError as error:
        print('ERROR: No existe un historial con ese DNI')
    except cx_Oracle.DatabaseError as error:
        codigo = error.args[0].code
        if (codigo == 20101):
            print('ERROR: Grupo sanguíneo no válido')
        elif (codigo == 12899):
            print('ERROR: Mucho texto en el DNI o en patologías y algergias');
        else:
            print('ERROR desconocido')
            print(error)
    except Error as error:
        print('ERROR desconocido')
        print(error)


def getHistorial(conexion,dni):
    cursor = conexion.cursor()

    try:
       cursor.callproc('getHistorial',(dni))
    except cx_Oracle.IntegrityError as error:
        print('ERROR: No existe un historial asociado a ese DNI')
    return cursor.fetchone()


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
            codigo = error.args[0].code
	    	
            if (codigo == 1):
                print('ERROR: Ya existe un tratamiento asociado a ese código de tratamiento')
            else:
                print('ERROR desconocido')
                print(error)
        except cx_Oracle.DatabaseError as error:
            codigo = error.args[0].code
	    
            if (codigo == 12899):
                print('ERROR: Mucho texto en la descripcion del tratamiento');
            else:
                print('ERROR desconocido')
                print(error)
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
			telefono    = int(input('Teléfono si se quiere modificar: '))
			pya         = input('Patologías y alergias si se quieren modificar: ')
			gs          = input('Grupo sanguíneo si se quieren modficar: ')
			print('Si quiere dejarlo como esta pulse intro')
                
			if (dni != None):   
				historialant = getHistorial(conexion,dni)
                    
			if (telefono == None):
				telefono = historialant[1]
			if (pya == None):
				pya = historialant[2]
			if (gs == None):
				gs = historialant[3]
				
			modHistorial(conexion,dni,telefono,pya,gs)

	
	    # Imprimir el historial 
		elif opc==3:
			dni = input('DNI del paciente asociado  al historial: ')
			historial = getHistorial(conexion,dni)
			if (historial != None):
				telefono    = historial[1]
				pya         = historial[2]
				gs          = historial[3]
				dniempleado = historial[4]

				print('DNI: ',dni)
				print('Teléfono: ',str(telefono))
				print('Patologías y alergias: ',pya)
				print('DNI del médico de cabecera: ',dniempleado)
			else:
				print('Error con DNI, por favor introduzcalo de nuevo.')
	    	
	    # Añadir un tratamiento
		elif opc==4:
			addTratamiento(conexion)

	    # Sale del menú
		elif opc==5:
			break
	    # Opcion no valida
		else:
			print('Opcion no valida, vuelva a elegir.\n')




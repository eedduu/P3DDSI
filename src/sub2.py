import cx_Oracle
import datetime

def addHistorial(conexion,dni,telefono,pya,gs,dniempleado):
    cursor = conexion.cursor()

    try:
        cursor.callproc('Historiales.addHistorial',[dni,telefono,pya,gs,dniempleado])
    except cx_Oracle.IntegrityError as error:
        print('...Error añadiendo el nuevo historial:\n\t{}\n'.format(error))


def modHistorial(conexion,dni,telefono,pya,gs,dniempleado):
    cursor = conexion.cursor()

    try:
        cursor.callproc('Historiales.modHistorial',[dni,telefono,pya,gs,dniempleado])
    except cx_Oracle.IntegrityError as error:
        print('...Error modificando el historial:\n\t{}\n'.format(error))


def getHistorial(conexion,dni):
    cursor = conexion.cursor()

    try:
       cursor.callproc('Historiales.getHistorial',[dni])
    except cx_Oracle.IntegrityError as error:
        print('...Error obteniendo el historial:\n\t{}\n'.format(error))
    return cursor.fetchone()


def addTratamiento(conexion,idtratamiento,fechai,fechaf,descripcion,dnipaciente):
    cursor = conexion.cursor()
    
    fechaInicio = datetime.strptime(fechai, "YYYY-MM-DD")
    fechaFinal = datetime.strptime(fechaf, "YYYY-MM-DD")
    try:
        cursor.callproc('Historiales.addTratamiento',[idtratamiento,fechaInicio,fechaFinal,descripcion,dnipaciente])
    except cx_Oracle.IntegrityError as error:
        print('...Error añadiendo el tratamiento:\n\t{}\n'.format(error))

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
                dniempleado = input('DNI del médico de cabecera si se quiere modificar: ') 
                print('Si quiere dejarlo como esta pulse intro')
                
                if (dni != None):   
                    historialant = getHistorial(conexion,dni)
                    
                    if (telefono == None):
                        telefono = historialant[1]
                    if (pya == None):
                        pya = historialant[2]
                    if (gs == None):
                        gs = historialant[3]
                    if (dniempleado == None):
                        dniempleado == historialant[4]

                    modHistorial(conexion,dni,telefono,pya,gs,dniempleado)

                else:
                    print('Introduzca el DNI asociado al historial que se quiere modificar')
	
	    # Imprimir el historial 
	    elif opc==3:
                dni = input('DNI del paciente al cual se le quiere modificar el historial: ')
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
                idtratamiento = input('ID del medicamento: ')
	        fechai = input('Fecha de inicio del tratamiento: ')
                fechaf = input('Fecha de final del tratamiento: ')
                datos  = input('Información asociada al tratamiento: ')
                dniempleado = input('DNI del médico que ha puesto el tratamiento: ')

                addTratamiento(conexion,idtratamiento,fechai,fechaf,datos,dniempleado)

	    # Sale del menú
	    elif opc==5:
	    	break
	    # Opcion no valida
	    else:
	    	print('Opcion no valida, vuelva a elegir.\n')








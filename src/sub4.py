import cx_Oracle


def menuConsulta():

	while True:

	    # Opción del menú
	    print('##################################################')
	    print('# Escoge una opción:                             #')
	    print('# 1.Pedir consulta                               #')
	    print('# 2.Cancelar consulta                            #')
	    print('# 3.Validar consulta                             #')
	    print('# 4.Derivar a especialista                       #')
	    print('# 5.Salir del subsistema                         #')
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
	    	print('we')
	    # Sale del menú
	    elif opc==5:
	    	break
	    # Opcion no valida
	    else:
	    	print('Opcion no valida, vuelva a elegir.\n')

	



def pedirConsulta(conexion, fecha, dniPa)


#Disparador


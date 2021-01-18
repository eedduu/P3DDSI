import cx_Oracle


def menuEmpleados(conn):

	cursor = conn.cursor()
	while True:

		print('###################################################')
		print('# Escoge una opción:                              #')
		print('# 1.Dar de alta un empleado                       #')
		print('# 2.Dar de baja un empleado                       #')
		print('# 3.Modificar datos de un empleado                #')
		print('# 4.Asignar médico de cabecera a historial        #')
		print('# 5.Salir del subsistema                          #')
		print('###################################################')
		opc = int(input('\n Entrada: '))



		if opc==1:
			dni = input('DNI del empleado: ')
			nombreApe = input('Introduzca el nombre y apellidos del empleado: ')
			salario = float(input('Introduzca el salario del empleado: '))

			tipo = input('Introduzca el tipo del empleado ((C)abecera/(E)specialista: ')
			
			if (tipo == 'E') or (tipo == 'C'):
				cursor.callproc("crearEmpleado", (dni, nombreApe,salario,tipo))
			else:
				print('Tipo de empleado no válido.')

		elif opc==2:
			dni = input('DNI del empleado: ')
			cursor.callproc("borrarEmpleado", [dni])
	    	
		elif opc==3:
			dni = input('DNI del empleado a modificar: ')
			nombreApe = input('Introduzca el nombre y apellidos del empleado: ')
			salario = float(input('Introduzca el salario del empleado: '))

			cursor.callproc("modificarEmpleado", (dni, nombreApe,salario))

		elif opc==4:
			dniEmp = input('DNI del empleado (médico de cabecera): ')
			dniHis = input('DNI del paciente (historial de salud): ')

			cursor.callproc("asignarMedicoCabHistorial", (dniEmp, dniHis))

		# Sale del menú
		elif opc==5:
			break
	    	
		# Opcion no valida
		else:
			print('Opcion no valida, vuelva a elegir.\n')

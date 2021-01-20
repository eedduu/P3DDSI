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
			
			try:			
				cursor.callproc("crearEmpleado", (dni, nombreApe,salario,tipo))
			except cx_Oracle.IntegrityError as error:
				codigo = error.args[0].code
		
				if (codigo == 1):
					print('ERROR: Ya existe un empleado con ese DNI')
				elif (codigo == 2290):
					print('ERROR: El salario debe ser positivo');
				else:
					print('ERROR desconocido')
					print(error)
			except cx_Oracle.DatabaseError as error:
				codigo = error.args[0].code
				if (codigo == 20101):
					print('ERROR: Tipo de empleado no válido')
				elif (codigo == 12899):
					print('ERROR: El DNI/Nombre y apellidos es demasiado largo');
				elif (codigo == 1438):
					print('ERROR: El salario no está en el rango establecido');
				else:
					print('ERROR desconocido')
					print(error)
			except Error as error:
				print('ERROR desconocido')
				print(error)


		elif opc==2:
			dni = input('DNI del empleado: ')

			try:
				cursor.callproc("borrarEmpleado", [dni])
			except cx_Oracle.DatabaseError as error:
				codigo = error.args[0].code
				
				if (codigo == 20100):
					print('ERROR: No hay ningún empleado con tal DNI')
				else:
					print('ERROR desconocido')
					print(error)
			except Error as error:
				print('ERROR desconocido')
				print(error)


		elif opc==3:
			dni = input('DNI del empleado a modificar: ')
			nombreApe = input('Introduzca el nombre y apellidos del empleado: ')
			salario = float(input('Introduzca el salario del empleado: '))

			try:
				cursor.callproc("modificarEmpleado", (dni, nombreApe,salario))
			except cx_Oracle.DatabaseError as error:
				codigo = error.args[0].code
				
				if (codigo == 20100):
					print('ERROR: No hay ningún empleado con tal DNI')
				elif (codigo == 12899):
					print('ERROR: El nombre es demasiado largo.')
				elif (codigo ==1438):
					print('ERROR: El salario no está en el rango establecido');
				elif (codigo == 2290):
					print('ERROR: El salario debe ser positivo');
				else:
					print('ERROR desconocido')
					print(error)
			except cx_Oracle.IntegrityError as error:
				codigo = error.args[0].code
		
				if (codigo == 2290):
					print('ERROR: El salario debe ser positivo');
				else:
					print('ERROR desconocido')
					print(error)
			except Error as error:
				print('ERROR desconocido')
				print(error)


		elif opc==4:
			dniEmp = input('DNI del empleado (médico de cabecera): ')
			dniHis = input('DNI del paciente (historial de salud): ')

			try:
				cursor.callproc("asignarMedicoCabHistorial", (dniEmp, dniHis))
			except cx_Oracle.DatabaseError as error:
				codigo = error.args[0].code
				if (codigo == 20141):
					print('ERROR: Quedan consultas pendientes con el médico de cabecera.')
				elif (codigo == 20142):
					print('ERROR: Mismo médico que antes')
				elif (codigo == 1403):
					print('ERROR: No existe tal paciente')
				elif (codigo == 2291):
					print('ERROR: No existe tal médico de cabecera.')
				else:
					print('ERROR desconocido')
					print(error)

			except cx_Oracle.IntegrityError as error:
				if (codigo == 2291):
					print('ERROR: No existe tal médico de cabecera.')
				else:
					print('ERROR desconocido')
					print(error)

			except Error as error:
				print('ERROR desconocido')
				print(error)			

		# Sale del menú
		elif opc==5:
			break
	    	
		# Opcion no valida
		else:
			print('Opcion no valida, vuelva a elegir.\n')

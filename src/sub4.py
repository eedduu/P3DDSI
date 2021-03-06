import cx_Oracle
import datetime


def menuConsulta(conn):

	cursor = conn.cursor()
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
	
	
		# Pedir consulta
		if opc==1:
			dni = input('   DNI del paciente: ')
			dia = int(input('   Día: '))
			mes = int(input('   Mes: '))
			anyo = int(input('   Año: '))
			fecha_correcta = True
			
			
			
			try:
				fecha = datetime.date(anyo,mes,dia).__str__()
			except:
				print("Fecha inválida.")
				fecha_correcta = False
			
			if fecha_correcta :
				try:
					cursor.callproc("pedirConsultaCab", (fecha, dni) )
					conn.commit()
				except cx_Oracle.IntegrityError as error:
					print( (error.args[0].message).split('\n')[0] )
				except cx_Oracle.DatabaseError as error:
					print( (error.args[0].message).split('\n')[0] )
				except Error as error:
					print('ERROR desconocido')
					print(error)
			
		# Cancelar consulta
		elif opc==2:
			idcon = input('ID de la consulta: ')
		
			try:
				cursor.callproc('cancelarConsulta', (idcon))
				conn.commit()
			except cx_Oracle.IntegrityError as error:
				print( (error.args[0].message).split('\n')[0] )
			except cx_Oracle.DatabaseError as error:
				print( (error.args[0].message).split('\n')[0] )
			except Error as error:
				print('ERROR desconocido')
				print(error)

		# Validar consulta
		elif opc==3:
			idcon = input('ID de la consulta: ')

			try:
				cursor.callproc('confirmacion', (idcon))
				conn.commit()
			except cx_Oracle.IntegrityError as error:
				print( (error.args[0].message).split('\n')[0] )
			except cx_Oracle.DatabaseError as error:
				print( (error.args[0].message).split('\n')[0] )
			except Error as error:
				print('ERROR desconocido')
				print(error)



		# Derivar a especialista
		elif opc==4:
			dniPa = input('DNI del paciente: ')
			dniEs = input('DNI del médico especialista: ')
			dia = int(input('   Día: '))
			mes = int(input('   Mes: '))
			anyo = int(input('   Año: '))
			fecha_correcta = True
			try:
				fecha = datetime.date(anyo,mes,dia).__str__()
			except:
				print("Fecha inválida.")
				fecha_correcta = False
	
			if fecha_correcta :
				try:
					cursor.callproc("derivarEsp", (fecha, dniPa, dniEs) )
					conn.commit()
				except cx_Oracle.IntegrityError as error:
					print( (error.args[0].message).split('\n')[0] )
				except cx_Oracle.DatabaseError as error:
					print( (error.args[0].message).split('\n')[0] )
				except Error as error:
					print('ERROR desconocido')
					print(error)

		# Sale del menú
		elif opc==5:
			break

		# Opcion no valida
		else:
			print('Opcion no valida, vuelva a elegir.\n')



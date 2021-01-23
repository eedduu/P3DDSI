import cx_Oracle
import config
import creacion_tablas
from sub1 import *
from sub2 import *
from sub3 import *
from sub4 import *
import sqlscript



# Conexión con la base de datos
conexion = cx_Oracle.connect(config.userid +'/'+ config.userid +'@'+ config.host +':1521/'+ config.service)


# Cursor para hacer transacciones
cursor = conexion.cursor()

# Creación y borrado de tablas
creacion_tablas.borrar_tablas(conexion)
creacion_tablas.crear_tablas(conexion)
creacion_tablas.insertar_tuplas_iniciales(conexion)


print('Creando funcionalidades sql')
sqlscript.run_sql_script(conexion, "plsqlsub1",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")

sqlscript.run_sql_script(conexion, "plsqlsub2",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")

sqlscript.run_sql_script(conexion, "plsqlsub3",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")

sqlscript.run_sql_script(conexion, "plsqlsub4",
                          main_user= "yo",
                          main_password="1234",
                          edition_user="tu",
                          edition_password="1234",
                          edition_name="bof")


while True:

    # Opción del menú

	print('###################################################')
	print('# Escoge una opción:                              #')
	print('# 1.Dar de alta un empleado                       #')
	print('# 2.Dar de baja un empleado                       #')
	print('# 3.Modificar datos de un empleado                #')
	print('# 4.Asignar médico de cabecera a historial        #')
	print('# 5.Añadir un nuevo historial                     #')
	print('# 6.Modificar un historial                        #')
	print('# 7.Imprimir el historial                         #')
	print('# 8.Añadir tratamientos                           #')
	print('# 9.Consultar stock de medicamento                #')
	print('# 10.Añadir stock medicamento                     #')
	print('# 11.Pedir consulta medico cabecera               #')
	print('# 12.Cancelar consulta                            #')
	print('# 13.Confirmar consulta                           #')
	print('# 14.Derivar especialista                         #')
	print('# 15.Reservar maquinaria                          #')
	print('# 16.Salir                                        #')
	print('###################################################')
	opc = int(input('\n Entrada: '))

	if opc==1:
		dni = input('DNI del empleado: ')
		nombreApe = input('Introduzca el nombre y apellidos del empleado: ')
		salario = float(input('Introduzca el salario del empleado: '))

		tipo = input('Introduzca el tipo del empleado ((C)abecera/(E)specialista: ')
		
		try:			
			cursor.callproc("crearEmpleado", (dni, nombreApe,salario,tipo))
			conexion.commit()
		except cx_Oracle.IntegrityError as error:
			print( (error.args[0].message).split('\n')[0] )
		except cx_Oracle.DatabaseError as error:
			print( (error.args[0].message).split('\n')[0] )
		except Error as error:
			print('ERROR desconocido')
			print(error)


	elif opc==2:
		dni = input('DNI del empleado: ')

		try:
			cursor.callproc("borrarEmpleado", [dni])
			conexion.commit()
		except cx_Oracle.IntegrityError as error:
			print( (error.args[0].message).split('\n')[0] )
		except cx_Oracle.DatabaseError as error:
			print( (error.args[0].message).split('\n')[0] )
		except Error as error:
			print('ERROR desconocido')
			print(error)

	elif opc==3:
		dni = input('DNI del empleado a modificar: ')
		nombreApe = input('Introduzca el nombre y apellidos del empleado: ')
		salario = float(input('Introduzca el salario del empleado: '))

		try:
			cursor.callproc("modificarEmpleado", (dni, nombreApe,salario))
			conexion.commit()
		except cx_Oracle.IntegrityError as error:
			print( (error.args[0].message).split('\n')[0] )
		except cx_Oracle.DatabaseError as error:
			print( (error.args[0].message).split('\n')[0] )
		except Error as error:
			print('ERROR desconocido')
			print(error)


	elif opc==4:
		dniEmp = input('DNI del empleado (médico de cabecera): ')
		dniHis = input('DNI del paciente (historial de salud): ')

		try:
			cursor.callproc("asignarMedicoCabHistorial", (dniEmp, dniHis))
			conexion.commit()
		except cx_Oracle.IntegrityError as error:
			print( (error.args[0].message).split('\n')[0] )
		except cx_Oracle.DatabaseError as error:
			print( (error.args[0].message).split('\n')[0] )
		except Error as error:
			print('ERROR desconocido')
			print(error)		
    # Crear un nuevo historial de salud
	if opc==5:
		dni         = input('DNI del paciente: ')
		telefono    = int(input('Teléfono: '))
		pya         = input('Patologías y alergias: ')
		gs          = input('Grupo sanguíneo: ')
		dniempleado = input('DNI del médico de cabecera: ')
		addHistorial(conexion,dni,telefono,pya,gs,dniempleado)
		conexion.commit()
    # Modificación de un historial
	elif opc==6:
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
                         conexion.commit()
		else:
			print('Introduzca un DNI')


    # Imprimir el historial 
	elif opc==7:
		dni = input('DNI del paciente asociado  al historial: ')
		row = getHistorial(conexion,dni)
		print('DNI: ',row[0])
		print('Telefono',row[1])
		print('Patologías y alergías: ',row[2])
		print('Grupo sanguíneo: ',row[3])
		print('DNI médico de cabecera: ',row[4])

	elif opc==8:
		
		cursor.execute("SAVEPOINT Cancelartratamiento")
		addTratamiento(conexion)
		cursor.execute("SAVEPOINT Cancelarrecetas")
		while True:
			print('###################################################')
			print('# Escoge una opción:                              #')
			print('# 1.Nuevo receta				                        #')
			print('# 2.Cancelar recetas                              #')
			print('# 3.Cancelar tratamiento                          #')
			print('# 4.Confirmar tratamiento                         #')
			print('###################################################')
			opc2 = int(input('\n Entrada: '))		
		
			if opc2 == 1:
				id= input('ID del medicamento')
				idtrat= input('ID del tratamiento')
				cant=input('Cantidad del medicamento')
				asignarMedicamentos(conexion, id, idtrat, cant)
			elif opc2 == 2:
				cursor.execute('ROLLBACK TO Cancelarrecetas')
			elif opc2 == 3:
				cursor.execute('ROLLBACK TO Cancelartratamiento')
				break
			elif opc2 == 4:
				break
			else:
				print('Opcion no valida, vuelva a elegir.\n')

		conexion.commit()
	elif opc==9:
		idMed = input('ID del medicamento: ')
		row = consultarStockMed(conexion, idMed)
		if (row!=None):
			print('La cantidad disponible del medicamento con identificador', idMed ,'es ', row)
	elif opc==10:
		cursor.execute("SAVEPOINT Cancelarstocknuevo")
		while True:
			print('###################################################')
			print('# Escoge una opción:                              #')
			print('# 1.Nuevo medicamento		                        #')
			print('# 2.Cancelar nuevo stock medicamentos             #')
			print('# 3.Confirmar cambios                             #')
			print('###################################################')
			opc2 = int(input('\n Entrada: '))		
			if opc2 == 1:
				idmed = input('ID del medicamento')
				cantidad = input('Cantidad del medicamento')
				añadirStock(conexion, idmed, cantidad)
			elif opc2 == 2:
				cursor.execute('ROLLBACK TO Cancelarstocknuevo')
				break
			elif opc2 == 3:
				break
			else:
				print('Opcion no valida, vuelva a elegir.\n')
		
		conexion.commit()

	elif opc==11:
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
					
	elif opc == 12:
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
	elif opc == 13:
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
	
	elif opc == 14:		
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
				conexion.commit()
			except cx_Oracle.IntegrityError as error:
				print( (error.args[0].message).split('\n')[0] )
			except cx_Oracle.DatabaseError as error:
				print( (error.args[0].message).split('\n')[0] )
			except Error as error:
				print('ERROR desconocido')
				print(error)

	
	elif opc == 15:
	
		cursor.execute("SAVEPOINT CancelarMaquinaria")
		idconsulta = input('ID de la consulta')
		while True:
			print('###################################################')
			print('# Escoge una opción:                              #')
			print('# 1.Reservar Maquina			                     #')
			print('# 2.Cancelar Reservas                             #')
			print('# 3.Confirmar reservas                            #')
			print('###################################################')
			opc2 = int(input('\n Entrada: '))		
		
			if opc2 == 1:
				idmaquina = input('ID de la maquina')
				reservar_maquinas(conexion, idmaquina, idconsulta)
			elif opc2 == 2:
				cursor.execute('ROLLBACK TO CancelarMaquinaria')
				break
			elif opc2 == 3:
				break
			else:
				print('Opcion no valida, vuelva a elegir.\n')

		conexion.commit()
	elif opc == 16:
		conexion.commit()
		break
	else:
		print("Opcion no válida")

conexion.commit()










	



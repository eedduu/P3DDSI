##################################################################################
##################################################################################
#############           Borrado y creación de tablas           ###################
##################################################################################
##################################################################################
#
#


import cx_Oracle

#
#	Borrado de tablas
#

def borrar_tablas(conexion):
	
	print('Borrando las tablas...')
	cursor = conexion.cursor()

	# Borrado de tabla Reserva
	try:
		cursor.execute('''DROP TABLE Reserva''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla Reserva:\n\t{}\n'.format(error))

	# Borrado de tabla Receta
	try:
		cursor.execute('''DROP TABLE Receta''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla Receta:\n\t{}\n'.format(error))

	# Borrado de tabla Maquina
	try:
		cursor.execute('''DROP TABLE Maquina''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla Maquina:\n\t{}\n'.format(error))

	# Borrado de tabla Medicamento
	try:
		cursor.execute('''DROP TABLE Medicamento''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla Medicamento:\n\t{}\n'.format(error))

	# Borrado de tabla ConsultaPideRealiza
	try:
		cursor.execute('''DROP TABLE ConsultaPideRealiza''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla ConsultaPideRealiza:\n\t{}\n'.format(error))

	# Borrado de tabla TratamientoTrata
	try:
		cursor.execute('''DROP TABLE TratamientoTrata''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla TratamientoTrata:\n\t{}\n'.format(error))

	# Borrado de tabla HistorialAsigna
	try:
		cursor.execute('''DROP TABLE HistorialAsigna''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla HistorialAsigna:\n\t{}\n'.format(error))

	# Borrado de tabla MedEspecialista
	try:
		cursor.execute('''DROP TABLE MedEspecialista''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla MedEspecialista:\n\t{}\n'.format(error))

	# Borrado de tabla MedCabecera
	try:
		cursor.execute('''DROP TABLE MedCabecera''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla MedCabecera:\n\t{}\n'.format(error))
		
	# Borrado de tabla Empleado
	try:
		cursor.execute('''DROP TABLE Empleado''')
	except cx_Oracle.DatabaseError as error:
		print('Error borrando la tabla Empleado:\n\t{}\n'.format(error))

	print('Fin de borrado de tablas.\n')


#
# Creación de las tablas
#

def crear_tablas(conexion):

	print('Creando las tablas...')
	cursor = conexion.cursor()


	# Creacion de las tablas Stock, Pedido y DetallePedido
	try:
		cursor.execute('''
			CREATE TABLE Maquina(
				IDmaquina int PRIMARY KEY
			)''')

		cursor.execute('''
			CREATE TABLE Medicamento(
				IDmedicamento int PRIMARY KEY,
				CantidadMed int DEFAULT 0,
				constraint cantidad_positiva CHECK (CantidadMed >=0)
			)''')

		cursor.execute('''
			CREATE TABLE Empleado(
				DNIempleado varchar2(9) PRIMARY KEY,
				Nombreyapellidos varchar2(40),
				Salario Number(11,2) CONSTRAINT salario_positivo CHECK (Salario > 0)
			)''')
			
		cursor.execute('''
			CREATE TABLE MedCabecera(
				DNIempleado PRIMARY KEY REFERENCES Empleado(DNIempleado) ON DELETE CASCADE
			)''')

		cursor.execute('''
			CREATE TABLE MedEspecialista(
				DNIempleado PRIMARY KEY REFERENCES Empleado(DNIempleado) ON DELETE CASCADE
			)''')

		cursor.execute('''
			CREATE TABLE HistorialAsigna(
				DNIpaciente varchar2(9) PRIMARY KEY,
				Telefono number(11),
				PyA varchar2(40),
				GS varchar2(3) CHECK (GS in ('A-', 'A+', 'B-', 'B+', 'AB+', 'AB-', '0-', '0+')),
				DNIempleado REFERENCES Medcabecera(DNIempleado)
			)''')
			
		cursor.execute('''
			CREATE TABLE ConsultaPideRealiza(
				IDconsulta int PRIMARY KEY,
				Valida varchar2(5) CHECK (Valida in ('true', 'false')),
				Fecha date,
				DNIpaciente NOT NULL REFERENCES HistorialAsigna(DNIpaciente),
				DNIempleado NOT NULL REFERENCES Empleado(DNIempleado) ON DELETE CASCADE
			)''')

		cursor.execute('''
			CREATE TABLE TratamientoTrata(
				IDtratamiento int PRIMARY KEY,
				FechaI date,
				FechaF date,
				Descripcion varchar2(40),
				DNIpaciente REFERENCES HistorialAsigna(DNIpaciente),
				CONSTRAINT antiviaje CHECK( FechaI < FechaF )
			)''')

		cursor.execute('''
			CREATE TABLE Reserva(
				IDmaquina REFERENCES Maquina(IDmaquina),
				IDconsulta REFERENCES ConsultaPideRealiza(IDconsulta) ON DELETE CASCADE,
				PRIMARY KEY (IDmaquina,IDconsulta)
			)''')

		cursor.execute('''
			CREATE TABLE Receta(
				IDtratamiento REFERENCES TratamientoTrata(IDtratamiento),
				IDmedicamento REFERENCES Medicamento(IDmedicamento),
				CantidadRec int CHECK (CantidadRec > 0),
				PRIMARY KEY (IDtratamiento, IDmedicamento)
			)''')

	except cx_Oracle.DatabaseError as error:
		print('Error creando las tablas:\n\t{}\n'.format(error))

	print('Fin de creación de tablas.\n')


#
# Insertar tuplas iniciales de stock
#
def insertar_tuplas_iniciales(conexion):

	print('...Insertando tuplas...')
	cursor = conexion.cursor()

	# Insercción de tuplas 
	# En caso de error en mitad del try se ejecuta rollback 
	# y no se añade ninguna tupla
	try:
		cursor.execute('''insert into Maquina values (01)''')
		cursor.execute('''insert into Maquina values (02)''')
		cursor.execute('''insert into Maquina values (03)''')
		cursor.execute('''insert into Maquina values (04)''')
		
		cursor.execute('''insert into Medicamento values (01, 100)''')
		cursor.execute('''insert into Medicamento values (02, 50)''')
		cursor.execute('''insert into Medicamento values (03, 20)''')
		cursor.execute('''insert into Medicamento values (04, 10)''')
		
		cursor.execute('''insert into Empleado values ('23862375L', 'Luis Ródriguez Dominguez', 5.05)''')
		cursor.execute('''insert into Empleado values ('23973136C', 'Carlos Lara Casanueva', 10)''')
		cursor.execute('''insert into Empleado values ('99999999L', 'Luis Torno Fabios', 999123)''')
		cursor.execute('''insert into Empleado values ('11111111E', 'Emomu', 0.05)''')
		
		cursor.execute('''insert into MedCabecera values ('23862375L')''')
		cursor.execute('''insert into MedCabecera values ('23973136C')''')		
		cursor.execute('''insert into MedEspecialista values ('99999999L')''')
		cursor.execute('''insert into MedEspecialista values ('11111111E')''')
		
		cursor.execute('''insert into HistorialAsigna values ('19191919Z', 958181818, 'Cáctus.', 'A-', '23862375L')''')
		cursor.execute('''insert into HistorialAsigna values ('89157300N', 955121212, 'Guiña un ojo raro', 'AB+','23973136C')''')
		
		cursor.execute('''insert into ConsultaPideRealiza values ( 01, 'false', TO_DATE('17/12/2022', 'DD/MM/YYYY'), '19191919Z', '23862375L')''')
		cursor.execute('''insert into ConsultaPideRealiza values ( 02, 'false', TO_DATE('01/01/2019', 'DD/MM/YYYY'), '89157300N', '99999999L')''')
		
		cursor.execute('''insert into TratamientoTrata values (01,TO_DATE('01/01/2020', 'DD/MM/YYYY'),TO_DATE('01/05/2020', 'DD/MM/YYYY'), 'Cada 3 días que se rasque', '19191919Z')''')
		cursor.execute('''insert into TratamientoTrata values(02,TO_DATE('29/12/2020', 'DD/MM/YYYY'),TO_DATE('24/2/2021', 'DD/MM/YYYY'), 'Ibuprofeno cada 8 hora','89157300N')''')
		
		cursor.execute('''insert into Reserva values (03, 01)''')
		cursor.execute('''insert into Reserva values (01, 02)''')
		
		cursor.execute('''insert into Receta values (01, 04, 9)''')
		cursor.execute('''insert into Receta values (02, 03, 11)''')
		
	except cx_Oracle.DatabaseError as error:
		print('...Error insertando las tuplas:\n\t{}\n'.format(error))
		conexion.rollback()
	finally:
		conexion.commit()

	print('...Fin de inserción de tuplas.\n')





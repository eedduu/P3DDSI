import cx_Oracle


def pedirConsulta(conexion, fecha, dniPa)
    cursor = conexion.cursor()

    cursor.execute('''SELECT DNIempleado FROM MedCabecera where IDmedicameto = ?''', idMed)
    cantidad = cursor.fetchone()
    print ('La cantidad del medicamento con id ? es ?', idMed, cantidad)


#Disparador


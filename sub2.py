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


def getHistorial(conexion):
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
        

import cx_Oracle
import datetime

def addHistorial(cursor,dni,telefono,pya,gs,dniempleado):
    try:
        cursor.callproc('Historiales.addHistorial',[dni,telefono,pya,gs,dniempleado])
    except cx_Oracle.IntegrityError as error:
        print('...Error añadiendo el nuevo historial:\n\t{}\n'.format(error))


def modHistorial(cursor,dni,telefono,pya,gs,dniempleado):
    try:
        cursor.callproc('Historiales.modHistorial',[dni,telefono,pya,gs,dniempleado])
    except cx_Oracle.IntegrityError as error:
        print('...Error modificando el historial:\n\t{}\n'.format(error))


def getHistorial(cursor):
    try:
       cursor.callproc('Historiales.getHistorial',[dni])
    except cx_Oracle.IntegrityError as error:
        print('...Error obteniendo el historial:\n\t{}\n'.format(error))
    return cursor.fetchone()

def addTratamiento(cursor,idtratamiento,fechai,fechaf,descripcion,dnipaciente):
    fechaInicio = datetime.strptime(fechai, "YYYY-MM-DD")
    fechaFinal = datetime.strptime(fechaf, "YYYY-MM-DD")
    try:
        cursor.callproc('Historiales.addTratamiento',[idtratamiento,fechaInicio,fechaFinal,descripcion,dnipaciente])
    except cx_Oracle.IntegrityError as error:
        print('...Error añadiendo el tratamiento:\n\t{}\n'.format(error))
        

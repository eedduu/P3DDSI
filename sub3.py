import cx_Oracle


def consultarStockMed(conexion, idMed)
    cursor = conexion.cursor()

    cursor.execute('''SELECT CantidadMed FROM Medicamento where IDmedicameto = ?''', idMed)
    cantidad = cursor.fetchone()
    print ('La cantidad del medicamento con id ? es ?', idMed, cantidad)


#Disparador en el 3.2 para que insertemos una maquina en una cita y comprueba que esa maquina no esté en otra cita
#Lo dejo planteado
argumentos: idmaq, idconsul
REATE OR REPLACE TRIGGER comprobar_maquinas BEFORE INSERT ON Reserva FOR EACH ROW
BEGIN
    mifecha= idconsulta.fecha
    SELECT idconsultas FROM Consultas where fecha=mifecha
    Select * From Reservas where idconsulta=idconsultas && idmaquina=idmaq
    if cursor == none => la maquina no está cogida

END

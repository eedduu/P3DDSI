CREATE OR REPLACE PROCEDURE consultarStock(idMed INTEGER) IS

  cantidad INTEGER;
  
BEGIN
  SELECT CantidadMed INTO cantidad FROM Medicamento WHERE IDmedicamento = idMed;
  dbms_output.put_line('La cantidad disponible del medicamento con identificador ' || idMed || ' es : ' || cantidad);

END consultarStock;


/

CREATE OR REPLACE TRIGGER comprobar_maquinas
BEFORE INSERT ON Reserva FOR EACH ROW
DECLARE
  mifecha DATE;
  miconsulta INTEGER;
  mimaquina INTEGER;
  cursor consultas IS SELECT IDconsulta FROM Reserva WHERE IDmaquina = new.IDmaquina;
  fila CONSULTAPIDEREALIZA%ROWTYPE;
BEGIN
  miconsulta:= new.IDconsulta;
  mimaquina:= new.IDmaquina;
  SELECT Fecha INTO mifecha FROM ConsultaPideRealiza WHERE IDconsulta = miconsulta;
  OPEN consultas;
  FETCH consultas INTO fila;
  WHILE consultas%found LOOP
    IF(fila.Fecha = mifecha) THEN
      RAISE_APPLICATION_ERROR(-20000, 'Maquina ya reservada');
    END IF;
    FETCH consultas INTO fila;
  END LOOP;
  CLOSE consultas;

END comprobar_maquinas;

/


CREATE OR  REPLACE PROCEDURE reservar_maquinas(idmaq INTEGER, idconsulta INTEGER) IS
BEGIN
  INSERT INTO Reserva(IDmaquina, IDconsulta) VALUES (idmaq, idconsulta);
  COMMIT;
END reservar_maquinas;


/


CREATE OR REPLACE PROCEDURE asignar_med(idmed INTEGER, idtrat INTEGER, cantidad INTEGER) IS
  actual INTEGER;

BEGIN
  SELECT CantidadRec INTO actual FROM Receta WHERE IDmedicamento = idmed   AND IDtratamiento = idtrat;
  actual:= actual + cantidad;
  UPDATE Receta SET CantidadRec = actual WHERE IDmedicamento = idmed   AND IDtratamiento = idtrat;
  COMMIT;

END asignar_med;


/

CREATE OR REPLACE PROCEDURE añadirStock(idmed INTEGER, cantidad INTEGER) IS
  actual INTEGER;
BEGIN
  SELECT CantidadMed INTO actual FROM Medicamento WHERE IDmedicamento = idmed;
  actual:= actual + cantidad;
  UPDATE Medicamento SET CantidadMed = actual WHERE IDmedicamento = idmed;
  COMMIT;
END añadirStock;
/

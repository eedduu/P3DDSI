CREATE OR REPLACE PROCEDURE consultarStock(idmed int) IS

  cantidad int;

BEGIN
  SELECT CantidadMed INTO cantidad FROM Medicamento WHERE IDmedicamento = idmed;
  DBMS_OUTPUT.PUT_LINE('La cantidad disponible del medicamento con identificador ' || idmed || ' es : ' || cantidad);

END consultarStock;
/

CREATE OR REPLACE TRIGGER comprobar_maquinas
BEFORE INSERT ON Reserva
DECLARE
  mifecha DATE;
  miconsulta INTEGER;
  mimaquina INTEGER;
  cursor consultas IS SELECT * FROM Reserva WHERE IDmaquina = new.IDmaquina;
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
  SHOW ERRORS TRIGGER trigger_name;
  INSERT INTO Reserva(IDmaquina, IDconsulta) VALUES (idmaq, idconsulta);
  COMMIT;
END reservar_maquinas;
/


CREATE OR REPLACE PROCEDURE asignar_med(idmed INTEGER, idtrat INTEGER, cantidad INTEGER) IS
BEGIN
  INSERT INTO Receta(IDmedicamento, IDtratamiento, CantidadRec) VALUES (idmed, idtrat, cantidad);
  COMMIT;
END asignar_med;
/

CREATE OR REPLACE PROCEDURE aniadirStock(idmed INTEGER, cantidad INTEGER) IS
  actual INTEGER;
BEGIN
  SELECT CantidadMed INTO actual FROM Medicamento WHERE IDmedicamento = idmed;
  actual:= actual + cantidad;
  UPDATE Medicamento SET CantidadMed = actual WHERE IDmedicamento = idmed;
  COMMIT;
END aniadirStock;
/

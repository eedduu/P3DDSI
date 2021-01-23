create or replace PROCEDURE consultarStock(idMed int) IS
  cantidad int;

BEGIN
  SELECT CantidadMed INTO cantidad FROM Medicamento WHERE IDmedicamento = idMed;
  DBMS_OUTPUT.PUT_LINE('La cantidad disponible del medicamento con identificador ' || idMed || ' es : ' || cantidad);
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('ERROR, argumentos no válidos');
			RAISE_APPLICATION_ERROR (-20303, 'ERROR, argumentos no validos');
END consultarStock;
/

create or replace TRIGGER comprobar_maquinas
BEFORE INSERT ON Reserva FOR EACH ROW
DECLARE
  mifecha DATE;
  miconsulta INTEGER;
  mimaquina INTEGER;
  abortar BOOLEAN;
  cursor consultas IS SELECT * FROM ConsultaPideRealiza JOIN Reserva ON ConsultaPideRealiza.IDconsulta=Reserva.IDconsulta;
  ocupada EXCEPTION;
BEGIN
  miconsulta:= :new.IDconsulta;
  mimaquina:= :new.IDmaquina;
  SELECT Fecha INTO mifecha FROM ConsultaPideRealiza WHERE IDconsulta=miconsulta;
  abortar:= false;
  FOR elem IN consultas LOOP
    IF(elem.Fecha = mifecha AND elem.IDmaquina = mimaquina) THEN
      abortar:=true;
    END IF;
  END LOOP;
  IF (abortar) THEN
    DBMS_OUTPUT.PUT_LINE('ERROR, maquina ya reservada para otra consulta');
    RAISE_APPLICATION_ERROR (-20305, 'Error al reservar maquina');
  END IF;
END comprobar_maquinas;
/


create or replace PROCEDURE reservar_maquinas(idmaq INTEGER, idconsulta INTEGER) IS
    already EXCEPTION;
    PRAGMA EXCEPTION_INIT (already, -1);
BEGIN
  INSERT INTO Reserva(IDmaquina, IDconsulta) VALUES (idmaq, idconsulta);
  COMMIT;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('ERROR, argumentos no válidos');
			RAISE_APPLICATION_ERROR (-20302, 'ERROR, argumentos no validos');
    WHEN already THEN
            DBMS_OUTPUT.PUT_LINE('ERROR, La maquina ya habia sido reservada para esta consulta');
			RAISE;
END reservar_maquinas;
/


create or replace PROCEDURE asignar_med(idmed INTEGER, idtrat INTEGER, cantidad INTEGER) IS
    actual INTEGER;
    cant EXCEPTION;
    PRAGMA EXCEPTION_INIT(cant, -02290);
BEGIN
  SELECT CantidadMed INTO actual FROM Medicamento WHERE IDmedicamento = idmed;
  actual:= actual - cantidad;
  UPDATE Medicamento SET CantidadMed =actual WHERE IDmedicamento = idmed;
  INSERT INTO Receta(IDmedicamento, IDtratamiento, CantidadRec) VALUES (idmed, idtrat, cantidad);
  COMMIT;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('ERROR, medicamento o tratamiento no valido');
			RAISE_APPLICATION_ERROR (-20301, 'ERROR, medicamento o tratamiento no valido');
    WHEN cant THEN
            DBMS_OUTPUT.PUT_LINE('ERROR, cantidad no disponible');
			RAISE;
END asignar_med;
/

create or replace PROCEDURE aniadirStock(idmed INTEGER, cantidad INTEGER) IS
  actual INTEGER;
  cant EXCEPTION;
  PRAGMA EXCEPTION_INIT(cant, -2290);
BEGIN
  SELECT CantidadMed INTO actual FROM Medicamento WHERE IDmedicamento = idmed;
  actual:= actual + cantidad;
  UPDATE Medicamento SET CantidadMed = actual WHERE IDmedicamento = idmed;
  COMMIT;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el medicamento no está en la base de datos');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el medicamento no está en la base de datos');
    WHEN cant THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, cantidad no valida');
			RAISE;
END aniadirStock;
/

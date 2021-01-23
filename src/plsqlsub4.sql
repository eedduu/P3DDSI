CREATE OR REPLACE PROCEDURE pedirConsultaCab(fecha varchar2, dniPa varchar2) IS 
	dniCab VARCHAR2(9);
	nuevoID INTEGER;
	
	fechainvalida EXCEPTION;
	
	PRAGMA EXCEPTION_INIT (fechainvalida, -20010);
BEGIN 
	SELECT DNIempleado INTO dniCab FROM HistorialAsigna WHERE DNIpaciente = dniPa ;
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	IF( SYSDATE > TO_DATE( fecha,'YYYY-MM-DD') ) THEN
		RAISE_APPLICATION_ERROR (-20010, 'Fecha anterior al dia actual');
	END IF;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniCab ); 
	
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20001, 'DNI incorrecto');
	WHEN fechainvalida THEN
		RAISE_APPLICATION_ERROR (-20010, 'Fecha anterior al dia actual');
	WHEN OTHERS THEN
		RAISE_APPLICATION_ERROR (-20100, 'Error desconocido');
END pedirConsultaCab;
/

CREATE OR REPLACE PROCEDURE cancelarConsulta( idcon INTEGER ) IS 
	idFalse INTEGER;
BEGIN 
	SELECT IDconsulta INTO idFalse FROM ConsultaPideRealiza WHERE IDconsulta = idcon ;
	DELETE FROM Reserva WHERE IDconsulta = idcon; 
	DELETE FROM ConsultaPideRealiza WHERE IDconsulta = idcon; 
	
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20002, 'Sin Datos');
	WHEN OTHERS THEN
		RAISE_APPLICATION_ERROR (-20100, 'Error desconocido');
END cancelarConsulta; 
/
   
CREATE OR REPLACE PROCEDURE confirmacion ( idcon INTEGER ) IS 
	idFalse INTEGER;
	validez EXCEPTION;

	PRAGMA EXCEPTION_INIT (validez, -20005);
BEGIN 
	SELECT IDconsulta INTO idFalse FROM ConsultaPideRealiza WHERE IDconsulta = idcon ;
	UPDATE ConsultaPideRealiza SET Valida = 'true' WHERE IDconsulta = idcon;
	
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20003, 'Sin Datos');
	WHEN validez THEN
		RAISE_APPLICATION_ERROR (-20005, 'Ya hay una valida');
	WHEN OTHERS THEN
		RAISE_APPLICATION_ERROR (-20100, 'Error desconocido');
END confirmacion; 
/

CREATE OR REPLACE PROCEDURE derivarEsp ( fecha varchar2, dniPa varchar2, dniEs varchar2 ) IS
	nuevoID INTEGER; 
	dniFalse VARCHAR(9);
BEGIN 
	SELECT DNIempleado INTO dniFalse FROM MedEspecialista WHERE DNIempleado = dniEs ;
	SELECT DNIpaciente INTO dniFalse FROM HistorialAsigna WHERE DNIpaciente = dniPa ;
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniEs ); 
	
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20004, 'Sin Datos');
	WHEN OTHERS THEN
		RAISE_APPLICATION_ERROR (-20100, 'Error desconocido');
END derivarEsp;
/

create or replace TRIGGER MUCHAS_CONSULTAS
	FOR 
	UPDATE OF Valida ON ConsultaPideRealiza
	COMPOUND TRIGGER
    
    cod INTEGER;
    fech date;
    dnipa varchar(9);
    dniemp varchar(9);
	
BEFORE EACH ROW IS
BEGIN

    fech := :new.Fecha;
    dnipa := :new.DNIpaciente;
    dniemp := :new.DNIempleado;    
	
END BEFORE EACH ROW;

AFTER STATEMENT IS
BEGIN

	SELECT count(*) INTO cod FROM ConsultaPideRealiza WHERE Fecha = fech AND DNIpaciente = dnipa AND DNIempleado = dniemp AND Valida = 'true';

	IF ( cod != 1 ) THEN
		RAISE_APPLICATION_ERROR (-20005, 'No se puede validar');
	END IF;

END AFTER STATEMENT;
END;
/



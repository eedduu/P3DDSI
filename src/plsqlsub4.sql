CREATE OR REPLACE PROCEDURE pedirConsultaCab(fecha varchar2, dniPa varchar2) IS 
	dniCab VARCHAR2(9);
	nuevoID INTEGER;
BEGIN 
	SELECT DNIempleado INTO dniCab FROM HistorialAsigna WHERE DNIpaciente = dniPa ;
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniCab ); 
	COMMIT;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20001, 'Sin Datos');
END pedirConsultaCab;
/

CREATE OR REPLACE PROCEDURE cancelarConsulta( idcon INTEGER ) IS 
	idFalse INTEGER;
BEGIN 
	SELECT IDconsulta INTO idFalse FROM ConsultaPideRealiza WHERE IDconsulta = idcon ;
	DELETE FROM Reserva WHERE IDconsulta = idcon; 
	DELETE FROM ConsultaPideRealiza WHERE IDconsulta = idcon; 
	COMMIT;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20002, 'Sin Datos');
END cancelarConsulta; 
/
   
CREATE OR REPLACE PROCEDURE confirmacion ( idcon INTEGER ) IS 
	idFalse INTEGER;
BEGIN 
	SELECT IDconsulta INTO idFalse FROM ConsultaPideRealiza WHERE IDconsulta = idcon ;
	UPDATE ConsultaPideRealiza SET Valida = 'true' WHERE IDconsulta = idcon;
	COMMIT;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20003, 'Sin Datos');
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
	COMMIT;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RAISE_APPLICATION_ERROR (-20004, 'Sin Datos');
END derivarEsp;
/


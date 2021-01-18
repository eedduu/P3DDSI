CREATE OR REPLACE PROCEDURE pedirConsultaCab(fecha varchar2, dniPa varchar2) IS 
	dniCab VARCHAR2(9);
	nuevoID INTEGER;
BEGIN 
	SELECT DNIempleado INTO dniCab FROM HistorialAsigna WHERE DNIpaciente = dniPa ;
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniCab ); 
	COMMIT;
END pedirConsultaCab;
/

CREATE OR REPLACE PROCEDURE cancelarConsulta( idcon INTEGER ) IS 
BEGIN 
	DELETE FROM Reserva WHERE IDconsulta = idcon; 
	DELETE FROM ConsultaPideRealiza WHERE IDconsulta = idcon; 
	COMMIT;
END cancelarConsulta; 
/
   
CREATE OR REPLACE PROCEDURE confirmacion ( idcon INTEGER ) IS 
BEGIN 
	UPDATE ConsultaPideRealiza SET Valida = 'true' WHERE IDconsulta = idcon;
	COMMIT;
END confirmacion; 
/

CREATE OR REPLACE PROCEDURE derivarEsp ( fecha varchar2, dniPa varchar2, dniEs varchar2 ) IS
	nuevoID INTEGER; 
BEGIN 
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniEs ); 
	COMMIT;
END derivarEsp;
/


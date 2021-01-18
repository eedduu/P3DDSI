CREATE OR REPLACE PROCEDURE pedirConsultaCab(fecha varchar2, dniPa varchar2) AS 
	dniCab VARCHAR2(9);
	nuevoID INTEGER;
BEGIN 
	SELECT DNIempleado INTO dniCab FROM HistorialAsigna WHERE DNIpaciente = dniPa ;
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniCab ); 
END;
/

CREATE OR REPLACE PROCEDURE cancelarConsulta( idcon INTEGER ) AS 
BEGIN 
	DELETE FROM Reserva WHERE IDconsulta = idcon; 
	DELETE FROM ConsultaPideRealiza WHERE IDconsulta = idcon; 
END; 
/
   
CREATE OR REPLACE PROCEDURE confirmacion ( idcon INTEGER ) AS 
BEGIN 
	UPDATE ConsultaPideRealiza SET Valida = 'true' WHERE IDconsulta = idcon;
END; 
/

CREATE OR REPLACE PROCEDURE derivarEsp ( fecha varchar2, dniPa varchar2, dniEs varchar2 ) AS
	nuevoID INTEGER; 
BEGIN 
	SELECT IDconsulta INTO nuevoID FROM ConsultaPideRealiza WHERE IDconsulta >= ALL ( SELECT IDconsulta FROM ConsultaPideRealiza );
	nuevoID := nuevoID + 1 ;
	INSERT INTO ConsultaPideRealiza VALUES ( nuevoID, 'false', TO_DATE( fecha,'YYYY-MM-DD'), dniPa, dniEs ); 
END;
/

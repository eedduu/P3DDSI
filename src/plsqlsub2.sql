CREATE OR REPLACE PROCEDURE addHistorial(dni HistorialAsigna.DNIpaciente%type, 
	telefono HistorialAsigna.Telefono%type, 
	pya  HistorialAsigna.PyA%type,  
	gs   HistorialAsigna.GS%type,
	dniempleado   HistorialAsigna.DNIempleado%type)
 IS 
BEGIN 
	INSERT INTO HistorialAsigna (DNIpaciente,Telefono,PyA,GS,DNIempleado) 
	VALUES(dni, telefono, pya, gs, dniempleado);
	COMMIT; 
END addHistorial; 
/

CREATE OR REPLACE PROCEDURE modHistorial(dni HistorialAsigna.DNIpaciente%type, 
	telefono HistorialAsigna.Telefono%type, 
	pya  HistorialAsigna.PyA%type,  
	gs   HistorialAsigna.GS%type)
IS 
BEGIN 
	UPDATE HistorialAsigna
	SET Telefono = telefono, PyA = pya, GS = gs
	WHERE DNIpaciente = dni; 
	COMMIT;
END modHistorial; 
/

CREATE OR REPLACE PROCEDURE getHistorial (dni HistorialAsigna.DNIpaciente%type)
IS 
BEGIN 
	SELECT * FROM HistorialAsigna WHERE DNIpaciente = dni; 
END getHistorial; 
/

CREATE OR REPLACE PROCEDURE addTratamiento (idtratamiento TratamientoTrata.IDtratamiento%type,
	fechai TratamientoTrata.FechaI%type,
	fechaf TratamientoTrata.FechaF%type,
	descripcion TratamientoTrata.Descripcion%type,
	dnipaciente TratamientoTrata.DNIpaciente%type)
IS 
BEGIN 
	INSERT INTO TratamientoTrata (IDtratamiento, FechaI, FechaF, Descripcion, DNIpaciente)
	VALUES (idtratamiento, fechai, fechaf, descripcion, dnipaciente)
	COMMIT; 
END addTratamiento; 


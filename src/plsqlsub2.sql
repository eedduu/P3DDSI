CREATE OR REPLACE TRIGGER nuevoTratamiento
AFTER INSERT ON TratamientoTrata
FOR EACH ROW
BEGIN
	DELETE FROM TratamientoTrata WHERE DNIpaciente = new.DNIpaciente AND IDtratamiento = mew.IDtratamiento;
END;
/

CREATE OR REPLACE PROCEDURE addHistorial(dni HistorialAsigna.DNIpaciente%type, 
	telefono HistorialAsigna.Telefono%type, 
	pya  HistorialAsigna.PyA%type,  
	gs   HistorialAsigna.GS%type,
	dniempleado   HistorialAsigna.DNIempleado%type)
 IS 
dni_dupliado EXCEPTION;
gs_invalido EXCEPTION;
pya_invalido EXCEPTION;

PRAGMA EXCEPTION_INIT(dni_duplicado, -1);
PRAGMA EXCEPTION_INIT(gs_invalido, -20101);
PRAGMA EXCEPTION_INIT(pya_invalido, -12899;

BEGIN 
	INSERT INTO HistorialAsigna (DNIpaciente,Telefono,PyA,GS,DNIempleado) 
	VALUES(dni, telefono, pya, gs, dniempleado);
	COMMIT; 
	
	EXCEPTION
		WHEN dni_duplicado THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el historial con ese DNI ya existe');
			RAISE_APPLICATION_ERROR (-1, 'ERROR, el historial con ese DNU ya existe');
		WHEN gs_invalido THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el grupo sanguineo introducido es invalido');
			RAISE_APPLICATION_ERROR (-20100, 'ERROR, el grupo sanguineo introducido es invalido');
		WHEN pya_invalido THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, mucho texto introducido en patologias y algergias');
			RAISE_APPLICATION_ERROR (-12899, 'ERROR, mucho texto introducido en patologias y algergias');	
END addHistorial; 
/

CREATE OR REPLACE PROCEDURE modHistorial(dni HistorialAsigna.DNIpaciente%type, 
	telefono HistorialAsigna.Telefono%type, 
	pya  HistorialAsigna.PyA%type,  
	gs   HistorialAsigna.GS%type)
IS 

no_existe  EXCEPTION;
mucho_texto EXCEPTION;

PRAGMA EXCEPTION_INIT (no_existe, -20300);
PRAGMA EXCEPTION_INIT (mucho_texto, -12899); 
BEGIN 
	UPDATE HistorialAsigna
	SET Telefono = telefono, PyA = pya, GS = gs
	WHERE DNIpaciente = dni; 
	COMMIT;

	EXCEPTION
		WHEN no_existe THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el historial con ese DNI no existe');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el historial con ese DNI no existe');
		WHEN mucho_texto THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, mucho texto en patologias y algergias');
			RAISE_APPLICATION_ERROR (-12899, 'ERROR, mucho texto en patologias y algergias');
END modHistorial; 
/

CREATE OR REPLACE PROCEDURE getHistorial (dni HistorialAsigna.DNIpaciente%type)
IS 
no_existe EXCEPTION;

PRAGMA EXCEPTION_INIT (no_existe, -20300);

BEGIN 
	SELECT * FROM HistorialAsigna WHERE DNIpaciente = dni; 

	EXCEPTION
		WHEN no_existe THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el historial con ese DNI no existe');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el historial con ese DNI no existe');
END getHistorial; 
/

CREATE OR REPLACE PROCEDURE addTratamiento (idtratamiento TratamientoTrata.IDtratamiento%type,
	fechai TratamientoTrata.FechaI%type,
	fechaf TratamientoTrata.FechaF%type,
	descripcion TratamientoTrata.Descripcion%type,
	dnipaciente TratamientoTrata.DNIpaciente%type)
IS 

no_existe EXCEPTION;
mucho_texto EXCEPTION;

PRAGMA EXCEPTION_INIT (no_existe, -20300);
PRAGMA EXCEPTION_INIT (mucho_texto, -12899);

BEGIN 
	INSERT INTO TratamientoTrata (IDtratamiento, FechaI, FechaF, Descripcion, DNIpaciente)
	VALUES (idtratamiento, fechai, fechaf, descripcion, dnipaciente)
	COMMIT; 

	EXCEPTION
		WHEN no_existe THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el tratamiento o el paciente no existen');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el tratamiento o el paciente no existen');
		WHEN mucho_texto THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, mucho texto en la descripcion del tratamiento');
			RAISE_APPLICATION_ERROR (-12899, 'ERROR, muco texto en la descripcion del tratamiento');
END addTratamiento; 


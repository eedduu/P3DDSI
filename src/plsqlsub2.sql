create or replace TRIGGER nuevoTratamiento
BEFORE INSERT ON TratamientoTrata
FOR EACH ROW
DECLARE
    n INTEGER;
BEGIN
    SELECT count(*) INTO n FROM TratamientoTrata WHERE (dnipaciente = :new.dnipaciente AND fechaf > :new.fechai); 
    DBMS_OUTPUT.PUT_LINE(n);
	IF (n > 0) THEN
       		raise_application_error(-20620, 'ERROR, el paciente sólo puede tener un tratamiento activo' );
    END IF;
END;
/

CREATE OR REPLACE PROCEDURE addHistorial(dnin HistorialAsigna.DNIpaciente%type, 
	telefonon HistorialAsigna.Telefono%type, 
	pyan  HistorialAsigna.PyA%type,  
	gsn   HistorialAsigna.GS%type,
	dniempleadon   HistorialAsigna.DNIempleado%type)
 IS 
dni_duplicado EXCEPTION;
gs_invalido EXCEPTION;
pya_invalido EXCEPTION;

PRAGMA EXCEPTION_INIT(dni_duplicado, -1);
PRAGMA EXCEPTION_INIT(gs_invalido, -20101);
PRAGMA EXCEPTION_INIT(pya_invalido, -12899);

BEGIN 
	INSERT INTO HistorialAsigna (DNIpaciente,Telefono,PyA,GS,DNIempleado) 
	VALUES(dnin, telefonon, pyan, gsn, dniempleadon);
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
		WHEN others then
			DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
			RAISE_APPLICATION_ERROR (-20105, 'ERROR desconocido');


END addHistorial; 
/

CREATE OR REPLACE PROCEDURE modHistorial(dni HistorialAsigna.DNIpaciente%type, 
	telefonon HistorialAsigna.Telefono%type, 
	pyan  HistorialAsigna.PyA%type,  
	gsn   HistorialAsigna.GS%type)
IS 

no_existe  EXCEPTION;
mucho_texto EXCEPTION;

PRAGMA EXCEPTION_INIT (no_existe, -20300);
PRAGMA EXCEPTION_INIT (mucho_texto, -12899); 
BEGIN 
	UPDATE HistorialAsigna
	SET Telefono = telefonon, PyA = pyan, GS = gsn
	WHERE DNIpaciente = dni; 
	COMMIT;

	EXCEPTION
		WHEN no_existe THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el historial con ese DNI no existe');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el historial con ese DNI no existe');
		WHEN mucho_texto THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, mucho texto en patologias y algergias');
			RAISE_APPLICATION_ERROR (-12899, 'ERROR, mucho texto en patologias y algergias');
		WHEN others then
			DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
			RAISE_APPLICATION_ERROR (-20105, 'ERROR desconocido');

END modHistorial; 
/


CREATE OR REPLACE PROCEDURE getHistorial (dni HistorialAsigna.DNIpaciente%type) IS

fila HISTORIALASIGNA%ROWTYPE;
no_existe EXCEPTION;

PRAGMA EXCEPTION_INIT (no_existe, -20300);

BEGIN 
	SELECT * INTO fila FROM HistorialAsigna WHERE DNIpaciente = dni;
	DBMS_OUTPUT.PUT_LINE('DNI: ' || fila.DNIpaciente || ' Telefono: ' || fila.telefono ||'GS: ' || fila.gs || ' Patologias y alergias: ' || fila.PyA || ' DNI medico cabecera' || fila.DNIempleado );
EXCEPTION
		WHEN no_existe THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el historial con ese DNI no existe');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el historial con ese DNI no existe');
		WHEN others then
			DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
			RAISE_APPLICATION_ERROR (-20105, 'ERROR desconocido');

END; 
/

CREATE OR REPLACE PROCEDURE addTratamiento (idtratamienton TratamientoTrata.IDtratamiento%type,
	fechain varchar2,
	fechafn varchar2,
	descripcionn TratamientoTrata.Descripcion%type,
	dnipacienten TratamientoTrata.DNIpaciente%type)
IS 

no_existe EXCEPTION;
mucho_texto EXCEPTION;
mucho_tratamiento EXCEPTION;

PRAGMA EXCEPTION_INIT (mucho_tratamiento, -20620);
PRAGMA EXCEPTION_INIT (no_existe, -20300);
PRAGMA EXCEPTION_INIT (mucho_texto, -12899);

BEGIN 
	INSERT INTO TratamientoTrata (IDtratamiento, FechaI, FechaF, Descripcion, DNIpaciente)
	VALUES (idtratamienton, TO_DATE( fechain,'YYYY-MM-DD'), TO_DATE( fechafn,'YYYY-MM-DD'), descripcionn, dnipacienten);
	COMMIT; 

	EXCEPTION
		WHEN no_existe THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, el tratamiento o el paciente no existen');
			RAISE_APPLICATION_ERROR (-20300, 'ERROR, el tratamiento o el paciente no existen');
		WHEN mucho_texto THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, mucho texto en la descripcion del tratamiento');
			RAISE_APPLICATION_ERROR (-12899, 'ERROR, mucho texto en la descripcion del tratamiento');
		WHEN mucho_tratamiento THEN
			DBMS_OUTPUT.PUT_LINE('ERROR, mucho texto en la descripcion del tratamiento');
			RAISE_APPLICATION_ERROR (-20620, 'ERROR, sólo puede haber un tratamiento activo');
		WHEN others then
			DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
			RAISE_APPLICATION_ERROR (-20105, 'ERROR desconocido');
END addTratamiento; 
/

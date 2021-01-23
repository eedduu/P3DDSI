create or replace PROCEDURE crearEmpleado(dniEmp varchar2, nombreApe varchar2, salario number, tipo varchar2) IS

salario_negativo EXCEPTION;
empleado_duplicado EXCEPTION;
tipo_invalido EXCEPTION;
dni_nombre_largo EXCEPTION;
salario_fuera_rango EXCEPTION;

PRAGMA EXCEPTION_INIT (salario_negativo, -2290);
PRAGMA EXCEPTION_INIT (empleado_duplicado, -1);
PRAGMA EXCEPTION_INIT (tipo_invalido, -20101);
PRAGMA EXCEPTION_INIT (dni_nombre_largo, -12899);
PRAGMA EXCEPTION_INIT (salario_fuera_rango, -1438);


BEGIN
	INSERT INTO Empleado VALUES (dniEmp, nombreApe, salario);

	IF (tipo = 'E') THEN
		INSERT INTO MedEspecialista VALUES (dniEmp);
	ELSIF (tipo = 'C') THEN
		INSERT INTO MedCabecera VALUES (dniEmp);
	ELSE 
		RAISE_APPLICATION_ERROR (-20101, 'Tipo de empleado no válido');
	END IF;

    
    EXCEPTION
        WHEN salario_negativo THEN
         DBMS_OUTPUT.PUT_LINE('ERROR, el salario debe ser positivo');
			RAISE_APPLICATION_ERROR (-20100, 'ERROR, el salario debe ser positivo');
        WHEN empleado_duplicado THEN
         DBMS_OUTPUT.PUT_LINE('ERROR, empleado con ese dni ya existe');
			RAISE_APPLICATION_ERROR (-20102, 'ERROR, empleado con ese dni ya existe');
        WHEN tipo_invalido THEN
         DBMS_OUTPUT.PUT_LINE('ERROR, el tipo de médico es inválido');
			RAISE_APPLICATION_ERROR (-20101, 'ERROR, el tipo de médico es inválido');
        WHEN dni_nombre_largo THEN
         DBMS_OUTPUT.PUT_LINE('ERROR, el dni o el nombre son demasiado largos');
			RAISE_APPLICATION_ERROR (-20103, 'ERROR, el dni o el nombre son demasiado largos');
        WHEN salario_fuera_rango THEN
         DBMS_OUTPUT.PUT_LINE('ERROR, el salario es demasiado largo');
			RAISE_APPLICATION_ERROR (-20104, 'ERROR, el salario es demasiado largo');
        WHEN others then
         DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
			RAISE_APPLICATION_ERROR (-20105, 'ERROR desconocido');
         
END crearEmpleado;
/

CREATE OR REPLACE PROCEDURE borrarEmpleado(dniEmp varchar2) IS
nu INT;

no_existe EXCEPTION;
no_quedan EXCEPTION;

PRAGMA EXCEPTION_INIT (no_quedan, -20600);
PRAGMA EXCEPTION_INIT (no_existe, -20201);

BEGIN

	SELECT COUNT(*) INTO nu FROM empleado WHERE dniempleado = dniEmp;	

	IF (nu = 0) THEN
		RAISE_APPLICATION_ERROR (-20201, 'No existe un empleado con ese DNI');
	END IF;

	DELETE FROM empleado WHERE dniempleado = dniEmp;

   EXCEPTION
 	 WHEN no_existe THEN
 	   DBMS_OUTPUT.PUT_LINE('ERROR, no existe el empleado que pretende borrar');
		RAISE_APPLICATION_ERROR (-20201, 'ERROR, el empleado no existe');
	 WHEN no_quedan THEN
		DBMS_OUTPUT.PUT_LINE('ERROR, no quedan más medicos de cabecera');
		RAISE_APPLICATION_ERROR (-20600, 'ERROR, no quedan más medicos de cabecera');
 	 WHEN others THEN
   	DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
		RAISE_APPLICATION_ERROR (-20202, 'ERROR desconocido');
         
END borrarEmpleado;
/

CREATE OR REPLACE PROCEDURE modificarEmpleado(dniEmp varchar2, nombreApe varchar2, sal number) IS
nu INT;

no_existe EXCEPTION;
nombre_largo EXCEPTION;
salario_largo EXCEPTION;
salario_negativo EXCEPTION;

PRAGMA EXCEPTION_INIT (no_existe, -20300);
PRAGMA EXCEPTION_INIT (nombre_largo, -12899);
PRAGMA EXCEPTION_INIT (salario_largo, -1438);
PRAGMA EXCEPTION_INIT (salario_negativo, -2290);

BEGIN

	SELECT COUNT(*) INTO nu FROM empleado WHERE dniempleado = dniEmp;	

	IF (nu = 0) THEN
		RAISE_APPLICATION_ERROR (-20100, 'No existe un empleado con ese DNI');
	END IF;

	UPDATE empleado 
	SET nombreyapellidos = nombreApe, salario = sal
	WHERE dniempleado = dniEmp;


	EXCEPTION
 	 WHEN no_existe THEN
 	   DBMS_OUTPUT.PUT_LINE('ERROR, el empleado no existe');
		RAISE_APPLICATION_ERROR (-20300, 'ERROR, el empleado no existe');
 	 WHEN nombre_largo THEN
   	DBMS_OUTPUT.PUT_LINE('ERROR, el nombre es demasiado largo');
		RAISE_APPLICATION_ERROR (-20301, 'ERROR, el nombre es demasiado largo');
 	 WHEN salario_largo THEN
   	DBMS_OUTPUT.PUT_LINE('ERROR, el salario es demasiado largo');
		RAISE_APPLICATION_ERROR (-20303, 'ERROR, el salario es demasiado largo');
 	 WHEN salario_negativo THEN
   	DBMS_OUTPUT.PUT_LINE('ERROR, el salario debe ser positivo');
		RAISE_APPLICATION_ERROR (-20304, 'ERROR, el salario debe ser positivo');
    WHEN others then
      DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
	   RAISE_APPLICATION_ERROR (-20305, 'ERROR desconocido');
         
END modificarEmpleado;
/

CREATE OR REPLACE PROCEDURE asignarMedicoCabHistorial (dniEmp varchar2, dniHis varchar2) IS
diactual date;

fila CONSULTAPIDEREALIZA%ROWTYPE;
antiguomedico varchar2(9);

cursor consultas IS SELECT * FROM CONSULTAPIDEREALIZA 
WHERE (DNIPACIENTE = dniHis AND fecha >= diactual);

mismo_medico EXCEPTION;
no_existe_medico EXCEPTION;

PRAGMA EXCEPTION_INIT (mismo_medico, -20142);
PRAGMA EXCEPTION_INIT (no_existe_medico, -2291);

BEGIN

	SELECT CURRENT_DATE into diactual FROM DUAL;
	SELECT dniempleado INTO antiguomedico FROM historialasigna WHERE dnipaciente = dniHis;

	IF (antiguomedico = dniEmp) THEN
		RAISE_APPLICATION_ERROR (-20142, 'Mismo médico');
	END IF;

	OPEN consultas;
	FETCH consultas INTO fila;
	WHILE consultas%found LOOP
		IF (fila.DNIEMPLEADO = antiguomedico) THEN
			dbms_output.put_line(fila.DNIEMPLEADO);
			dbms_output.put_line(antiguomedico);
			cancelarConsulta(fila.IDCONSULTA); 
		END IF;
		FETCH consultas INTO fila; 
	END LOOP;
	CLOSE consultas;


	UPDATE historialasigna 
	SET dniempleado = dniEmp
	WHERE dnipaciente = dniHis;


	EXCEPTION
 	 WHEN mismo_medico THEN
   	DBMS_OUTPUT.PUT_LINE('ERROR, es el mismo médico que antes');
		RAISE_APPLICATION_ERROR (-20142, 'ERROR, es el mismo médico que antes');
	 WHEN NO_DATA_FOUND THEN
 	   DBMS_OUTPUT.PUT_LINE('ERROR, el paciente no existe');
		RAISE_APPLICATION_ERROR (-20143, 'ERROR, el paciente no existe');
 	 WHEN no_existe_medico THEN
   	DBMS_OUTPUT.PUT_LINE('ERROR, el paciente no existe');
		RAISE_APPLICATION_ERROR (-20144, 'ERROR, el médico no existe o no es de cabecera');
    WHEN others then
      DBMS_OUTPUT.PUT_LINE('ERROR desconocido ');
	   RAISE_APPLICATION_ERROR (-20145, 'ERROR desconocido');
END asignarMedicoCabHistorial;

/

CREATE OR REPLACE TRIGGER ANTES_BORRADO_EMPLEADO
	FOR 
	DELETE ON MEDCABECERA
	COMPOUND TRIGGER

	diactual date;	
	n_otros INTEGER;
	fila_paciente HISTORIALASIGNA%ROWTYPE;

	cursor pacientes IS SELECT * FROM HISTORIALASIGNA 
	WHERE (DNIEMPLEADO = :old.DNIEMPLEADO);

	nuevo_medico varchar(9);

BEFORE EACH ROW IS
BEGIN

	DBMS_OUTPUT.PUT_LINE(:old.DNIEMPLEADO);
-- recorro los pacientes que tenia asignado y los re-asigno
	OPEN pacientes;
	FETCH pacientes INTO fila_paciente;
	WHILE pacientes%found LOOP
		UPDATE HISTORIALASIGNA SET DNIEMPLEADO = NULL WHERE DNIEMPLEADO = :old.DNIEMPLEADO;
		FETCH pacientes INTO fila_paciente; 
	END LOOP;
	CLOSE pacientes;
	
END BEFORE EACH ROW;

AFTER STATEMENT IS
BEGIN

	SELECT CURRENT_DATE into diactual FROM DUAL;

	-- Otros médicos, si no hay cancelar el borrado.
	-- En el caso de que sólo haya uno sin pacientes asignados
	-- no haría falta cancelar el borrado, pero es un caso extremo.
	-- No merece la pena.

	SELECT count(*) INTO n_otros FROM  MEDCABECERA;

	IF (n_otros = 0) THEN
		RAISE_APPLICATION_ERROR (-20600, 'No hay otros médicos de cabecera');	
	END IF;	

	-- Selecciono nuevo.
	SELECT * INTO nuevo_medico FROM MEDCABECERA
	 WHERE rownum = 1;

	-- recorro los pacientes que tenia asignado y los re-asigno
	UPDATE HISTORIALASIGNA SET DNIEMPLEADO = nuevo_medico where DNIEMPLEADO is null;
END AFTER STATEMENT;
END;


/

CREATE OR REPLACE PROCEDURE crearEmpleado(dniEmp varchar2, nombreApe varchar2, salario number, tipo varchar2) IS
BEGIN
	INSERT INTO Empleado VALUES (dniEmp, nombreApe, salario);

	IF (tipo = 'E') THEN
		INSERT INTO MedEspecialista VALUES (dniEmp);
	ELSIF (tipo = 'C') THEN
		INSERT INTO MedCabecera VALUES (dniEmp);
	ELSE 
		RAISE_APPLICATION_ERROR (-20101, 'Tipo de empleado no válido');
	END IF;

	COMMIT;

END crearEmpleado;
/

CREATE OR REPLACE PROCEDURE borrarEmpleado(dniEmp varchar2) IS
nu INT;
BEGIN

	SELECT COUNT(*) INTO nu FROM empleado WHERE dniempleado = dniEmp;	

	IF (nu = 0) THEN
		RAISE_APPLICATION_ERROR (-20100, 'No existe un empleado con ese DNI');
	END IF;

	DELETE FROM empleado WHERE dniempleado = dniEmp;
	COMMIT;
END borrarEmpleado;
/

CREATE OR REPLACE PROCEDURE modificarEmpleado(dniEmp varchar2, nombreApe varchar2, sal number) IS
nu INT;
BEGIN

	SELECT COUNT(*) INTO nu FROM empleado WHERE dniempleado = dniEmp;	

	IF (nu = 0) THEN
		RAISE_APPLICATION_ERROR (-20100, 'No existe un empleado con ese DNI');
	END IF;

	UPDATE empleado 
	SET nombreyapellidos = nombreApe, salario = sal
	WHERE dniempleado = dniEmp;

	COMMIT;
END modificarEmpleado;
/

CREATE OR REPLACE PROCEDURE asignarMedicoCabHistorial (dniEmp varchar2, dniHis varchar2) IS
diactual date;

fila CONSULTAPIDEREALIZA%ROWTYPE;
abortar boolean := false;
antiguomedico varchar2(9);

cursor consultas IS SELECT * FROM CONSULTAPIDEREALIZA 
WHERE (DNIPACIENTE = dniHis AND fecha >= diactual);
BEGIN

	SELECT CURRENT_DATE into diactual FROM DUAL;
	SELECT dniempleado INTO antiguomedico FROM historialasigna WHERE dnipaciente = dniHis;

	IF (antiguomedico = dniEmp) THEN
		RAISE_APPLICATION_ERROR (-20142, 'Mismo médico');
	END IF;

	OPEN consultas;
	abortar := false;
	FETCH consultas INTO fila;
	WHILE consultas%found LOOP
		IF (fila.DNIEMPLEADO = antiguomedico) THEN
			dbms_output.put_line(fila.DNIEMPLEADO);
			dbms_output.put_line(antiguomedico);
			abortar := true; 
		END IF;
		FETCH consultas INTO fila; 
	END LOOP;
	CLOSE consultas;

   IF (abortar = true) then
        RAISE_APPLICATION_ERROR (-20141, 'Quedan consultas pendientes');
   END IF;

	UPDATE historialasigna 
	SET dniempleado = dniEmp
	WHERE dnipaciente = dniHis;

	COMMIT;
END asignarMedicoCabHistorial;
/

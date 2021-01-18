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
BEGIN

	DELETE FROM empleado where dniempleado = dniEmp;
	COMMIT;
END borrarEmpleado;
/

CREATE OR REPLACE PROCEDURE modificarEmpleado(dniEmp varchar2, nombreApe varchar2, sal number) IS
BEGIN

	UPDATE empleado 
	SET nombreyapellidos = nombreApe, salario = sal
	WHERE dniempleado = dniEmp;

	COMMIT;
END modificarEmpleado;
/

CREATE OR REPLACE PROCEDURE asignarMedicoCabHistorial (dniEmp varchar2, dniHis varchar2) IS
BEGIN

	UPDATE historialasigna 
	SET dniempleado = dniEmp
	WHERE dnipaciente = dniHis;

	COMMIT;
END asignarMedicoCabHistorial;
/

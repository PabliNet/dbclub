from os import get_terminal_size, name, system
from datetime import date
from re import search

# Sí o no
def si_o_no (var, no_valida=True):
	if no_valida:
		return True if var.lower() == 's' else False
	else:
		return True if var.lower() in ('s', 'n') else False

# Muestra el valor de una variable numérica de manera legible
def numero (var, digitos=2):
	if int(float(var)) == float(var):
		return var
	else:
		if len(str(var).split('.')[1]) == 1:
			return str(var) + '0'
		else:
			return round(float(var), digitos)

# Si es número
def es_numero (variable):
	test = search('^\d+$', variable)
	if bool(test):
		return True
	else:
		return False

# Sumar meses de a uno
def sumar_mes(_mes, ano_bool=False, _ano=date.today().year):
    _mes += 1
    _ano = _ano if _mes < 13 else _ano + 1
    _mes = 1 if _mes == 13 else _mes
    if ano_bool:
        _mes = str(_mes) if _mes > 9 else f'0{_mes}'
        return f'{_ano}-{_mes}'
    else:
        return _mes

# Restar meses de a uno
def restar_mes(_mes, ano_bool=False, _ano=date.today().year):
    _mes -= 1
    _ano = _ano if _mes > 0 else _ano - 1
    _mes = 12 if _mes == 0 else _mes
    if ano_bool:
        _mes = str(_mes) if _mes > 9 else f'0{_mes}'
        return f'{_ano}-{_mes}'
    else:
        return _mes

#Añador ceros antes del número
def pre_0 (_x, cant_0=9):
	_x = str(_x)
	cant_0 = cant_0 - len(_x)
	return cant_0*'0' + str(_x)

# Limpiar pantalla
limpiar = lambda os_type=name, os_dict={
	'posix': 'clear',
	'nt': 'cls'
}: system(os_dict[os_type])

# Filas y columnas
tam = lambda filas_o_columnas, term_dict = {
	'columnas': get_terminal_size().columns,
	'filas': get_terminal_size().lines
}: term_dict[filas_o_columnas]

# Pausar
pausa = lambda: input('Presione ENTRE para continuar\u2026')

# Si es bisiesto
es_bisiesto = lambda ano: ano % 4 == 0 and ano % 100 != 0 and ano % 400 == 0

if __name__ == '__main__':
	pass
import readline
from os.path import exists
from sys import argv, exit
from datetime import datetime
from json import load, dump

def sumar_mes(_mes):
    _ano, _mes = int(str(_mes)[:-2]), int(str(_mes)[-2:])
    _mes += 1
    _ano = _ano if _mes < 13 else _ano + 1
    _mes = 1 if _mes == 13 else _mes
    _mes = str(_mes) if _mes > 9 else f'0{_mes}'
    return int(f'{_ano}{_mes}')

if __name__ == '__main__':
    if len(argv) != 2:
        exit()
    meses_cuotas = argv[1] + '.json'
    if exists(meses_cuotas):
        with open(meses_cuotas) as _cuotas:
            meses = load(_cuotas)

    if not 'meses' in globals():
        while True:
            while True:
                try:
                    fecha = input('Ingrese año y mes de la nueva cuota (AAA-MM): ')
                    if len(fecha) > 0:
                        datetime.strptime(fecha, '%Y-%m')
                        fecha_list = fecha.split('-')
                        fecha_list[1] = fecha_list[1] if len(fecha_list[1]) == 2 \
                            else '0' + fecha_list[1]
                        fecha = ''.join(fecha_list)
                except ValueError:
                    print ('ERROR: Ingrese AAAA-MM.')
                else:
                    break
            if len(fecha) == 0:
                if len(meses) == 0:
                    exit()
                break

            while True:
                try:
                    importe = int(input('Ingrese el nuevo importe: '))
                    importe = importe if importe > 0 else ''
                except ValueError:
                    print ('ERROR: Importe incorecto.')
                else:
                    break

            if not 'meses' in globals():
                meses = {}
            meses[fecha] = importe
    mes_actual = int(datetime.now().strftime('%Y%m'))
    meses_list = []
    for mes in meses.keys():
        meses_list.append(int(mes))
    i = meses_list[0]
    while i <= mes_actual:
        if not i in meses_list:
            meses_list.append(i)
        i = sumar_mes(i)

    meses_list.sort()

    aux = meses.copy()
    for k, v in tuple(aux.items()):
        if isinstance(k, str):
            aux[int(k)] = v
            aux.pop(k)

    meses = {}
    for m in meses_list:
        if m in aux.keys():
            _cuota = aux[m]
            meses[m] = _cuota
        else:
            meses[m] = _cuota

    with open(meses_cuotas, 'w') as file:
        dump(meses, file, indent=4)
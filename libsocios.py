##edad, atraso, si es baja, antigüedad, categoria
from os import get_terminal_size
from os.path import exists
from json import load, dump
from datetime import datetime
from time import strftime
from mcuotas import sumar_mes

if exists('setting.json'):
    with open('setting.json') as _config:
        CONFIG = load(_config)
else:
    CONFIG = {
        'FORMATO_FECHA': '%d-%m-%Y', 
        'CUOTA': 200,
        'VENCIMIENTO': 20
        }
    with open(f'setting.json', 'w') as _config:
        dump(CONFIG, _config, indent=4)

class Socio:
    def __init__(self,
    numero_de_socio,
    nombre,
    apellido,
    nacimiento,
    dni,
    genero,
    domicilio,
    localidad,
    codigo_postal,
    telefono,
    celular,
    email,
    categoria,
    actividades,
    alta,
    es_baja,
    ultimo_pago,
    adelanto=0):
        self.numero_de_socio = numero_de_socio
        self.nombre = nombre
        self.apellido = apellido
        self.nacimiento = nacimiento
        self.dni = dni
        self.genero = genero
        self.domicilio = domicilio
        self.localidad = localidad
        self.codigo_postal = codigo_postal
        self.telefono = telefono
        self.celular = celular
        self.email = email
        self.categoria = categoria
        self.actividades = actividades
        self.alta = alta
        self.es_baja = es_baja
        self.ultimo_pago = ultimo_pago
        self.adelento = adelanto

    def __str__(self) -> str:
        print_list = [
            ('Número de socio:', self.numero_de_socio),
            ('Nombre', self.nombre_completo),
            ('Fecha de nacimiento', f'{self.nacimiento} ({self.edad} años)'),
            ('DNI', self.dni),
            ('Género', self.genero),
            ('Domicilio', self.domicilio),
            ('Localidad', self.localidad),
            ('Código postal', self.codigo_postal),
            ('Teléfono fijo', self.telefono),
            ('Teléfono celular', self.celular),
            ('E-mail', self.email),
            ('Categoría', self.categoria),
            ('Actividades', self.actividades),
            ('Fecha de alta', self.alta),
            ('Estado', 'Baja' if self.es_baja else 'En actividad'),
            ('Fecha de último pago', self.ultimo_pago)
        ]
        if self.deuda:
            print_list.insert(-1, ('Deuda', self.deuda))
        for label, dato in print_list[:-1]:
            print(f'{label:\uFF65<22}{dato}')

        return f'{print_list[-1][0]:\uFF65<22}{print_list[-1][1]}'

    @property
    def hoy(self):
        return datetime.now()

    @property
    def nombre_completo(self):
        return f'{self.apellido}, {self.nombre}'

    @property
    def edad(self):
        _nacimiento = datetime.strptime(self.nacimiento, CONFIG['FORMATO_FECHA'])
        retorno = self.hoy.year - _nacimiento.year
        retorno = retorno if si_paso(
            _nacimiento,
            CONFIG['FORMATO_FECHA'],
            'aniversario_ano') else retorno - 1
        return retorno

    @property
    def antiguedad(self):
        _alta = datetime.strptime(self.alta, CONFIG['FORMATO_FECHA'])
        retorno = self.hoy.year - _alta.year
        retorno = retorno if si_paso(
            _alta,
            CONFIG['FORMATO_FECHA'],
            'aniversario_ano') else retorno - 1
        return retorno

    @property
    def estado(self):
        return 'Baja' if self.es_baja else 'Activo'

    @property
    def deuda(self):
        _ult_pago = datetime.strptime(self.ultimo_pago, CONFIG['FORMATO_FECHA'])
        ult_mes = int(_ult_pago.strftime('%m'))
        ult_ano = int(_ult_pago.strftime('%Y'))
        mes_actual = self.hoy.month
        ano_actual = self.hoy.year
        _vencida = not (ult_ano == ano_actual and ult_mes == mes_actual)
        _mes_anterior = restar_mes(self.hoy.month, True)
        _mes_anterior = _mes_anterior
        _ult_pago_m_a = _ult_pago.month, _ult_pago.year
        if _vencida and self.hoy.day < CONFIG['VENCIMIENTO'] \
            and _ult_pago_m_a == _mes_anterior or not _vencida:
            return False
        elif _vencida:
            if exists(self.categoria + '.json'):
                with open(self.categoria + '.json') as file_cuotas:
                    cuotas = load(file_cuotas)
            else:
                print ('Faltan ingresar los importes de las cuotas.')
                exit()
            meses_deuda = contar_meses(self.ultimo_pago)
            meses_deuda.pop()
            meses_deuda = [x.replace('-', '') for x in meses_deuda]
            total = 0
            u_mes_cuotas = tuple(cuotas.keys())
            u_mes_cuotas = u_mes_cuotas[-1]
            u_cuota = cuotas[tuple(cuotas.keys())[-1]]
            ano, mes = int(u_mes_cuotas[:4]), int(u_mes_cuotas[-2:])
            anomes_hoy = int(datetime.strftime(self.hoy, '%Y%m'))
            while int(u_mes_cuotas) < anomes_hoy:
                ano, mes = int(ano), int(mes)
                mes += 1
                ano = ano + 1 if mes == 13 else ano
                mes = 1 if mes == 13 else mes
                mes = f'0{mes}' if mes < 10 else mes
                u_mes_cuotas = f'{ano}{mes}'
                cuotas[u_mes_cuotas] = u_cuota
            for cuota in meses_deuda:
                total = total + cuotas[cuota]
            x_meses = len(meses_deuda)
            for x in range(x_meses):
                pass
            return \
            f'${total} ({x_meses} meses)'

class Deudor (Socio):
    def __str__(self) -> str:
        return tabla(self.numero_de_socio, self.nombre_completo,
        self.ultimo_pago, self.deuda)

def si_paso(_fecha, _formato_fecha, _opcion, _hoy=datetime.now()):
    if _opcion == 'aniversario_ano':
        if isinstance(_fecha, str):
            cumple = datetime.strptime(
                    datetime.strptime(_fecha, _formato_fecha)\
                    .strftime('%d-%m-' + str(_hoy.year)),
                    CONFIG['FORMATO_FECHA'])
        else:
            cumple = _fecha.strftime(f'%d-%m-{_hoy.year}')
            cumple = datetime.strptime(cumple, CONFIG['FORMATO_FECHA'])
        dias_cumple = _hoy - cumple
        return dias_cumple.days >= 0

    elif _opcion == 'aniversario_mes':
        dam = datetime.strptime(
            datetime.strptime(_fecha, _formato_fecha)\
            .strftime('%d-' + str(datetime.now()\
            .strftime('%m-%Y'))),
            CONFIG['FORMATO_FECHA'])
        dias_dam = _hoy - dam
        return dias_dam.days >= 0

def sumar_mes(_mes, ano_bool=False, _ano=datetime.now().year):
    _mes += 1
    _ano = _ano if _mes < 13 else _ano + 1
    _mes = 1 if _mes == 13 else _mes
    if ano_bool:
        return _mes, _ano
    else:
        return _mes

def restar_mes(_mes, ano_bool=False, _ano=datetime.now().year):
    _mes -= 1
    _ano = _ano if _mes > 0 else _ano - 1
    _mes = 12 if _mes == 0 else _mes
    if ano_bool:
        _mes = str(_mes) if _mes > 9 else f'0{_mes}'
        return f'{_ano}-{_mes}'
    else:
        return _mes

def contar_meses(hasta, desde=datetime.now()):
    hasta = datetime.strptime(hasta, CONFIG['FORMATO_FECHA'])
    desde = {'ano': int(desde.year), 'mes': int(desde.month)}
    hasta = {'ano': int(hasta.year), 'mes': int(hasta.month)}
    meses = []
    while not (desde['mes'] == hasta['mes']
        and desde['ano'] == hasta['ano']):
        meses.append(restar_mes(desde['mes'], True, desde['ano']))
        desde['mes'] = restar_mes(desde['mes'])
        desde['ano'] = desde['ano'] if desde['mes'] < 12 else desde['ano'] -1
    return meses

def tabla(s, n, u, d):
    cols = get_terminal_size().columns
    _s, _u, _d = 10, 12, 23
    _n = cols - _s - _u - _d
    n = n[:_n]
    _s = f'<{_s}'
    _n = f'^{_n}'
    _u = f'^{_u}'
    _d = f'>{_d}'
    return format(s, _s) + format(n, _n) + format(u, _u) + format(d, _d)

salida = lambda label, dato: f'{label:\uFF65<22}{dato}'

if __name__ == '__main__':
    db_file = 'socios.json'
    if exists(db_file):
        with open(db_file) as _db_file:
            db = load(_db_file)
    socio = Socio(*db['55'].values())

    print (socio.deuda)
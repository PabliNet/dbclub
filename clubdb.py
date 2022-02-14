#!/usr/bin/env python3
import readline
from os import get_terminal_size, system
from os.path import exists
from sys import exit
from datetime import datetime
from argparse import ArgumentParser
from glob import glob
from locale import LC_ALL, setlocale
from json import load, dump
from re import search
from operator import itemgetter
from time import strptime

from click import edit
from pablinet import es_numero, limpiar, numero, pausa, si_o_no, system, tam
from libsocios import CONFIG, Deudor, Socio, tabla

setlocale(LC_ALL, '')

def entrada (variable, tipo, letra=False):
    leyenda = lambda: f'Ingrese {variable}: '
    while True:
        if tipo == 'num':
            valor = input(leyenda())
            if bool(es_numero(valor)):
                break
        elif tipo =='str':
            valor = input(leyenda())
            if letra == 'capital':
                while bool(search('^\s', valor)):
                    valor = valor[1:]
                valor = valor.replace('  ', ' ').capitalize()
            if len(valor) > 0:
                break
        elif tipo == 'genero':
            valor = input(leyenda()).lower()
            generos = {
                'f': 'Femenino',
                'm': 'Masculino',
                'o': 'otro'
            }
            if valor in ('f', 'm', 'o'):
                valor = generos[valor]
                break
            else:
                print ('Ingrese F, M u O.')
        elif tipo =='tel':
            valor = input(leyenda())
            if len(valor) == 0 or (es_numero(valor) and len(valor) == 10):
                break
        elif tipo =='cel':
            valor = input(leyenda())
            if len(valor) == 0 or (es_numero(valor) and len(valor) == 12):
                break
        elif tipo =='fecha':
            formato_fecha = CONFIG['FORMATO_FECHA']
            try:
                valor = input(leyenda())\
                    .replace('/', '-')
                datetime.strptime(valor, CONFIG['FORMATO_FECHA'])
            except ValueError:
                print (f'ERROR: El formato fecha tiene que ser {formato_fecha}.')
            else:
                break
        elif tipo =='cp':
            valor = input(leyenda())
            er = '\d{4}|[A-Za-z]\d{4}[A-Za-z]{3}'
            if bool(search(er, valor)):
                break
        elif tipo =='email':
            er = '^[A-Za-z0-9!#$%&\'*/=?^_+-~\.]+@[A-Za-z0-9\-\.]+\.[A-Za-z]+$'
            valor = input(leyenda())
            if len(valor) == 0:
                break
            elif bool(search(er, valor)):
                usuario, dominio = valor.split('@')
                chars = usuario[0] + usuario[-1] + dominio[0] + dominio[-1]
                if not '.' in chars:
                    break
        elif tipo =='ubicacion':
            er = '[A-Za-z0-9\'°\-\. ]+'
            valor = input(leyenda()).capitalize()
            if search(er, valor):
                break
        elif tipo == 'lista':
            valor = []
            aux_bool = False
            while True:
                actividad = input('Ingrese una actividad, para termina deje el campo vacío: ')
                if len(actividad) >= 0 and not ',' in actividad:
                    aux_bool = True
                    if len(actividad) == 0:
                        break
                    valor.append(actividad.capitalize())
                elif ',' in actividad and not aux_bool:
                    _aux = actividad.capitalize().split(',')
                    _aux = [x for x in _aux if len(x) > 0]
                    while len([ne for ne in _aux if ne[0] == ' ']) > 0:
                        _aux = [ne[1:].capitalize() if ne[0] == ' ' else \
                            ne.capitalize() for ne in _aux]
                    valor.extend(_aux)
                    del(_aux)
                    break
            break
        elif tipo == 'sn':
            valor = input('¿Se le dio la baja? (si/NO) ')
            _aux = ['sí', 'si', 's', 'no', 'n', '']
            if valor in _aux:
                valor = valor in _aux[:3]
                break
    return valor

def cambiar_opcion (n):
    opciones_dict = {
        'e': 'editar',
        'b': 'baja',
        'r': 'remueve',
        'u': 'pago'
    }
    while True:
        opcion = input(f'\n¿Desea \x1b[1;37;40me\x1b[0mditar, dar de \x1b[1;37;40mb\x1b[0maja o \x1b[1;37;40mr\x1b[0memover, actualizar \x1b[1;37;40mú\x1b[0mltimo pago del socio N° {n} o \x1b[1;37;40ms\x1b[0malir? ')
        if opcion == 's':
            exit()
        elif opcion in opciones_dict:
            return opciones_dict[opcion]
        else:
            print ('ERROR: Tiene que tipear B, R, U, o S.')

entradas = (
    ('numero_de_socio', 'num'),
    ('nombre', 'str'),
    ('apellido', 'str'),
    ('nacimiento', 'fecha'),
    ('dni', 'num'),
    ('genero', 'genero'),
    ('domicilio', 'ubicacion'),
    ('localidad', 'str'),
    ('codigo_postal', 'cp'),
    ('telefono', 'tel'),
    ('celular', 'cel'),
    ('email', 'email'),
    ('categoria', 'str'),
    ('actividades', 'lista'),
    ('alta', 'fecha'),
    ('es_baja', 'sn'),
    ('ultimo_pago', 'fecha')
    )

attrs_display = (
    'el número de socio',
    'el nombre',
    'el apellido',
    'la fecha de nacimiento',
    'el DNI',
    'el género (F/M/O)',
    'el domicilio',
    'la localidad',
    'el codigo postal',
    'el teléfono fijo',
    'el celular',
    'el e-mail',
    'la categoria',
    'las actividades',
    'la fecha de alta',
    'si es baja',
    'el último pago'
    )

db_file = 'socios.json'

if exists(db_file):
    with open(db_file, 'r+') as _de_file:
        db = load(_de_file)
else:
    db = {}

parser = ArgumentParser(description='Base de datos de los socios')
opciones = parser.add_argument_group('group')
opciones.add_argument('-a', '--alta', action='store_true', help='Nuevo socio')
opciones.add_argument('-e', '--editar', type=int, help='Editar socio')
opciones.add_argument('-b', '--baja', type=int, help='Baja socio')
opciones.add_argument('-r', '--remueve', type=int, help='Remueve socio')
opciones.add_argument('-l', '--lista', action='store_true', help='Lista socios')
opciones.add_argument('-s', '--buscar', type=int, help='Buscar socio')
opciones.add_argument('-u', '--ultimo', type=str, help='Actualizar último pago')
opciones.add_argument('-f', '--filtro', type=str, help='Filtrar búsqueda')
opciones.add_argument('-d', '--deudores', action='store_true', help='Lista de deudores')
opciones.add_argument('-v', '--version', action='store_true', help='Muestra la versión de DB Club')
args = parser.parse_args().__dict__

if exists(db_file):
    with open(db_file) as _db_file:
        db = load(_db_file)

for opcion, valor in args.items():
    if bool(valor):
        break
opcion = opcion if valor else False
valor = str(valor) if isinstance(valor, int) else valor
del(args)

if not 'opcion' in locals():
    print ('Seleccione una opción, utilice --help para más información')
    exit()

if opcion == 'alta':
    alta = []
    for i, e in enumerate(entradas):
        while True:
            dato = entrada(attrs_display[i], e[1])
            alta.append(dato)
            if e[0] == 'numero_de_socio' and dato in db:
                print (f'ERROR: El socio número {dato} ya existe.')
            elif e[0] == 'dni':
                dnis = [v['dni'] for k, v in db.items()]
                if int(dato) in dnis:
                    for k, v in db.items():
                        if int(dato) == v['dni']:
                            _v = v['nombre'] + ' ' + v['apellido']
                            break
                    print (f'ERROR: El DNI {dato} ya existe y es de {_v}.')
                else:
                    break
            else:
                break
    socio = Socio(*alta)
    db[alta[0]] = socio.__dict__

elif opcion in ('editar', 'baja', 'remueve', 'lista', 'buscar', 'pago'):
    if not str(valor) in db and opcion != 'lista':
        print (f'El socio número {valor} no existe')
        exit(1)
    if opcion != 'lista':
        socio = Socio(*db[valor].values())
        socio_dict = socio.__dict__
        attrs = socio_dict.keys()
        print (socio)
    while True:
        socio_edit = []
        if opcion == 'editar':
            db_editar = db[valor].copy()
            n = f'{db_editar["numero_de_socio"]}'
            editar = []
            for i, _campo, in enumerate(entradas):
                while True:
                    if _campo[0] != 'es_baja':
                        _preg = input(f'¿Desea editar {attrs_display[i]} al socio N° {n} (s/N)? ')
                        _preg = 'n' if len(_preg) == 0 else _preg
                        if si_o_no(_preg, False):
                            if si_o_no(_preg):
                                while True:
                                    dato_nuevo = entrada(*_campo)
                                    if not _campo[0] in ('numero_de_socio', 'dni'):
                                        editar.append(dato_nuevo)
                                        break
                                    elif _campo[0] == 'numero_de_socio':
                                        if not dato_nuevo in db or dato_nuevo == n:
                                            editar.append(dato_nuevo)
                                            break
                                        else:
                                            print (f'ERROR: El número de socio {dato_nuevo} ya existe.')
                                    elif _campo[0] == 'dni':
                                        dnis = [v['dni'] for k, v in db.items()]
                                        if not str(dato_nuevo) in dnis:
                                            editar.append(dato_nuevo)
                                            break
                                        else:
                                            print (f'ERROR: El DNI {dato_nuevo} ya existe.')
                            else:
                                editar.append(db_editar[_campo[0]])
                            break
                    else:
                        editar.append(db_editar[_campo[0]])
                    if i == len(entradas) - 2:
                        break

            if str(editar[0]) != valor:
                db.pop(valor)
                valor = str(editar[0])
            socio = Socio(*editar)
            db[valor] = socio.__dict__
            break
        elif opcion == 'baja':
            while True:
                if socio.es_baja:
                    baja = input ('¿Desea volver a darlo de alta (s/n)? ')
                    if si_o_no (baja, False):
                        if si_o_no(baja):
                            socio.es_baja = False
                            db[valor] = socio.__dict__
                        break
                    else:
                        print ('ERROR: Tipee S o N.')
                else:
                    baja = input ('¿Desea darlo de baja (s/n)? ')
                    if si_o_no (baja, False):
                        if si_o_no(baja):
                            socio.es_baja = True
                            db[valor] = socio.__dict__
                        break
                    else:
                        print ('ERROR: Tipee S o N.')
            opcion = False
            if not opcion:
                break
        elif opcion == 'remueve':
            while True:
                remueve = input(f'¿Desea remover al socio número {valor}? (sí o no) ').lower()
                if remueve in ('sí', 'si', 'no'):
                    if remueve in ('sí', 'si'):
                        db.pop(valor)
                        print (f'El socio número {valor} ha sido eliminado.')
                    break
                else:
                    print ('ERROR: Escriba sí o no.')
            break
        elif opcion == 'lista':
            for k, v in db.items():
                x = Socio(*v.values())
                print ('{0:10} {1}'.format(k, x.nombre_completo))
            break
        elif opcion == 'buscar':
            opcion = cambiar_opcion(valor)
        if opcion == 'pago':
            while True:
                try:
                    pago = input('Ingrese la última fecha de pago: ').lower()
                    pago = socio.hoy.strftime(CONFIG['FORMATO_FECHA']) if pago == 'hoy' else pago
                    strptime(pago, CONFIG['FORMATO_FECHA'])
                except ValueError:
                    print ('ERROR: Escriba hoy o la fecha del último pago.')
                else:
                    break
            db[valor]['ultimo_pago'] = pago
            break
elif opcion == 'filtro':
    valor = valor.lower()
    aux = []
    for k, v in db.items():
        for test in (v['nombre'].lower(), v['apellido'].lower()):
            if valor in test:
                aux.append(k)
                break
    for k in aux:
        socio = Socio(*db[k].values())
        print ('{0:10} {1}'.format(k, socio.nombre_completo))
    exit()

elif opcion == 'deudores':
    deudores = []
    for n, d in db.items():
        s = Deudor(*d.values())
        if s.deuda:
            deudores.append(s)
    print (tabla('Socio N°', 'Nombre completo', 'Ult. pago', 'deuda'))
    for d in deudores:
        print (d)
elif opcion == 'version':
    print ('DB Club 0.2')

#print (socio, '\nputo')
if opcion !='deudores':
    db = dict(sorted((int(k), v) for k, v in db.items()))
    with open(db_file, 'w') as _db_file:
        dump(db, _db_file, indent=4, ensure_ascii=False)
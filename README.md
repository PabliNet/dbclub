# BIENVENIDO AL MANUAL DE DB CLUB

## Pasos para descargar e instalar DB CLUB
Para descargar con git.
```
$ git clone https://github.com/PabliNet/dbclub
```
Si lo desea compilar, utilice pyinstaller:
```
$ pyinstaller -F clubdb.py
$ pyinstaller -F mcuotas.py
```
En caso contrario debe utilizar como script como lo mostraré en este tutorial, pero primero le damos permisos de ejecución a los script:
```
$ chmod +x clubdb.py mcuotas.py
```
## PREPARACIÓN
Antes de comenzar la base de datos debe completar el esquema de cuotas desde el endeudamiento más antiguo. Sólo debe ingresar los meses en el que aumentó la cuota.

Para eso debe ejecutar el archivo `./ncuotas.py` aclarando la categoría de la cuota.

Ejemplo:
```
$ ./mcuotas.py adeherente
```

## USO DE DB CLUB
DB Club utiliza los campo: número de socio (clave primaria), nombre, apellido, DNI, género, domicilio, localidad, código postal, teléfonos fijo y celular, e-mail, categoría, actividades, fecha de alta, estado y último pago.
Para añadir, editar, dar de baja, buscar, actualizar un pago de un socio y listar los deudores, se utilizará el comando `./clubdb.py`.

### Añadir un nuevo socio
Para añadir un socio se necesita utilizar la opción `-a` y se tiene que ingresar todos campos.
```
./clubdb.py -a
```

### Editar un socio
Para editar un socio se necesita utilizar la opción `-e` especificando el número de socio y se preguntará en cada campo a editar.
```
./clubdb.py -e N
```

### Dar de baja un socio
Para dar de baja un socio se necesita utilizar la opción `-b` especificando el número de socio y preguntará si se quiere dar de baja. Si el está dado de baja, se preguntará si se quiere volver a dar de alta.
```
./clubdb.py -b N
```

### Eliminar un socio
Para remover un socio se necesita utilizar la opción `-r` especificando el número de socio.
```
./clubdb.py -r N
```

### Buscar un socio
Para buscar un socio se necesita utilizar la opción `-s` especificando el número de socio.
```
./clubdb.py -s N
```

### Actualizar el pago de un socio
Para actualizar el pago de un socio se necesita utilizar la opción `-p` especificando el número de socio. Se pedirá la fecha de pago.
```
./clubdb.py -p N
```

### Filtro por nombre o apellido
Para listar a los deudores utilizar la opción `-f` especificando la cadena de caracteres.
```
./clubdb.py -f [CADENA DE CARACTERES]
```

### Listar deudores
Para listar a los deudores utilizar la opción `-s` especificando el número de socio.
```
./clubdb.py -d
```
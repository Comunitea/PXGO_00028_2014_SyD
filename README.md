# Buildout base para proyectos con Odoo y PostgreSQL
Odoo 11.0 en el base, PostgreSQL 10.3 y Supervisord 3.0
- Buildout crea cron para iniciar Supervisord después de reiniciar (esto no lo he probado)
- Supervisor ejecuta PostgreSQL, más info http://supervisord.org/
- También ejecuta la instancia de PostgreSQL
- Si existe un archivo dump.sql, el sistema generará la base de datos con ese dump
- Si existe  un archivo frozen.cfg es el que se debería usar ya que contiene las revisiones aprobadas
- PostgreSQL se compila y corre bajo el usuario user (no es necesario loguearse como root), se habilita al autentificación "trust" para conexiones locales. Más info en more http://www.postgresql.org/docs/9.3/static/auth-methods.html
- Existen plantillas para los archivo de configuración de Postgres que se pueden modificar para cada proyecto.


# Uso (adaptado)
En caso de no haberse hecho antes en la máquina en la que se vaya a realizar, instalar las dependencias que mar Anybox
- Añadir el repo a /etc/apt/sources.list:
```
$ deb http://apt.anybox.fr/openerp common main
```
- Si se quiere añadir la firma. Esta a veces tarda mucho tiempo o incluso da time out. Es opcional meterlo
```
$ sudo apt-key adv --keyserver hkp://subkeys.pgp.net --recv-keys 0xE38CEB07
```
- Actualizar e instalar
```
$ sudo apt-get update
$ sudo apt-get install openerp-server-system-build-deps
```
- Para poder compilar e instalar postgres (debemos valorar si queremos hacerlo siempre), es necesario instalar el siguiente paquete (no e sla solución ideal, debería poder hacerlo el propio buildout, pero de momento queda así)
```
$ sudo apt-get install libreadline-dev
```
- Descargar el  repositorio de buildouts :
```
$ git clone -b 11.0 https://github.com/Comunitea/PXGO_00028_2014_SyD.git <ubicacion_local_repo>
```
- Crear un virtualenv dentro de la carpeta del respositorio. Esto podría ser opcional, obligatorio para desarrollo o servidor de pruebas, tal vez podríamos no hacerlo para un despliegue en producción. Si no está instalado, instalar el paquete de virtualenv
```
$ sudo apt-get install python3-virtualenv
$ cd <ubicacion_local_repo>
$ virtualenv -p python3 sandbox --no-setuptools
```
- Ahora procedemos a ejecutar el buildout en nuestro entorno virtual
```
$ sandbox/bin/python bootstrap.py -c <configuracion_elegida>
```
- Ejecutar Supervisor, encargado de lanzar los servicios postgresql y odoo
```
$ bin/supervisord
```
- No crea carpeta project-addons, crearla a mano
```
$ mkdir project-addons
```
- Y por último
```
$ bin/buildout -c <configuracion_elegida>
```
- Urls
- Odoo: http://localhost:8069
      admin//admin

## Configurar Odoo
Archivo de configuración: etc/odoo.cfg, si sequieren cambiar opciones en odoo.cfg, no se debe editar el fichero,
si no añadirlas a la sección [odoo] del buildout.cfg
y establecer esas opciones .'add_option' = value, donde 'add_option'  y ejecutar buildout otra vez.

Por ejmplo: cambiar el nivel de logging de OpenERP
```
'buildout.cfg'
...
[odoo]
options.log_handler = [':ERROR']
...
```

Si se quiere jeecutar más de una instancia de OpenERP, se deben cambiar los puertos,
please change ports:
```
odoo_xmlrpc_port = 8069  (8069 default openerp)
supervisor_port = 9002      (9001 default supervisord)
postgres_port = 5434        (5432 default postgres)
```

## Creators

Rastislav Kober, http://www.kybi.sk


# Solución Backend para organizar la información de personajes y locaciones de los multiversos

A continuación se describe el procedimiento que se debe realizar para desplegar la solución propuesta de manera local.

### Instalación

Se recomienda trabajar sobre un ambiente virtual para evitar conflictos con otros proyectos. Para ello se ejecutan los siguientes comandos.

``` bash
virtualenv <directorio> --python=python3.6
source directorio/bin/activate
```
Se debe observar un cambio en el prompt que indique que se activó el entorno virtual. Lo siguiente será instalar los módulos necesarios.
```bash
pip install Flask Flask-JWT Flask-RESTful Flask-SQLAlchemy
```

### Modificación programa principal

Para realizar las pruebas localmente en el archivo *app.py* se deben descomentar las líneas que inicializan la base de datos y crean las tablas correspondientes.

Así también, cada vez que se ejecute la aplicación es necesario eliminar el archivo *data.db* que se crea en el directorio en el que se ejecuta la aplicación, de lo contrario habrá inconsistencias.

### Ejecución

Para desplegar la aplicación se debe ejeecutar el siguiente comando:

```bash
python app.py
```

### Pruebas

Para verificar que funciona correctamente se recomienda utilizar una herramienta externa diseñada específicamente para esto, como Postman o bien desplegar la API en un entorno apropiado como Heroku.

#### Heroku

Es posible desplegar la aplicación creando una nueva api que se vincule con este repositorio, utilizando una base de datos gratuita de JawsDB MySQL. Lo único que se debe considerar es que en el archivo *app.py* se deben comentar las líneas que inicializan la base de datos y crean las tablas correspondientes.


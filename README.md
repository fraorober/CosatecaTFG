# CosatecaTFG
Trabajo de Fin de Grado realizado por Francisco de Paula Orozco Bernárdez-Zerpa.

En este README podrá encontrar dos breves guías para poder ejecutar la aplicación y los "test".

Instrucciones e indicaciones para poder probar la aplicación:
1. Descargamos el zip, extraigalo y ábralo con su IDE favorito. Podrá observar cuatro archivos entre los que se encuentra el “requirements.txt” que contiene todas las dependencias necesarias para que funcione el proyecto. Se recomienda el uso de un entorno virtual. Si se encuentra en Windows y usando Visual Studio Code, ejecute los siguientes comandos:
   
            python -m venv NOMBRE_ENTORNO → Le creará el entorno virtual.
   
            NOMBRE_ENTORNO/Scripts/activate → Para activar el entorno virtual.
   
            pip install -r requirements.txt → Para instalar todas las dependencias.
   
2. De las dos carpetas mencionadas anteriormente, sitúese dentro de la carpeta denominada “Cosateca”.
   
3. Dentro de esta podrá encontrar diversos archivos y directorios, entre ellos el archivo “manage.py” que nos servirá más adelante para arrancar la aplicación.
   
4. Antes de ejecutar la aplicación debemos conectarla con la base de datos. Para ello diríjase a un software que le permita conectarse a la base de datos MySQL (se recomienda HeidiSQL). Establezca una conexión con los siguientes datos:

            Usuario: root
   
            Contraseña: root
   
            Puerto 3306
   
            Host: 127.0.0.1

    Es importante que se respeten estos campos, pues la conexión con la base de datos está configurada de esta manera en el “settings.py”.

5. Una vez haya abierto la conexión, tiene que crear una base de datos con el siguiente nombre:

            Nombre: cosateca

6. Ya está creada la base de datos. Hacemos la migración, ejecutando dicho comando a la altura del archivo “manage.py”:

            python manage.py makemigrations

            python manage.py migrate
   
7. Ahora se procede a hacer una población inicial para simular lo que sería un uso normal de la aplicación. Para ello se le proporciona un script que deberá ejecutar con el siguiente comando (importante que lo haga a la altura del archivo manage.py):
   
            python population.py

8. Arranque la aplicación ejecutando el siguiente comando (también a la altura del archivo manage.py):

            python manage.py runserver

Ya podrá disfrutar de la aplicación.

Para probar la aplicación puede registrarse o iniciar sesión con alguno de los usuarios ya creados, por ejemplo:

      Con derecho de administración:
                  Username: admin
                  Password: admin
      Usuario registrado:
                  Username: pedroJose_10
                  Password: asdf1234


Instrucciones para ejecutar los “tests”:
1. En la terminal póngase a la altura del archivo “manage.py”.
   
2. Puede ejecutar las pruebas con dos comandos diferentes:

                  pytest → Le muestra una salida por consola resumiendo los resultados de los tests.
   
                  pytest --cov=CosatecaApp --cov-report=html → Le muestra una salida por consola de los resultados de los tests y además le genera unos archivos (que sobreescribirían a los ya presentes). Estos son el archivo “.coverage” y la carpeta “htmlcov”. Ésta última carpeta contiene un archivo html denominado “index.html”, que si abre con su navegador, podrá ver un resumen más detallado de la cobertura proporcionada por las pruebas.

    Es importante ejecutar el comando que elija, a la altura del archivo “manage.py”, puesto que en la clase de prueba se hace una llamada a la ruta de imágenes. Si lo ejecuta en otro directorio, probablemente el método o los método en cuestión, no encuentren dicho archivo.

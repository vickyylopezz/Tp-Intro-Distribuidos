# Introducción a los Sistemas Distribuidos:  TP N°1: File Transfer

Este documento contiene instrucciones de cómo ejecutar el cliente y el servidor.

## Dependencias a instalar:
* Python 3
* mininet

## Pasos a seguir para ejecutar la aplicación:

### Cómo ejecutar mininet
Para ejecutar _mininet_, correr el siguiente comando, especificando el número de clientes y el porcentaje de pérdida de los enlaces:

      ./run_topology.sh numero_de_clientes porcentaje_de_perdida

### Servidor

El servidor consta de un sólo comando `start-server`, que permite iniciar el servidor. Para correrlo, ejecutar en el directorio del archivo _start-server.py_:

    $ python3 ./start-server [-h] [-v | -q] (-w | -r) [-H ADDR] [-p PORT] [-s DIRPATH]

Pueden utilizarse distintos flags:

`-h` , `--help` permite mostrar el mensaje de ayuda y detalle de los distintos flags.  
`-v` , `--verbose` | `-q` , `--quiet` muestra detalles extra sobre el envío de archivos.  
   `-H` , `--host` permite indicar el host donde se quiere levantar el servidor.  
    `-p` , `--port` permite indicar el puerto donde se quiere levantar el servidor.  
    `-s` , `--storage` permite indicar el directorio donde se quieren bajar los archivos.  
    `-w`, `--saw` | `-r`, `--sr` permite elegir el protocolo de capa de transporte. Este flag es obligatorio.

Se puede frenar la ejecución del servidor en cualquier momento presionando la letra `q`.

### Cliente

El cliente cuenta con dos comandos distintos:  

   `upload-file`: permite subir un archivo al servidor.     
    `download-file`: permite descargar un archivo del servidor.     
  
  
  
#### upload-file

Para correr este módulo, ejecutar en el directorio del archivo _upload-file.py_:

    $ python3 ./upload-file [-h] [-v | -q] (-w | -r) [-H ADDR] [-p PORT] [-s FILEPATH] [-n FILENAME]

Pueden utilizarse distintos flags:

   `-h` , `--help` permite mostrar el mensaje de ayuda y detalle de los distintos flags.  
    `-v` , `--verbose` | `-q` , `--quiet` muestra detalles extra sobre el envío de archivos.  
    `-H` , `--host` permite indicar la dirección IP del servidor.  
    `-p` , `--port` permite indicar el puerto en el que está escuchando el servidor.  
    `-s` , `--src` permite indicar la ruta del archivo a enviar.  
    `-n` , `--name` permite indicar el nombre con el cual el archivo queda guardado en el servidor.  
    `-w`, `--saw` | `-r`, `--sr` permite elegir el protocolo de capa de transporte. Este flag es obligatorio.

#### download-file

Para correr este módulo, ejecutar en el directorio del archivo _download-file.py_:

    $ python3 ./download-file [-h] [-v | -q] (-w | -r) [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME]

Pueden utilizarse distintos flags:

   `-h` , `--help` permite mostrar el mensaje de ayuda y detalle de los distintos flags.  
    `-v` , `--verbose` | `-q` , `--quiet` muestra detalles extra sobre el envío de archivos.  
    `-H` , `--host` permite indicar la dirección IP del servidor.  
    `-p` , `--port` permite indicar el puerto en el que está escuchando el servidor.  
    `-s` , `--dst` permite indicar la ruta donde será guardado el archivo descargado.  
    `-n` , `--name` permite indicar el nombre del archivo alojado en el servidor a descargar.  
    `-w`, `--saw` | `-r`, `--sr` permite elegir el protocolo de capa de transporte. Este flag es obligatorio.

## Cuestiones a considerar

* No se permite subir archivos al servidor ni solicitar la descarga de archivos cuyo nombre contenga el caracter `#`, ya que se usa como separador en los mensajes de protocolo de aplicación.
* El tamaño máximo de archivo que se puede subir o bajar es de 2 GB.

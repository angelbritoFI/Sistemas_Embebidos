#|/bin/bash
# @Autor        Angel Brito Segura
# @Fecha        16/10/2021
# @Descripcion  Crear canción con el lenguaje C

echo "Compilando el programa"
gcc programa.c

echo "Ejecutando el programa redireccionando la salida a la tarjeta de audio"
./a.out | aplay -f U8
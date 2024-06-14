# Services

Esta documentación describe el uso de las aplicaciones usadas en el examen de admisión al programa de Música de la Universidad del Atlántico. Esto no quiere decir, por ningún motivo, que el desarrollo pertenezca a dicha universidad. El único propietario de este desarrollo es el propio desarrollador.

## Cargar la lista de aspirantes

### Archivo csv con los aspirantes

Se carga un archivo .csv en la carpeta services/data/.
Este archivo es un documento de 4 columnas separadas por comas, siguiendo el siguiente formato
documento de identidad,GRUPO_{int},NOMBRE,INSTRUMENTO

Este documento se genera desde excel a partir de un documento que debe entregar la coordinación del programa.

### Indicar el path del archivo csv

En el archivo ``setAspirantes.py`` actualizar el nombre del archivo en la línea 11 ``filname = os.sep.join(['data', 'nombre_del_archivo'])`` remplazando nombre_del_archivo por el nombre real del archivo.

### Correr el script

``$ python3 setAspirantes.py``

Para correr la versión local es necesario tener corriendo el backend en local.

## Definir personas

### Definir jurados uno a uno

1. Se corre el script ``$ python3 setPerson.py``
2. Opción 2- Ingresar un nuevo jurado
3. Indique el nombre del jurado
4. Ingrese el número de cédula
5. Ingrese el grupo

### Definir jurados desde un archivo

1. En ``data/lista_jurados.csv`` se definen los jurados con la convención:
GRUPO_{int},Nombre del jurado,cédula
2. Se corre el script ``$ python3 setPerson.py``
3. Opción 3- Otro
4. Opción 5- Agregar los jurados desde un archivo 
5. Determine el tipo de conexión. Para local se debe tener corriendo el back en local

### Definir monitor uno a un o

## URLs para el registro de notas

### Solfeo Jurados

Solfeo_1: https://riedmusicapp.com/examination/admisionesUA/solfeo_1/jury
Solfeo_2: https://riedmusicapp.com/examination/admisionesUA/solfeo_2/jury
Solfeo_3: https://riedmusicapp.com/examination/admisionesUA/solfeo_3/jury
Solfeo_4: https://riedmusicapp.com/examination/admisionesUA/solfeo_4/jury
Solfeo_5: https://riedmusicapp.com/examination/admisionesUA/solfeo_5/jury
Solfeo_6: https://riedmusicapp.com/examination/admisionesUA/solfeo_6/jury
Solfeo_7: https://riedmusicapp.com/examination/admisionesUA/solfeo_7/jury
Solfeo_8: https://riedmusicapp.com/examination/admisionesUA/solfeo_8/jury
Solfeo_9: https://riedmusicapp.com/examination/admisionesUA/solfeo_9/jury

### Instrumento Jurados

GRUPO_1 - Acordeón
https://riedmusicapp.com/examination/admisionesUA/grupo1/jury

GRUPO_2 - Guitarra eléctica y bajo eléctrico
https://riedmusicapp.com/examination/admisionesUA/grupo2/jury

GRUPO_3 - Canto
https://riedmusicapp.com/examination/admisionesUA/grupo3/jury

GRUPO_4 - Eufonio, Saxofón, Trompeta, Clarinete
https://riedmusicapp.com/examination/admisionesUA/grupo4/jury

GRUPO_5 - Guitarra acústica
https://riedmusicapp.com/examination/admisionesUA/grupo5/jury

GRUPO_6 - Percusión
https://riedmusicapp.com/examination/admisionesUA/grupo6/jury

GRUPO_7 - Piano
https://riedmusicapp.com/examination/admisionesUA/grupo7/jury

GRUPO_8 - Violín, Viola
https://riedmusicapp.com/examination/admisionesUA/grupo8/jury

### Instrumento Monitores

GRUPO_1 - Acordeón
https://riedmusicapp.com/examination/admisionesUA/grupo1/monitor

GRUPO_2 - Guitarra eléctica y bajo eléctrico
https://riedmusicapp.com/examination/admisionesUA/grupo2/monitor

GRUPO_3 - Canto
https://riedmusicapp.com/examination/admisionesUA/grupo3/monitor

GRUPO_4 - Eufonio, Saxofón, Trompeta, Clarinete
https://riedmusicapp.com/examination/admisionesUA/grupo4/monitor

GRUPO_5 - Guitarra acústica
https://riedmusicapp.com/examination/admisionesUA/grupo5/monitor

GRUPO_6 - Percusión
https://riedmusicapp.com/examination/admisionesUA/grupo6/monitor

GRUPO_7 - Piano
https://riedmusicapp.com/examination/admisionesUA/grupo7/monitor

GRUPO_8 - Violín, Viola
https://riedmusicapp.com/examination/admisionesUA/grupo8/monitor






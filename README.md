El archivo .pdf se encuentrar las instrucciones para realizar esta prueba. En el archivo .zip se encuentra la base de datos de SQLite. Recuerde que se espera un repositorio por persona, por lo tanto, no se aceptarán commints en este repositorio.

SOLUCIÓN:

Envía un correo electrónico con asunto en tabla parámetros de Excel, a los destinatarios en tabla parámetros de Excel, con los valores totales a cobrar a cada empresa en estado en tabla parámetros de Excel, para el rango de fechas en la tabla parámetros de Excel.

Para instalar los requisitos en torno a librerías de Python, es necesario ejecutar el archivo 'install.bat'. Este permitirá que la solución se pueda ejecutar sin contratiempos.

Librerías necesarias:
- pywin32==306
- openpyxl==3.1.5
- pandas==2.2.2

PARÁMETROS DE ENTRADA:

En el archivo de Excel 'insumos/condiciones_por_empresa.xslx' existen 3 hojas de cálculo con información parametrizada para la ejecución:
1.	Comisiones: Lo referente a la traducción del cobro de comisiones de las condiciones de contratadas por cada empresa.
2.	Descuentos: Lo referente a la traducción del descuento por no respuesta de la API según condiciones contratadas por cada empresa.
3.	Parámetros: Parámetros de ejecución:
    - mail_to: Correo electrónico a quién se le enviará el archivo xlsx resultante y la información. En caso de requerir más usuario, separarlos por punto y como. Ejemplo: user1@...; user2@...
    - subject: Asunto con el que se enviará el correo.
    - fecha_incio: Fecha inicio de facturación en formato yyyymmddHHMMSS
    - fecha_fin: Fecha fin de facturación en formato yyyymmddHHMMSS

EJECUCIÓN:

Tras instalar con install.bat, ejecutar el archivo cobro_comisiones.py.
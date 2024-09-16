import os
import sqlite3
import pandas as pd
import win32com.client

class Comisiones():
    def __init__(self):
        # Obtener la ruta completa del archivo en ejecución
        self.directorio = os.path.dirname(os.path.abspath(__file__))
        # Validar que la base de datos exista, de lo contrario cerrar ejecución mostrando error
        if os.path.exists(f'{self.directorio}/database.sqlite'):
            self.conexion = sqlite3.connect(f'{self.directorio}/database.sqlite')
            print(f'Conexión establecidad con "database.sqlite"')
        else:
            # Mostrar error
            Exception(f'Base de datos "{self.directorio}/database.sqlite" no existe')

    def enviar_correo(self, parametros, file, tabla):
        """Función para enviar correo

        Args:
            parametros (dict): Condiciones de uso
            file (str): Dirección al archivo adjunto
            tabla (html): Tabla del archivo adjunto en HTML
        """
        # Busco la aplicacion de Outlook
        ol = win32com.client.Dispatch('Outlook.application')
        # Creo un correo
        correo = ol.CreateItem(0)
        # Insertar destinatarios o destinatario
        correo.To = parametros['mail_to']
        # Insertar asunto
        correo.Subject = parametros['subject']
        # Insertar cuerpo de correo (<br>, salto de linea)
        correo.HTMLbody = f'Cordial saludo.<br>Se adjunta cuenta de cobro para el rango de fechas de {parametros["fecha_inicio"]} a {parametros["fecha_fin"]}.<br> {tabla}'
        # Adjuntar al correo el xlsx
        correo.Attachments.Add(file)
        # Enviar el correo
        correo.Send()
        print(f'Correo enviado exitosamente')

    def run(self):
        """Ejecuta la lógica del cobro de comisiones
        """
        # Leer comisiones, descuentos y parámetros
        print("Leyendo insumos")
        df_comisiones = pd.read_excel(f'{self.directorio}/insumos/condiciones_por_empresa.xlsx', sheet_name='comisiones')
        df_descuentos = pd.read_excel(f'{self.directorio}/insumos/condiciones_por_empresa.xlsx', sheet_name='descuentos')
        parametros = pd.read_excel(f'{self.directorio}/insumos/condiciones_por_empresa.xlsx', sheet_name='parametros')
        # Convertir DataFrame a un diccionario para usar parámetros en ejecución
        print("Calculando parámetros")
        parametros = pd.Series(parametros['valor_parametro'].values, index=parametros['nombre_parametro']).to_dict()
        # Modificar fechas
        # Fecha inicio
        parametros['fecha_inicio'] = pd.to_datetime(parametros['fecha_inicio'], format='%Y%m%d%H%M%S')
        parametros['fecha_inicio'] = parametros['fecha_inicio'].strftime('%Y-%m-%d %H:%M:%S')
        # Fecha fin
        parametros['fecha_fin'] = pd.to_datetime(parametros['fecha_fin'], format='%Y%m%d%H%M%S')
        parametros['fecha_fin'] = parametros['fecha_fin'].strftime('%Y-%m-%d %H:%M:%S')
        # Traerme la consulta
        print('Leyendo SQL conteo_llamados_api.sql')
        with open(f'{self.directorio}/insumos/conteo_llamados_api.sql') as sql_file:
            sql = sql_file.read()
        # Cargar los datos en un DataFrame de pandas
        print('Ejecutando SQL conteo_llamados_api.sql')
        df = pd.read_sql_query(sql.format(**parametros), self.conexion)
        # Definir de forma dinámica los limites superiores de las comisiones y los descuentos  con base a los máximos del consolidado
        print('Completando información')
        # Encuentra el valor máximo en la columna successful_count
        max_valor_succ = df['successful_count'].max()
        # Encuentra el valor máximo en la columna unsuccessful_count
        max_valor_unsucc = df['unsuccessful_count'].max()
        # Rellenar los valores nulos en la columna 'max_successful' con el valor máximo
        df_comisiones.fillna({'lim_sup_successful':max_valor_succ}, inplace=True)
        # Rellenar los valores nulos en la columna 'max_unsuccessful' con el valor máximo
        df_descuentos.fillna({'lim_sup_unsuccessful':max_valor_unsucc}, inplace=True)
        # Guardar el DataFrame en la base de datos SQLite, realizar el procesamiento con SQL
        print('Subiendo información de consilidado sin comisiones')
        df.to_sql('consolidado_sin_comisiones', self.conexion, if_exists='replace', index=False)
        df_comisiones.to_sql('comisiones', self.conexion, if_exists='replace', index=False)
        df_descuentos.to_sql('descuentos', self.conexion, if_exists='replace', index=False)
        # Traerme la consulta del cálculo de comisiones
        print('Leyendo SQL calculo_comisiones.sql')
        with open(f'{self.directorio}/insumos/calculo_comisiones.sql') as sql_file:
            sql_calculo_comisiones = sql_file.read()
        # Cargar los datos en un DataFrame de pandas
        print('Ejecutando SQL conteo_llamados_api.sql')
        df_calculo_comisiones = pd.read_sql_query(sql_calculo_comisiones, self.conexion)
        # Crear carpeta de resultados
        print('Validando carpeta de resultados')
        if not os.path.isdir(f'{self.directorio}/resultados'):
            os.mkdir(f'{self.directorio}/resultados')
        # Exportar DataFrame a Excel
        print('Exportando documento de facturas')
        file = f'{self.directorio}/resultados/calculo_comisiones.xlsx'
        # index=False -> Sin numeración de filas
        df_calculo_comisiones.to_excel(file, index=False)
        # index=False -> Sin numeración de filas
        print('Enviado correo')
        self.enviar_correo(parametros, file, df_calculo_comisiones.to_html(index=False))

if __name__ == "__main__":
    # Solo se ejecuta la lógica de este script si se ejecutada directamente desde el .py (no ejecuta si se importa)
    comisiones = Comisiones()
    comisiones.run()

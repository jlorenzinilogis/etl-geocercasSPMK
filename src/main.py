import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import os



def extract_report(df_plates, df_geocercas, desde, hasta):
    '''
    Función que extrae reporte.
    '''
    plates_list = list(df_plates["patente"])
    geofences_ids = list(df_geocercas["ID"])

    # Endpoint
    url = 'https://drivetech.pro/api/v1/get_geofences_events/'

    headers = {
        'Authorization': f'Token {os.environ.get("DRIVETECH_API_TOKEN")}', 
        'Content-Type': 'application/json'}
    
    payload = {
    "plates": plates_list, #["SVWB37", "SVBZ14", "LWDC16"]
    "start": desde, #"2025-06-25 04:00:00"
    "end": hasta, #"2025-06-25 05:00:00"
    "geofences": geofences_ids, #["5e21f2635b360d000ac79eb0", "5e21f569819bfa000f399982"]
    "min_permanence": 600
    }

    #Response
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        # Convertir respuesta a JSON
        json_data = response.json()

        # Verificamos que la respuesta indique éxito
        if json_data.get("success") and "data" in json_data:
            data = json_data["data"]

            # Convertimos cada lista de eventos en DataFrame y le agregamos la patente
            df = pd.concat([
                pd.DataFrame(events).assign(patente=plate)
                for plate, events in data.items()
            ], ignore_index=True)

        else:
            print("La respuesta no contiene datos válidos.")
    else:
        print(f"Error en la solicitud: {response.status_code}")

    return df


def transform_report(df_report):

    # Quedar con las columnas de interes.
    df_report = df_report.drop(columns = ["in","out","driver", "activeDispatches"])

    # Duración de segundo a horas.
    df_report["duration"]= (df_report["duration"]/3600).round(2)

    # Convertir datatime en formato fecha.
    #df_report["datetime"] = pd.to_datetime(df_report["datetime"], format="mixed").dt.date

    # Ordenar por fecha
    df_report = df_report.sort_values(by="patente", ascending = False)

    return df_report


def load_report(
    df: pd.DataFrame,
    table_name: str = "geofences",
    db_user: str = "postgres",
    db_pass: str = "Logis2021",
    db_host: str = "10.1.1.26",
    db_port: str = "5432",
    db_name: str = "geocercas_SPMK",
    update_on_conflict: bool = True  # True: actualiza; False: ignora duplicados
) -> int:
    """
    Inserta df en `table_name` evitando duplicados por (geofence, datetime, patente).
    Requiere UNIQUE (geofence, datetime, patente) en la tabla destino.
    Devuelve cantidad de filas procesadas.
    """
    from sqlalchemy.dialects.postgresql import insert
    from sqlalchemy import MetaData, Table

    # Conexión
    engine_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(engine_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(table_name, metadata, autoload_with=engine)

    # Inserción con manejo de duplicados
    rows_inserted = 0
    with engine.begin() as conn:
        for _, row in df.iterrows():
            insert_stmt = insert(table).values(row.to_dict())
            if update_on_conflict:
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=['geofence', 'datetime', 'patente'],
                    set_={'duration': row['duration']}
                )
                conn.execute(do_update_stmt)
            else:
                do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                    index_elements=['geofence', 'datetime', 'patente']
                )
                conn.execute(do_nothing_stmt)
            rows_inserted += 1

    return rows_inserted


def main():

    df_plates = pd.read_excel("../data/Patentes.xlsx")
    df_geocercas = pd.read_excel("../data/Geocercas.xlsx")

    start = datetime.now()  # Fecha de inicio, puede ser modificada según necesidad
    # Fecha de inicio, puede ser modificada según necesidad

    # Formato correcto: '%Y-%m-%d %H:%M:%S'
    start_str = start.strftime('%Y-%m-%d 00:00:00')
    end_str = start.strftime('%Y-%m-%d 23:59:59')

    

    df_report = extract_report(df_plates, df_geocercas, start_str, end_str)
    print(df_report.head(15))
    #df_report = transform_report(df_report)
    #print(df_report.head(15))
    #load_report(df_report,"geofences")


    return 0


main()


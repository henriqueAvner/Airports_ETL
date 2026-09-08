import os
from pathlib import Path
import csv
import psycopg
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)



class AirportsLoad():

  BASE_DIR = Path(__file__).resolve().parents[2]

  @staticmethod
  def get_connection():
    load_dotenv()

    conn = psycopg.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      dbname = os.getenv("DB_NAME"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      connect_timeout = 5
    )

    return conn

  @staticmethod
  def create_tables():
    logger.info("Iniciando criação / verificação das tabelas")

    try:
      
      SQL_FILE = AirportsLoad.BASE_DIR / "sql" / "create_table.sql"

      with open(SQL_FILE, "r", encoding="utf-8") as arquivosql:
        sql_script = arquivosql.read()

      with AirportsLoad.get_connection() as connection:
        with connection.cursor() as cursor:
          cursor.execute(sql_script)

        connection.commit()

      logger.info("Tabelas criadas / verificadas com sucesso")

    except Exception as e:
      logger.exception("Erro durante a criação / verificação das tabelas: ", e)
      raise

  @staticmethod
  def load_airports():
    logger.info("Iniciando carga de dados ao banco")
    connection = None
    cursor = None

    airports_csv = AirportsLoad.BASE_DIR / "data" / "processed" / "airports.csv"

    query = '''INSERT INTO airports (
      ciad,
      codigoOACI,
      airport_name,
      state,
      city,
      altitude,
      latgeopoint,
      longeopoint,
      latitude,
      longitude)
    VALUES (
      %s, %s, %s, %s, %s, %s, 
      %s, %s, %s, %s
    )
    ON CONFLICT(ciad)
    DO UPDATE SET
      codigoOACI = EXCLUDED.codigoOACI,
      airport_name = EXCLUDED.airport_name,
      state = EXCLUDED.state,
      city = EXCLUDED.city,
      altitude = EXCLUDED.altitude,
      latgeopoint = EXCLUDED.latgeopoint,
      longeopoint = EXCLUDED.longeopoint,
      latitude = EXCLUDED.latitude,
      longitude = EXCLUDED.longitude,
      updated_at = CURRENT_TIMESTAMP
      WHERE
      airports.codigoOACI IS DISTINCT FROM EXCLUDED.codigoOACI
      OR airports.airport_name IS DISTINCT FROM EXCLUDED.airport_name
      OR airports.state IS DISTINCT FROM EXCLUDED.state
      OR airports.city IS DISTINCT FROM EXCLUDED.city
      OR airports.altitude IS DISTINCT FROM EXCLUDED.altitude
      OR airports.latgeopoint IS DISTINCT FROM EXCLUDED.latgeopoint
      OR airports.longeopoint IS DISTINCT FROM EXCLUDED.longeopoint
      OR airports.latitude IS DISTINCT FROM EXCLUDED.latitude
      OR airports.longitude IS DISTINCT FROM EXCLUDED.longitude;
    '''
    try:
      with open(airports_csv, mode='r', encoding="utf-8") as arquivo:
        leitor_dict = csv.DictReader(arquivo, delimiter=',')

        connection = AirportsLoad.get_connection()
        cursor = connection.cursor()

        data_to_insert = [
          (
            row['ciad'],
            row['codigoOACI'],
            row['airport_name'],
            row['state'],
            row['city'],
            row['altitude'],
            row['latgeopoint'],
            row['longeopoint'],
            row['latitude'],
            row['longitude'],

          )
          for row in leitor_dict
        ]

        logger.info("Dados preparados para carga, registros = %s",
                     len(data_to_insert))

        if data_to_insert:
          cursor.executemany(query, data_to_insert)
          connection.commit()

          logger.info("Carga no PostgreSQL concluída, total = %s", 
                      len(data_to_insert))
        else:
          logger.warning("Nenhum registro encontrado no CSV para carga")
    except Exception as e:
      if connection:
        connection.rollback()
      logger.exception("Erro durante a carga ao postgreSQL: %s", e)
      raise
    finally:
      if cursor:
        cursor.close()
      if connection:
        connection.close()
from src.extract.extract import Extract
from src.transform.transform import Transform
from src.load.load import AirportsLoad
from src.utils.logger import setup_logger
import logging
import time

setup_logger()
logger = logging.getLogger(__name__)

def main():
  start_time = time.perf_counter()
  try:
    full_data = Extract.extract_data()
    logger.info("Dados extraídos com sucesso")

    Transform.transform_all_data(full_data)
    logger.info("Dados Transformados com sucesso")

    logger.info("Verificando a existência da tabela em banco")
    AirportsLoad.create_tables()

    logger.info("Carregando dados no PostgreSQL")
    AirportsLoad.load_airports()

    duration = time.perf_counter() - start_time

    logger.info(
        "Pipeline finalizado com sucesso, duração=%.2f segundos",
        duration
    )
    
  except Exception:
     duration = time.perf_counter() - start_time
     logger.exception(
        "Pipeline interrompido por erro, duração=%.2f segundos",
        duration)
     raise


if __name__ == "__main__":
  main()
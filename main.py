from src.extract.extract import Extract
from src.transform.transform import Transform
from src.utils.logger import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

def main():
  try:
    full_data = Extract.extract_data()
    logger.info("Dados extraídos com sucesso")

    Transform.transform_all_data(full_data)
    logger.info("Dados Transformados com sucesso")
    
  except Exception:
    logger.exception("Erro na execução do pipeline: ")


if __name__ == "__main__":
  main()
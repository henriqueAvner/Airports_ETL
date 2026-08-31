from src.extract.extract import Extract
from src.utils.logger import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

def main():
  try:
    Extract.extract_data()
  except Exception:
    logger.exception("Erro na execução do pipeline: ")






if __name__ == "__main__":
  main()
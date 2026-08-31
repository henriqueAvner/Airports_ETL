import requests
import json
import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
logger = logging.getLogger(__name__)

class Extract:
  def extract_data():
    url = "https://sistemas.anac.gov.br/dadosabertos/Aerodromos/Aeródromos%20Públicos/Lista%20de%20aeródromos%20públicos/AerodromosPublicos.json"
    DATA_RAW = RAW_DIR / "data_raw.json"
    logger.info("Iniciando extração dos dados de aeródromos públicos")
    try:
      resp = requests.get(url, timeout=10)
      resp.encoding = 'utf-8-sig'
      resp.raise_for_status()

      dados = resp.json()
      print(type(dados))
      json_formated = []

      for data in dados:
        json_formated.append(data)
      
      with open(DATA_RAW, 'w', encoding='utf-8') as all_data:
        json.dump(json_formated, all_data, indent=4, ensure_ascii=False)

      logger.info("Dados extraídos com sucesso! Aeródromos públicos: %s", len(json_formated))

      return json_formated
    except Exception as e:
      logger.exception("Erro ao extrair os dados: ", e)
      raise


from pathlib import Path
import re
import logging
import csv
import json

logger = logging.getLogger(__name__)

class Transform:

  BASE_DIR = Path(__file__).resolve().parents[2]

  @staticmethod
  def transform_raw(curr_raw):
    return {
      "ciad": curr_raw.get("CIAD"),
      "codigoOACI" : curr_raw.get("CódigoOACI"),
      "airport_name": curr_raw.get("Nome"),
      "state": curr_raw.get("UF"),
      "city":  curr_raw.get("Município"),
      "altitude": curr_raw.get("Altitude"),
      "latgeopoint": curr_raw.get("LatGeoPoint"),
      "longeopoint": curr_raw.get("LonGeoPoint"),
      "latitude": curr_raw.get("Latitude"),
      "longitude": curr_raw.get("Longitude"),
    }
  @staticmethod
  def transform_all_data(data):
    columns = ["ciad", "codigoOACI", "airport_name", "state",
                "city", "altitude", "latgeopoint", "longeopoint",
                  "latitude", "longitude"]

    dados_processados = Transform.BASE_DIR / "data" / "processed"
    dados_rejeitados = Transform.BASE_DIR / "data" / "rejected"

    dados_processados.mkdir(parents=True,  exist_ok = True)
    dados_rejeitados.mkdir(parents=True,  exist_ok = True)

    try:
       all_data = Transform.validate_data(data)

       logger.info("Iniciando a transformação dos dados, total: %s", len(data))

       processed_data, rejected_data = all_data

       logger.info("Processando %s dados aprovados", len(processed_data))
       Transform.save_processed_data(processed_data, columns)

       logger.info("Processando %s dados rejeitados", len(rejected_data))
       Transform.save_rejected_data(rejected_data)
    except Exception as e:
       logger.exception("Transformaçao concluída, válidos=%s, rejeitados=%s",
                        len(processed_data), len(rejected_data))



  @staticmethod
  def validate_data(data):
    processed_data = []
    rejected_data = []

    for dado in data:
      curr_data = Transform.transform_raw(dado)
      reasons = []
      ciad = curr_data.get("ciad")
      lat_raw = curr_data.get("latgeopoint")
      lon_raw = curr_data.get("longeopoint")

      if not ciad or len(ciad) != 6:
        reasons.append("ciad com tamanho inválido")
      elif not re.match(r"^[A-Z]{2}\d{4}$", ciad.strip()):
        reasons.append("Padrão ciad invalido: 2 letras + 4 números")

      if curr_data.get("codigoOACI") is None:
        reasons.append("CódigoOACI ausente")
      elif len(curr_data.get("codigoOACI")) != 4:
        reasons.append("CódigoOACI inválido")

      if curr_data.get("airport_name") is None:
        reasons.append("Nome do aeroporto vazio")

      if curr_data.get("state") is None:
        reasons.append("Nome do estado do aeroporto ausente")

      if curr_data.get("city") is None:
        reasons.append("Nome da cidade do aeroporto ausente")

      try:
        lat = float(lat_raw)
        if not (-34.0 <= lat <= +6.0):
            reasons.append("latgeopoint fora do intervalo global (-34.0 a -34.0)")
      except (ValueError, TypeError):
        reasons.append("latgeopoint deve ser um número válido")
        raise

      try:
          lon = float(lon_raw)
          if not (-180.0 <= lon <= 180.0):
              reasons.append("longeopoint fora do intervalo global (-180 a 180)")
          elif lon >= 0:
              reasons.append("longeopoint inválida: aeródromo no Brasil deve ter longitude negativa")
      except (ValueError, TypeError):
          reasons.append("longeopoint deve ser um número válido")
          raise

      if len(reasons) > 0:
        rejected_data.append({"reasons": reasons, "record": curr_data})
      else:
         processed_data.append(curr_data)

    if rejected_data:
       logger.warning("Foram encontrados %s registros inválidos", len(rejected_data))

    return [processed_data, rejected_data]


  #Criar métodos para salvar dados rejeitados e dados aceitos, e seguir linha 41
  @staticmethod
  def save_processed_data(processed_data, colunas):
    PROCESSED_DIR = Transform.BASE_DIR / "data" / "processed" / "airports.csv"
    try:
      with open(PROCESSED_DIR, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(processed_data)
      logger.info("Dados  processados e gravados em: %s", PROCESSED_DIR)
    except Exception as e:
       logger.exception("Erro ao gravar dados processados: ", e)
       raise

    
  @staticmethod
  def save_rejected_data(rejected_data):
    REJECTED_DIR = Transform.BASE_DIR / "data" / "rejected" / "rejected.json"
    try:
        with open(REJECTED_DIR, 'w', encoding="utf-8") as file:
          json.dump(rejected_data, file, ensure_ascii=False, indent=4)

        logger.info("Dados rejeitados gravados em: %s", REJECTED_DIR)
    except Exception as e:
       logger.exception("Erro ao gravar dados rejeitados em json: ", e)
       raise

       

         

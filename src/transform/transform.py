from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)

class Transform:

  BASSE_DIR = Path(__file__).resolve().parents[2]

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

  def transform_data(data):
    columns = ["ciad", "codigoOACI", "airport_name", "state",
                "city", "altitude", "latgeopoint", "longeopoint",
                  "latitude", "longitude"]

    processed_data = Transform.BASE_DIR / "data" / "processed"
    rejected_data = Transform.BASE_DIR / "data" / "rejected"

    processed_data.mkdir(parents=True,  exist_ok = True)
    rejected_data.mkdir(parents=True,  exist_ok = True)

    try:
       all_data = Transform.validate_data(data)

       logger.info("Iniciando a transformação dos dados, total: %s", len(all_data))

       processed_data, rejected_data = all_data


    except Exception as e:
       logger.exception("Transformaçao concluída, válidos=%s, rejeitados=%s",
                        len(processed_data), len(rejected_data))




  def validate_data(data):
    processed_data = []
    rejected_data = []

    for dado in data:
      curr_data = Transform.transform_raw(dado)
      reasons = []
      ciad = dado.get("ciad")
      lat_raw = dado.get("latgeopoint")
      lon_raw = dado.get("longeopoint")

      if not ciad or len(ciad) != 6:
        reasons.append("ciad com tamanho inválido")
      elif not re.match(r"^[A-Z]{2}\d{4}$", ciad.strip()):
        reasons.append("Padrão ciad invalido: 2 letras + 4 números")

      if dado.get("codigoOACI") is None:
        reasons.append("CódigoOACI ausente")
      elif len(dado.get("codigoOACI")) != 4:
        reasons.append("CódigoOACI inválido")

      if dado.get("airport_name") is None:
        reasons.append("Nome do aeroporto vazio")

      if dado.get("state") is None:
        reasons.append("Nome do estado do aeroporto ausente")

      if dado.get("city") is None:
        reasons.append("Nome da cidade do aeroporto ausente")

      try:
        lat = float(lat_raw)
        if not (-90.0 <= lat <= 90.0):
            reasons.append("latgeopoint fora do intervalo global (-90 a 90)")
        elif lat >= 0:
            reasons.append("latgeopoint inválida: aeródromo no Brasil deve ter latitude negativa")
      except (ValueError, TypeError):
        reasons.append("latgeopoint deve ser um número válido")

      try:
          lon = float(lon_raw)
          if not (-180.0 <= lon <= 180.0):
              reasons.append("longeopoint fora do intervalo global (-180 a 180)")
          elif lon >= 0:
              reasons.append("longeopoint inválida: aeródromo no Brasil deve ter longitude negativa")
      except (ValueError, TypeError):
          reasons.append("longeopoint deve ser um número válido")

      if len(reasons) > 0:
        rejected_data.append({"reasons": reasons, "record": curr_data})
      else:
         processed_data.append(curr_data)

    if rejected_data:
       logger.waring("Foram encontrados %s registros inválidos", len(rejected_data))

    return [processed_data, rejected_data]



  #Criar métodos para salvar dados rejeitados e dados aceitos, e seguir linha 41
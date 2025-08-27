from io import StringIO
import logging
import logging.handlers
import os
import requests
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

dataSource = {
    "url": "https://geoegl.msp.gouv.qc.ca/apis/wss/historiquesc.fcgi?service=wfs&version=1.1.0&request=getfeature&typename=msp_risc_evenements_public&outputformat=CSV",
    "format": "csv",
    "metadata_url": "https://www.donneesquebec.ca/recherche/dataset/evenements-de-securite-civile/resource/8a707be3-2452-43b2-be72-fb5926876c72",
    "updatedAt": "2025-05-09 09:40Z",
    "identifier": "8a707be3-2452-43b2-be72-fb5926876c72",
}

# %%
try:
    response = requests.get(dataSource["url"])
    response.raise_for_status()
    # Read the CSV data into a Pandas DataFrame
    csv_data = StringIO(response.text)
    rawDataframe = pd.read_csv(csv_data)
    logger.info(f"Fetched {len(rawDataframe)} records from {dataSource['url']}")
except Exception as e:
    logger.error(f'Error fetching data: {e}')
import json
import logging
import os
import sys
import azure.functions as func
 
# Add ...\app to sys.path so we can import app\Ingestion.py
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
 
from Ingestion import ingest_blob_by_name  # your file is app/Ingestion.py
 
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "rag-documents")
 
def main(msg: func.QueueMessage) -> None:
    payload = json.loads(msg.get_body().decode("utf-8"))
    blob_path = payload.get("blob_path")
    corr = payload.get("correlation_id", "na")
 
    if not blob_path:
        logging.error("[QueueIndexer] Missing blob_path in queue message")
        return
 
    prefix = f"{CONTAINER_NAME}/"
    blob_name = blob_path[len(prefix):] if blob_path.startswith(prefix) else blob_path
 
    logging.info(f"[QueueIndexer] START blob_name={blob_name}, corr={corr}")
    ingest_blob_by_name(blob_name)
    logging.info(f"[QueueIndexer] SUCCESS blob_name={blob_name}, corr={corr}")
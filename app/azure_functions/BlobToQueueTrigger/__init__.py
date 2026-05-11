import json
import logging
import uuid
from datetime import datetime
import azure.functions as func
 
def main(blob: func.InputStream, msg: func.Out[str]) -> None:
    logging.info(f"[BlobToQueueTrigger] Blob detected: {blob.name} ({blob.length} bytes)")
 
    payload = {
        "blob_path": blob.name,
        "event_time": datetime.utcnow().isoformat() + "Z",
        "correlation_id": str(uuid.uuid4())
    }
 
    msg.set(json.dumps(payload))
    logging.info(f"[BlobToQueueTrigger] Enqueued message for: {blob.name}")
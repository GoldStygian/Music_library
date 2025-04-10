import logging

logging.basicConfig(
    filename='app.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

logger.info("Start server app")
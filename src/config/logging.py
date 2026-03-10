import logging

from loguru import logger

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

socketio_file_handler = logging.FileHandler('logs/socketio.log')
socketio_file_handler.setFormatter(formatter)

socketio_logger = logging.getLogger('socketio')
socketio_logger.setLevel(logging.INFO)
socketio_logger.addHandler(socketio_file_handler)

logger.add(
    'logs/transcription.log',
    format='{time} {level} {message}',
    filter=lambda record: record['extra'].get('service') == 'transcription',
    rotation='00:00',
    retention='7 days',
    compression='zip',
    enqueue=True,
)

transcription_logger = logger.bind(service='transcription')

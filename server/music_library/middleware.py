import os
import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RangesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Verifica se la risposta è 200 e contiene un file da streammare
        if response.status_code != 200 or not hasattr(response, 'file_to_stream'):
            return response

        # Gestione della richiesta Range
        http_range = request.META.get('HTTP_RANGE')
        if not (http_range and http_range.startswith('bytes=') and http_range.count('-') == 1):
            return response

        # Verifica If-Range
        if_range = request.META.get('HTTP_IF_RANGE')
        if if_range and if_range != response.get('Last-Modified') and if_range != response.get('ETag'):
            return response

        f = response.file_to_stream
        try:
            statobj = os.fstat(f.fileno())
        except Exception as e:
            logger.error(f"Error while fetching file stats: {e}")
            return response

        # Calcolo del range
        start, end = http_range.split('=')[1].split('-')
        if not start:  # Gestione del caso in cui si richiedono gli ultimi N byte
            start = max(0, statobj.st_size - int(end))
            end = ''
        start, end = int(start or 0), int(end or statobj.st_size - 1)

        if start < 0 or start >= statobj.st_size:
            logger.error(f"Invalid start range: {start} for file size: {statobj.st_size}")
            response.status_code = 416
            response['Content-Range'] = f'bytes */{statobj.st_size}'
            return response

        # Definisce il range finale da servire
        end = min(end, statobj.st_size - 1)
        f.seek(start)
        old_read = f.read

        f.read = lambda n: old_read(min(n, end + 1 - f.tell()))

        # Modifica la risposta con status 206
        response.status_code = 206
        response['Content-Length'] = end + 1 - start
        response['Content-Range'] = f'bytes {start}-{end}/{statobj.st_size}'
        # logger.debug(f"Serving range {start}-{end} for file with size {statobj.st_size}")

        return response

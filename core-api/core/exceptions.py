# core-api/core/exceptions.py

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_code = exc.__class__.__name__
        message_data = response.data

        # Extrai detalhes de erro se for formato de dicionário
        if isinstance(message_data, dict) and 'detail' in message_data:
            message_detail = message_data['detail']
        else:
            message_detail = message_data

        response.data = {
            "error": error_code,
            "message": message_detail
        }

    return response
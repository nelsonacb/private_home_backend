from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Manejador global de excepciones para DRF.
    Devuelve respuestas de error con formato consistente.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Personalizar el formato del error
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail', 'Error'),
                'details': response.data
            }
        }
        response.data = custom_response_data
    else:
        # Para excepciones no manejadas (500)
        custom_response_data = {
            'success': False,
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error interno del servidor',
                'details': str(exc)
            }
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
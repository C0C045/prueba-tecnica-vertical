import requests
from fastapi import HTTPException, status

BASE_URL = "https://jsonplaceholder.typicode.com"

def get_posts():
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="El servicio externo tardó demasiado en responder."
        )
    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=response.status_code if 'response' in locals() else status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en la respuesta del servicio externo: {str(e)}"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar con el servicio externo."
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al consultar el servicio externo: {str(e)}"
        )

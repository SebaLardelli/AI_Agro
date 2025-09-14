import requests
from IPython.display import Markdown


# Almacena el valor de latitud en la variable 'lat'

lat = -34.6037  # Buenos Aires, Argentina

# Almacena el valor de longitud en la variable 'lon'
lon = -58.3816

# Almacena el valor de tu clave unica

api_key = userdata.get("OPEN_WEATHER_API_KEY")

url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt=1&lat={lat}&lon={lon}&appid={api_key}"

# Usa la función get de la biblioteca requests para almacenar la respuesta de la API
response = requests.get(url)

# Toma la respuesta de la API (en JSON) y asígnala a un diccionario de Python
data = response.json()

# Imprime
print(data)
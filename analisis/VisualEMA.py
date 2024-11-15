import os
import pandas as pd
from datetime import datetime
from datos import APITiingo, APIStub
from Mean import CalculadoraDePromedios
import matplotlib.pyplot as plt

tickers = []  
fecha_inicio = datetime(2020, 1, 1)
fecha_fin = datetime(2023, 10, 17)
clave_api_tiingo = os.environ.get('TIINGO_API_KEY') 
api = APITiingo(clave_api_tiingo)
datos = api.obtener_datos(tickers, fecha_inicio, fecha_fin)
#INSTA
calculadora = CalculadoraDePromedios(datos)

print("Tickers disponibles: ", ", ".join(tickers))
columna = input("Ticker para EMA: ").strip().upper()

if columna in tickers:
    
    ema = calculadora.media_movil_exponencial(columna, span=20)
    plt.figure(figsize=(10,6))
    plt.plot(ema.index, ema.values, label=f'EMA (span de 20) para {columna}')
    plt.title(f'Media Móvil Exponencial para {columna}')
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid(True)
    plt.show()

else:
    print(f"El ticker '{columna}' no está en la lista de tickers disponibles.")

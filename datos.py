import requests
import pandas as pd
from datetime import datetime

class APITiingo:
    def __init__(self, tiingo_api_key):
        self.tiingo_api_key = tiingo_api_key

    def obtener_datos(self, tickers, fecha_inicio, fecha_fin):
        datos_tiingo = {}
        
        for ticker in tickers:
            url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={fecha_inicio.strftime('%Y-%m-%d')}&endDate={fecha_fin.strftime('%Y-%m-%d')}&token={self.tiingo_api_key}"
    
            try:
                respuesta = requests.get(url, timeout=10)
                respuesta.raise_for_status()
                datos = respuesta.json()
                df = pd.DataFrame(datos)
                df['fecha'] = pd.to_datetime(df['date'])
                df.set_index('fecha', inplace=True)
                datos_tiingo[ticker] = df['adjClose']
            except requests.RequestException as e:
                print(f"Error al obtener datos para {ticker}: {e}")
                
        return pd.DataFrame(datos_tiingo)

class APIStub: 
    def __init__(self):
        pass

    def obtener_datos(self, tickers, fecha_inicio, fecha_fin):
        df = pd.read_pickle("./stub2.pk1")
        df['fecha'] = pd.to_datetime(df['date'])
        df.set_index('fecha', inplace=True)
        return df['adjClose']

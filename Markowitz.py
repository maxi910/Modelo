import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def principal():
    clave_api_quandl = os.environ.get('QUANDL_API_KEY')
    clave_api_tiingo = os.environ.get('TIINGO_API_KEY')

    try:
        tasa_libre_riesgo = obtener_tasa_libre_riesgo(clave_api_quandl)
        print(f"Tasa libre de riesgo (bonos del tesoro a 3 meses de EE. UU.): {tasa_libre_riesgo}%")
    except ValueError as e:
        print(e)
        return

    tickers = ['ENB', 'AAPL', 'ADBE', 'ALB', 'AMD'] 
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=5*365)

    dataframes = []
    for ticker in tickers:
        try:
            df = obtener_datos_tiingo(ticker, fecha_inicio, fecha_fin, clave_api_tiingo)
            dataframes.append(df)
        except ValueError as e:
            print(e)

    datos = pd.concat(dataframes, axis=1, keys=tickers)
    retornos = datos.ffill().pct_change().dropna()
    retornos_promedio = retornos.mean()
    matriz_cov = retornos.cov()

    num_portafolios = 100000
    resultados = np.zeros((3 + len(tickers), num_portafolios))
    for i in range(num_portafolios):
        pesos = np.random.random(len(tickers))
        pesos /= np.sum(pesos)
        
        retorno_portafolio = np.sum(retornos_promedio * pesos)
        desviacion_estandar_portafolio = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
        ratio_sharpe = (retorno_portafolio - tasa_libre_riesgo) / desviacion_estandar_portafolio if tasa_libre_riesgo else 0
        
        resultados[0,i] = retorno_portafolio
        resultados[1,i] = desviacion_estandar_portafolio
        resultados[2,i] = ratio_sharpe
        for j in range(len(pesos)):
            resultados[j+3,i] = pesos[j]

    capital_total = 2500  
    inversiones = {ticker: capital_total * peso for ticker, peso in zip(tickers, resultados[3:,resultados[2].argmax()])}

    # Suponiendo que tienes un diccionario con los betas de cada acción y el retorno esperado del mercado
    betas = {'ENB': 1.2, 'AAPL': 1.1, 'ADBE': 1.3, 'ALB': 1.0, 'AMD': 1.5}  # Ejemplo, reemplaza con los betas reales
    retorno_mercado = 0.1  # Ejemplo, reemplaza con el retorno esperado real del mercado

    print("Cantidad por acción y CAPM:")
    for ticker, inversion in inversiones.items():
        beta = betas.get(ticker, None)  # Obtener el beta de la acción, o None si no está disponible
        if beta is not None:
            capm = calcular_capm(tasa_libre_riesgo, beta, retorno_mercado)
            print(f"{ticker}: ${inversion:.2f}, CAPM: {capm*100:.2f}%")
        else:
            print(f"No se encontró el beta para {ticker}.")

    # Obtener el retorno del portafolio para el portafolio con el ratio Sharpe más alto
    mejor_retorno_portafolio = resultados[0, resultados[2].argmax()]

    # Calcular retornos esperados durante 1, 2 y 3 años
    retorno_esperado_1año = calcular_retorno_esperado(mejor_retorno_portafolio, 1)
    retorno_esperado_2años = calcular_retorno_esperado(mejor_retorno_portafolio, 2)
    retorno_esperado_3años = calcular_retorno_esperado(mejor_retorno_portafolio, 3)

    print("\nRetorno Esperado del Portafolio:")
    print(f"1 Año: {retorno_esperado_1año * 100:.2f}%")
    print(f"2 Años: {retorno_esperado_2años * 100:.2f}%")
    print(f"3 Años: {retorno_esperado_3años * 100:.2f}%")

if __name__ == "__main__":
    principal()
import yfinance as yf          
import pandas as pd          
import matplotlib.pyplot as plt
import seaborn as sns          # Visualización estadística avanzada
import requests             
import json   
import numpy as np 
import os 
import warnings
warnings.filterwarnings('ignore')          
from datetime import datetime, timedelta  
from rich.console import Console
from rich.markdown import Markdown 
from dotenv import load_dotenv 
from google import genai
from google.genai import types

load_dotenv() 

console = Console()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

cliente_gemini = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_ID = "gemini-2.0-flash" 

def analizar_con_gemini(prompt):
    response = cliente_gemini.models.generate_content(
        model=MODEL_ID,
        contents=[prompt]
    )
    return response.text


# print("Google Gemini API configurada correctamente")
# print(f"Modelo seleccionado: {MODEL_ID}")
# print("Función: Análisis inteligente de datos financieros agrícolas")

# def analizar_con_gemini(prompt):
#     """
#     Función para enviar consultas a Google Gemini y obtener análisis.

#     Parámetros:
#     prompt (str): La consulta o instrucción para el modelo de IA

#     Retorna:
#     str: La respuesta generada por Gemini
#     """
#     response = cliente_gemini.models.generate_content(
#         model=MODEL_ID,
#         contents=[prompt]
#     )
#     return response.text

# print("Función analizar_con_gemini() lista para usar")

"""## Obtención de Cotizaciones de Commodities Agrícolas

   ## Definición de los mercados a monitorear """

# Definición de commodities agrícolas principales y sus símbolos de mercado
commodities_agricolas = {
    'Soja': 'ZS=F',      # Soybean Futures - Chicago Board of Trade (CBOT)
    'Maíz': 'ZC=F',     # Corn Futures - CBOT
    'Trigo': 'ZW=F',    # Wheat Futures - CBOT
    'Dólar': 'USDARS=X' # Tipo de cambio USD/ARS
}

def obtener_cotizaciones_actuales():
    """
    Función para obtener las cotizaciones actuales de los commodities agrícolas.

    Esta función:
    1. Conecta con la API de Yahoo Finance
    2. Obtiene los precios actuales y del día anterior
    3. Calcula la variación porcentual diaria
    4. Maneja errores de conectividad o datos faltantes

    Retorna:
    dict: Diccionario con las cotizaciones y variaciones de cada commodity
    """
    cotizaciones = {}

    # Iteramos sobre cada commodity definido
    for nombre, simbolo in commodities_agricolas.items():
        try:
            print(f"Obteniendo datos para {nombre} ({simbolo})...")

            # Crear objeto ticker de Yahoo Finance
            ticker = yf.Ticker(simbolo)

            # Obtener información general del instrumento
            info = ticker.info

            # Obtener datos históricos del último día de trading
            hist = ticker.history(period='5d')

            if not hist.empty:
                # Extraer precios relevantes
                precio_actual = hist['Close'].iloc[-1]  # Precio de cierre
                precio_anterior = hist['Open'].iloc[-1] # Precio de apertura

                # Calcular variación porcentual
                variacion = ((precio_actual - precio_anterior) / precio_anterior) * 100

                # Almacenar resultados
                cotizaciones[nombre] = {
                    'precio': precio_actual,
                    'variacion': variacion,
                    'simbolo': simbolo
                }
                print(f"✓ {nombre}: ${precio_actual:.2f} ({variacion:+.2f}%)")
            else:
                print(f"⚠ Warning: No se encontraron datos para {nombre}")

        except Exception as e:
            print(f"✗ Error obteniendo {nombre}: {str(e)}")
            # Continuamos con el siguiente commodity aunque uno falle

    return cotizaciones

# Ejecutar la función para obtener cotizaciones actuales
print("Iniciando descarga de cotizaciones...")
cotizaciones_actuales = obtener_cotizaciones_actuales()

# Mostrar resultados formateados
print("\n" + "=" * 50)
print("COTIZACIONES ACTUALES - COMMODITIES AGRÍCOLAS")
print("=" * 50)

for commodity, datos in cotizaciones_actuales.items():
    precio = datos['precio']
    variacion = datos['variacion']

    # Determinar símbolo de tendencia
    if variacion > 0:
        tendencia = "↗ (Subida)"
    elif variacion < 0:
        tendencia = "↘ (Bajada)"
    else:
        tendencia = "→ (Sin cambio)"

    # Formatear salida según el tipo de commodity
    if commodity == 'Dólar':
        print(f"{commodity:8}: ${precio:8.2f} ARS {tendencia} ({variacion:+5.2f}%)")
    else:
        print(f"{commodity:8}: ${precio:8.2f} USD/bu {tendencia} ({variacion:+5.2f}%)")

print(f"\nÚltima actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nNotas:")
print("- Precios en dólares por bushel (bu) para granos")
print("- Tipo de cambio en pesos argentinos por dólar")
print("- Variación calculada respecto a la apertura del día")

""" Resultado """

# Iniciando descarga de cotizaciones...
# Obteniendo datos para Soja (ZS=F)...
# ✓ Soja: $1046.25 (+0.31%)
# Obteniendo datos para Maíz (ZC=F)...
# ✓ Maíz: $430.00 (+0.88%)
# Obteniendo datos para Trigo (ZW=F)...
# ✓ Trigo: $523.50 (+0.14%)
# Obteniendo datos para Dólar (USDARS=X)...
# ✓ Dólar: $1453.00 (+0.00%)

# ==================================================
# COTIZACIONES ACTUALES - COMMODITIES AGRÍCOLAS
# ==================================================
# Soja    : $ 1046.25 USD/bu ↗ (Subida) (+0.31%)
# Maíz    : $  430.00 USD/bu ↗ (Subida) (+0.88%)
# Trigo   : $  523.50 USD/bu ↗ (Subida) (+0.14%)
# Dólar   : $ 1453.00 ARS → (Sin cambio) (+0.00%)

# Última actualización: 2025-09-14 23:02:50

# Notas:
# - Precios en dólares por bushel (bu) para granos
# - Tipo de cambio en pesos argentinos por dólar
# - Variación calculada respecto a la apertura del día

"""## Análisis de Tendencias Históricas

   ## Importancia del contexto histórico

Para tomar decisiones comerciales informadas, es crucial entender no solo el precio actual, sino también:
- **Tendencia a largo plazo**: ¿Los precios van en alza o baja?
- **Volatilidad**: ¿Qué tan inestables son los precios?
- **Niveles históricos**: ¿El precio actual es alto o bajo comparado con el pasado?
- **Patrones estacionales**: ¿Hay épocas del año más favorables para vender?"""

# Obtención de datos históricos para análisis de tendencias
periodo_analisis = '6mo'  # Analizamos los últimos 6 meses
datos_historicos = {}

print(f"Descargando datos históricos ({periodo_analisis})...")

# Obtener datos históricos para cada commodity
for nombre, simbolo in commodities_agricolas.items():
    try:
        print(f"Procesando {nombre}...")
        ticker = yf.Ticker(simbolo)

        # Obtener datos históricos
        # period puede ser: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        hist = ticker.history(period=periodo_analisis)

        if not hist.empty:
            # Guardamos solo los precios de cierre para el análisis
            datos_historicos[nombre] = hist['Close']
            print(f"✓ {nombre}: {len(hist)} datos históricos obtenidos")
        else:
            print(f"⚠ {nombre}: Sin datos históricos disponibles")

    except Exception as e:
        print(f"✗ Error con {nombre}: {e}")

print(f"\nDatos históricos obtenidos para {len(datos_historicos)} commodities")

# Descargando datos históricos (6mo)...
# Procesando Soja...
# ✓ Soja: 127 datos históricos obtenidos
# Procesando Maíz...
# ✓ Maíz: 127 datos históricos obtenidos
# Procesando Trigo...
# ✓ Trigo: 127 datos históricos obtenidos
# Procesando Dólar...
# ✓ Dólar: 129 datos históricos obtenidos

# Datos históricos obtenidos para 4 commodities


""" ### Visualización de tendencias

Creamos gráficos que nos permiten visualizar rápidamente:
1. **Evolución temporal** de cada precio
2. **Líneas de tendencia** para identificar la dirección general
3. **Comparación visual** entre diferentes commodities """

if datos_historicos:
    print("Generando gráficos de tendencias...")

    # Configurar el layout de subgráficos (2x2)
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()  # Convertir matriz 2x2 en array 1D para fácil iteración

    # Colores para cada gráfico
    colores = ['blue', 'green', 'orange', 'red']

    for i, (commodity, precios) in enumerate(datos_historicos.items()):
        if i < len(axes):  # Verificar que no excedamos el número de subgráficos
            # Graficar la serie de precios
            axes[i].plot(precios.index, precios.values,
                        color=colores[i], linewidth=2, label=commodity)

            # Configurar títulos y etiquetas
            axes[i].set_title(f'{commodity} - Evolución Últimos 6 Meses',
                            fontsize=12, fontweight='bold')

            # Etiqueta del eje Y según el tipo de commodity
            if commodity == 'Dólar':
                axes[i].set_ylabel('Pesos Argentinos por USD')
            else:
                axes[i].set_ylabel('Precio USD por Bushel')

            # Configurar grilla para mejor lectura
            axes[i].grid(True, alpha=0.3)
            axes[i].tick_params(axis='x', rotation=45)  # Rotar fechas 45°

            # Calcular y agregar línea de tendencia
            # Convertimos las fechas a números para el cálculo de regresión lineal
            x_numeric = range(len(precios))
            # Calcular coeficientes de regresión lineal (pendiente e intercepto)
            coeficientes = np.polyfit(x_numeric, precios.values, 1)
            # Crear función polinomial de grado 1 (línea recta)
            linea_tendencia = np.poly1d(coeficientes)
            # Graficar línea de tendencia
            axes[i].plot(precios.index, linea_tendencia(x_numeric),
                        "r--", alpha=0.8, linewidth=1, label='Tendencia')

            # Agregar leyenda
            axes[i].legend()

            # Interpretar la pendiente de la tendencia
            pendiente = coeficientes[0]
            if pendiente > 0:
                tendencia_texto = "Tendencia: ALCISTA"
            elif pendiente < 0:
                tendencia_texto = "Tendencia: BAJISTA"
            else:
                tendencia_texto = "Tendencia: LATERAL"

            # Agregar texto explicativo
            axes[i].text(0.02, 0.98, tendencia_texto,
                        transform=axes[i].transAxes,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Ajustar espaciado entre subgráficos
    plt.tight_layout()
    plt.show()

    print("Gráficos generados exitosamente")
    print("\nInterpretación:")
    print("- Línea azul/verde/naranja/roja: Precio histórico")
    print("- Línea roja punteada: Línea de tendencia")
    print("- Pendiente ascendente: Tendencia alcista (precios subiendo)")
    print("- Pendiente descendente: Tendencia bajista (precios bajando)")
else:
    print("No se pudieron generar gráficos - datos históricos no disponibles")

""" Resultado """

# Generando gráficos de tendencias...
# Gráficos generados exitosamente

# Interpretación:
# - Línea azul/verde/naranja/roja: Precio histórico
# - Línea roja punteada: Línea de tendencia
# - Pendiente ascendente: Tendencia alcista (precios subiendo)
# - Pendiente descendente: Tendencia bajista (precios bajando)

"""### Análisis estadístico de precios

Calculamos métricas estadísticas clave para entender mejor la posición actual de cada commodity:

- **Percentil**: Indica qué porcentaje del tiempo histórico el precio actual es mayor
- **Volatilidad**: Mide la variabilidad de los precios (riesgo)
- **Máximos y mínimos**: Referencias para evaluar oportunidades """

# Análisis estadístico detallado de los precios
if datos_historicos:
    resumen_estadistico = {}

    print("Calculando métricas estadísticas...")

    for commodity, precios in datos_historicos.items():
        # Métricas básicas
        precio_actual = precios.iloc[-1]     # Último precio disponible
        precio_maximo = precios.max()        # Precio máximo del período
        precio_minimo = precios.min()        # Precio mínimo del período
        precio_promedio = precios.mean()     # Precio promedio

        # Métricas de volatilidad
        volatilidad = precios.std()          # Desviación estándar

        # Calcular percentil actual
        # Esto nos dice qué porcentaje del tiempo histórico el precio fue menor al actual
        percentil = (precios <= precio_actual).mean() * 100

        # Calcular retorno total del período
        retorno_total = ((precio_actual - precios.iloc[0]) / precios.iloc[0]) * 100

        # Almacenar todas las métricas
        resumen_estadistico[commodity] = {
            'actual': precio_actual,
            'máximo_6m': precio_maximo,
            'mínimo_6m': precio_minimo,
            'promedio_6m': precio_promedio,
            'volatilidad': volatilidad,
            'percentil': percentil,
            'retorno_total': retorno_total
        }

    # Mostrar resumen estadístico detallado
    print("\n" + "=" * 60)
    print("ANÁLISIS ESTADÍSTICO DETALLADO (ÚLTIMOS 6 MESES)")
    print("=" * 60)

    for commodity, stats in resumen_estadistico.items():
        print(f"\n{commodity.upper()}:")
        print(f"  Precio actual: ${stats['actual']:.2f}")
        print(f"  Rango histórico: ${stats['mínimo_6m']:.2f} - ${stats['máximo_6m']:.2f}")
        print(f"  Precio promedio: ${stats['promedio_6m']:.2f}")
        print(f"  Volatilidad (desv. std): ${stats['volatilidad']:.2f}")
        print(f"  Percentil actual: {stats['percentil']:.1f}%")
        print(f"  Retorno del período: {stats['retorno_total']:+.1f}%")

        # Interpretación del percentil para decisiones comerciales
        if stats['percentil'] > 75:
            evaluacion = "PRECIO ALTO - Favorable para venta"
            color = "🔴"
        elif stats['percentil'] < 25:
            evaluacion = "PRECIO BAJO - Considerar retención o compra"
            color = "🟢"
        else:
            evaluacion = "PRECIO MEDIO - Evaluar estrategia específica"
            color = "🟡"

        print(f"  Evaluación comercial: {color} {evaluacion}")

        # Análisis de volatilidad
        coef_variacion = (stats['volatilidad'] / stats['promedio_6m']) * 100
        if coef_variacion > 15:
            riesgo = "ALTA volatilidad - Mayor riesgo/oportunidad"
        elif coef_variacion > 8:
            riesgo = "MEDIA volatilidad - Riesgo moderado"
        else:
            riesgo = "BAJA volatilidad - Precio más estable"

        print(f"  Análisis de riesgo: {riesgo} (CV: {coef_variacion:.1f}%)")

    print("\n" + "=" * 60)
    print("INTERPRETACIÓN DE MÉTRICAS:")
    print("- Percentil 90-100%: Precio cerca de máximos históricos")
    print("- Percentil 0-10%: Precio cerca de mínimos históricos")
    print("- Coeficiente de Variación (CV): Volatilidad relativa al precio promedio")
    print("- Retorno del período: Ganancia/pérdida desde el inicio del análisis")
else:
    print("No se pueden calcular estadísticas sin datos históricos")

""" Resultado """

# Calculando métricas estadísticas...

# ============================================================
# ANÁLISIS ESTADÍSTICO DETALLADO (ÚLTIMOS 6 MESES)
# ============================================================

# SOJA:
#   Precio actual: $1046.25
#   Rango histórico: $961.50 - $1074.75
#   Precio promedio: $1025.97
#   Volatilidad (desv. std): $26.51
#   Percentil actual: 75.6%
#   Retorno del período: +4.7%
#   Evaluación comercial: 🔴 PRECIO ALTO - Favorable para venta
#   Análisis de riesgo: BAJA volatilidad - Precio más estable (CV: 2.6%)

# MAÍZ:
#   Precio actual: $430.00
#   Rango histórico: $371.50 - $490.25
#   Precio promedio: $429.12
#   Volatilidad (desv. std): $32.40
#   Percentil actual: 46.5%
#   Retorno del período: -3.5%
#   Evaluación comercial: 🟡 PRECIO MEDIO - Evaluar estrategia específica
#   Análisis de riesgo: BAJA volatilidad - Precio más estable (CV: 7.5%)

# TRIGO:
#   Precio actual: $523.50
#   Rango histórico: $495.00 - $574.25
#   Precio promedio: $529.69
#   Volatilidad (desv. std): $18.03
#   Percentil actual: 35.4%
#   Retorno del período: -4.1%
#   Evaluación comercial: 🟡 PRECIO MEDIO - Evaluar estrategia específica
#   Análisis de riesgo: BAJA volatilidad - Precio más estable (CV: 3.4%)

# DÓLAR:
#   Precio actual: $1453.00
#   Rango histórico: $1066.04 - $1453.00
#   Precio promedio: $1211.83
#   Volatilidad (desv. std): $100.44
#   Percentil actual: 100.0%
#   Retorno del período: +36.1%
#   Evaluación comercial: 🔴 PRECIO ALTO - Favorable para venta
#   Análisis de riesgo: MEDIA volatilidad - Riesgo moderado (CV: 8.3%)

# ============================================================
# INTERPRETACIÓN DE MÉTRICAS:
# - Percentil 90-100%: Precio cerca de máximos históricos
# - Percentil 0-10%: Precio cerca de mínimos históricos
# - Coeficiente de Variación (CV): Volatilidad relativa al precio promedio
# - Retorno del período: Ganancia/pérdida desde el inicio del análisis

""" ## Integración con Inteligencia Artificial: Análisis Comercial

### ¿Por qué usar IA para análisis financiero?

La inteligencia artificial nos permite:
1. **Procesar múltiples variables simultáneamente**
2. **Identificar patrones complejos** que podrían pasar desapercibidos
3. **Generar recomendaciones contextualizadas** para el mercado argentino
4. **Traducir datos numéricos** en estrategias comerciales claras
5. **Considerar factores cualitativos** junto con los cuantitativos """

# Preparación del contexto financiero para análisis con IA
if cotizaciones_actuales and datos_historicos:
    print("Preparando contexto financiero para análisis con Gemini...")

    # Construir un resumen estructurado de la información financiera
    contexto_financiero = """ANÁLISIS DE MERCADO - COMMODITIES AGRÍCOLAS ARGENTINOS

    COTIZACIONES ACTUALES (con variación diaria):
    """

    # Agregar cotizaciones actuales
    for commodity, datos in cotizaciones_actuales.items():
        precio = datos['precio']
        variacion = datos['variacion']
        contexto_financiero += f"""
    - {commodity}: ${precio:.2f} ({variacion:+.2f}% hoy)"""

    # Agregar análisis estadístico si está disponible
    contexto_financiero += "\n\nANÁLISIS ESTADÍSTICO (ÚLTIMOS 6 MESES):"

    if 'resumen_estadistico' in locals():
        for commodity, stats in resumen_estadistico.items():
            contexto_financiero += f"""
    - {commodity}: Actual ${stats['actual']:.2f} | Promedio ${stats['promedio_6m']:.2f} | Percentil {stats['percentil']:.0f}% | Retorno {stats['retorno_total']:+.1f}%"""

    # Agregar información sobre volatilidad
    contexto_financiero += "\n\nNIVELES DE VOLATILIDAD:"
    if 'resumen_estadistico' in locals():
        for commodity, stats in resumen_estadistico.items():
            cv = (stats['volatilidad'] / stats['promedio_6m']) * 100
            contexto_financiero += f"""
    - {commodity}: Coeficiente de Variación {cv:.1f}%"""

    print("Contexto financiero preparado para análisis:")
    print(contexto_financiero[:500] + "..." if len(contexto_financiero) > 500 else contexto_financiero)
    print(f"\nLongitud total del contexto: {len(contexto_financiero)} caracteres")
else:
    print("⚠ Warning: No se puede preparar contexto sin datos de cotizaciones")

""" Resultado """

# ============================================================
# INTERPRETACIÓN DE MÉTRICAS:
# - Percentil 90-100%: Precio cerca de máximos históricos
# - Percentil 0-10%: Precio cerca de mínimos históricos
# - Coeficiente de Variación (CV): Volatilidad relativa al precio promedio
# - Retorno del período: Ganancia/pérdida desde el inicio del análisis
# Preparando contexto financiero para análisis con Gemini...
# Contexto financiero preparado para análisis:
# ANÁLISIS DE MERCADO - COMMODITIES AGRÍCOLAS ARGENTINOS

#     COTIZACIONES ACTUALES (con variación diaria):

#     - Soja: $1046.25 (+0.31% hoy)
#     - Maíz: $430.00 (+0.88% hoy)
#     - Trigo: $523.50 (+0.14% hoy)
#     - Dólar: $1453.00 (+0.00% hoy)

# ANÁLISIS ESTADÍSTICO (ÚLTIMOS 6 MESES):
#     - Soja: Actual $1046.25 | Promedio $1025.97 | Percentil 76% | Retorno +4.7%
#     - Maíz: Actual $430.00 | Promedio $429.12 | Percentil 46% | Retorno -3.5%
#     - Trigo: Actual $523.50 | Promedio $529.69 | Perce...

# Longitud total del contexto: 802 caracteres

""" ### Generación de recomendaciones comerciales con IA

Ahora enviamos todos los datos financieros a Gemini para obtener 
un análisis integral y recomendaciones específicas para el contexto argentino. """

# Generación de análisis comercial integral con Gemini
if 'contexto_financiero' in locals():
    print("Enviando datos a Gemini para análisis comercial...")

    # Construir prompt especializado para análisis comercial agrícola
    prompt_comercializacion = f"""Como especialista en comercialización agrícola argentina con 15 años de experiencia, analiza la siguiente información de mercado y genera un INFORME INTEGRAL DE OPORTUNIDADES COMERCIALES:

{contexto_financiero}

CONTEXTO ESPECÍFICO DEL MERCADO ARGENTINO:
- Estamos en plena campaña agrícola 2024/25
- Los productores argentinos manejan stocks de soja y maíz de la campaña anterior
- El tipo de cambio oficial vs. paralelo ("blue") impacta significativamente en las decisiones de liquidación
- Los costos de producción han aumentado considerablemente debido a la inflación
- Existe incertidumbre política y económica que afecta las decisiones de inversión
- Los productores necesitan equilibrar flujo de caja con maximización de ingresos

GENERA UN ANÁLISIS COMERCIAL ESTRUCTURADO QUE INCLUYA:

1. **DIAGNÓSTICO ACTUAL**: Evaluación general del momento de mercado
2. **OPORTUNIDADES INMEDIATAS**: Qué commodities presentan ventanas de venta favorables HOY
3. **ESTRATEGIA DE RETENCIÓN**: Qué productos conviene mantener en stock esperando mejores precios
4. **ANÁLISIS DE RIESGO**: Factores macro y microeconómicos que podrían afectar los precios próximamente
5. **RECOMENDACIONES POR CULTIVO**: Estrategias específicas y diferenciadas para soja, maíz y trigo
6. **TIMING COMERCIAL**: Identificar ventanas de oportunidad en los próximos 30, 60 y 90 días
7. **GESTIÓN FINANCIERA**: Recomendaciones sobre exposición al dólar y estrategias de cobertura
8. **PLAN DE ACCIÓN**: Pasos concretos que un productor debería tomar esta semana

Enfoque requerido: PRÁCTICO, ACTIONABLE y ESPECÍFICO para productores argentinos que necesitan tomar decisiones comerciales inmediatas. Evita generalidades y enfócate en recomendaciones concretas.
"""

    try:
        print("Procesando análisis con Gemini (esto puede tomar unos segundos)...")
        analisis_comercial = analizar_con_gemini(prompt_comercializacion)

        print("\n" + "=" * 70)
        print("INFORME INTEGRAL DE OPORTUNIDADES COMERCIALES")
        print("Análisis generado por: Gemini AI + Datos Yahoo Finance")
        print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 70)
        console.print(Markdown(analisis_comercial))

    except Exception as e:
        print(f"✗ Error al generar análisis con Gemini: {e}")
        print("Verificar conectividad y configuración de API")
else:
    print("⚠ No se puede generar análisis sin contexto financiero preparado")


"""### Función de cálculo de márgenes

Esta función integra:
1. **Conversión de unidades**: De bushel (mercado internacional) a quintales (unidad argentina)
2. **Cálculo de ingresos**: Precio × Rendimiento
3. **Cálculo de márgenes**: Ingresos - Costos
4. **Conversión a pesos argentinos** usando el tipo de cambio actual"""

# Factores de conversión de bushel a quintal
# Estos factores se basan en el peso estándar de cada commodity
conversion_bu_qq = {
    'Soja': 0.6,      # 1 bushel soja = 27.2 kg ≈ 0.6 quintales
    'Maíz': 0.56,     # 1 bushel maíz = 25.4 kg ≈ 0.56 quintales
    'Trigo': 0.6      # 1 bushel trigo = 27.2 kg ≈ 0.6 quintales
}

costos_produccion = {
    'Soja': {'rendimiento_qq_ha': 30.0, 'costo_total_usd_ha': 520.0},
    'Maíz': {'rendimiento_qq_ha': 85.0, 'costo_total_usd_ha': 980.0},
    'Trigo': {'rendimiento_qq_ha': 35.0, 'costo_total_usd_ha': 620.0},
}

def usd_bu_a_usd_qq(precio_usd_bu: float, cultivo: str, conversion_bu_qq: dict) -> float:
    if cultivo not in conversion_bu_qq:
        raise KeyError(f"No hay factor de conversión para '{cultivo}'")
    qq_por_bu = conversion_bu_qq[cultivo]
    return precio_usd_bu / qq_por_bu

def calcular_margen_bruto(
    cultivo: str,
    precio_internacional_usd_bu: float,
    tipo_cambio_ars_usd: float | None,
    costos_produccion: dict,
    conversion_bu_qq: dict
) -> dict:
    if cultivo not in costos_produccion:
        raise KeyError(f"'{cultivo}' no está definido en costos_produccion")

    precio_usd_qq = usd_bu_a_usd_qq(precio_internacional_usd_bu, cultivo, conversion_bu_qq)
    rendimiento = float(costos_produccion[cultivo]['rendimiento_qq_ha'])
    costo_total_usd = float(costos_produccion[cultivo]['costo_total_usd_ha'])

    ingreso_bruto_usd = rendimiento * precio_usd_qq
    margen_bruto_usd  = ingreso_bruto_usd - costo_total_usd
    margen_pct = (margen_bruto_usd / ingreso_bruto_usd * 100.0) if ingreso_bruto_usd > 0 else 0.0

    ingreso_bruto_ars = costo_total_ars = margen_bruto_ars = None
    if tipo_cambio_ars_usd:
        ingreso_bruto_ars = ingreso_bruto_usd * tipo_cambio_ars_usd
        costo_total_ars   = costo_total_usd   * tipo_cambio_ars_usd
        margen_bruto_ars  = margen_bruto_usd  * tipo_cambio_ars_usd

    return {
        'cultivo': cultivo,
        'precio_usd_qq': precio_usd_qq,
        'rendimiento': rendimiento,
        'ingreso_bruto_usd': ingreso_bruto_usd,
        'ingreso_bruto_ars': ingreso_bruto_ars,
        'costo_total_usd': costo_total_usd,
        'costo_total_ars': costo_total_ars,
        'margen_bruto_usd': margen_bruto_usd,
        'margen_bruto_ars': margen_bruto_ars,
        'margen_porcentaje': margen_pct
    }

def calcular_margen_bruto(cultivo, precio_usd_por_bu, tipo_cambio=None):
    """
    Calcula el margen bruto para un cultivo específico basado en el precio actual.

    Esta función realiza los siguientes cálculos:
    1. Convierte el precio de bushel a quintal
    2. Calcula el ingreso bruto (precio × rendimiento)
    3. Resta los costos de producción
    4. Calcula el margen como porcentaje del ingreso
    5. Opcionalmente convierte a pesos argentinos

    Parámetros:
    cultivo (str): Nombre del cultivo ('Soja', 'Maíz', 'Trigo')
    precio_usd_por_bu (float): Precio en USD por bushel
    tipo_cambio (float, opcional): Tipo de cambio USD/ARS

    Retorna:
    dict: Diccionario con todos los cálculos de rentabilidad
    """

    # Verificar que el cultivo esté en nuestra base de datos
    if cultivo not in costos_produccion:
        print(f"✗ Error: Cultivo '{cultivo}' no encontrado en base de datos")
        return None

    # Obtener datos del cultivo
    datos_cultivo = costos_produccion[cultivo]

    # Convertir precio de bushel a quintal
    factor_conversion = conversion_bu_qq[cultivo]
    precio_usd_qq = precio_usd_por_bu / factor_conversion

    print(f"Análisis de rentabilidad para {cultivo}:")
    print(f"- Precio mercado: ${precio_usd_por_bu:.2f} USD/bu")
    print(f"- Factor conversión: {factor_conversion} qq/bu")
    print(f"- Precio equivalente: ${precio_usd_qq:.2f} USD/qq")

    # Calcular componentes financieros
    rendimiento = datos_cultivo['rendimiento_promedio']
    ingreso_bruto_usd = precio_usd_qq * rendimiento
    costo_total = datos_cultivo['total']
    margen_bruto_usd = ingreso_bruto_usd - costo_total

    # Calcular margen como porcentaje del ingreso
    if ingreso_bruto_usd > 0:
        margen_porcentaje = (margen_bruto_usd / ingreso_bruto_usd) * 100
    else:
        margen_porcentaje = 0
        print("⚠ Warning: Ingreso bruto es cero o negativo")

    # Crear diccionario con resultados
    resultado = {
        'cultivo': cultivo,
        'precio_usd_bu': precio_usd_por_bu,
        'precio_usd_qq': precio_usd_qq,
        'rendimiento': rendimiento,
        'ingreso_bruto_usd': ingreso_bruto_usd,
        'costo_total_usd': costo_total,
        'margen_bruto_usd': margen_bruto_usd,
        'margen_porcentaje': margen_porcentaje
    }

    # Si se proporciona tipo de cambio, agregar conversión a ARS
    if tipo_cambio and tipo_cambio > 0:
        resultado['tipo_cambio'] = tipo_cambio
        resultado['ingreso_bruto_ars'] = ingreso_bruto_usd * tipo_cambio
        resultado['costo_total_ars'] = costo_total * tipo_cambio
        resultado['margen_bruto_ars'] = margen_bruto_usd * tipo_cambio

        print(f"- Conversión a ARS con TC: ${tipo_cambio:.2f}")

    return resultado

print("Función calcular_margen_bruto() configurada correctamente")
print("\nFactores de conversión utilizados:")
print("- Soja: 1 bushel = 0.6 quintales")
print("- Maíz: 1 bushel = 0.56 quintales")
print("- Trigo: 1 bushel = 0.6 quintales")


""" Respuesta """

# Función calcular_margen_bruto() configurada correctamente

# Factores de conversión utilizados:
# - Soja: 1 bushel = 0.6 quintales
# - Maíz: 1 bushel = 0.56 quintales
# - Trigo: 1 bushel = 0.6 quintales


""" Cálculo de márgenes con precio actual """

# Ejecutar análisis de márgenes con precios actuales de mercado
print("=" * 70)
print("ANÁLISIS DE RENTABILIDAD - MÁRGENES BRUTOS CON PRECIOS ACTUALES")
print("=" * 70)

if cotizaciones_actuales:
    # Obtener tipo de cambio actual
    tipo_cambio = cotizaciones_actuales.get('Dólar', {}).get('precio', None)

    if tipo_cambio:
        print(f"Tipo de cambio utilizado: ${tipo_cambio:.2f} ARS/USD")
    else:
        print("⚠ Warning: No se pudo obtener tipo de cambio, análisis solo en USD")

    print(f"Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # Lista para almacenar resultados para análisis posterior
    resultados_margenes = []

    # Analizar cada cultivo
    for cultivo in ['Soja', 'Maíz', 'Trigo']:
        if cultivo in cotizaciones_actuales:
            print(f"\n{cultivo.upper()} - ANÁLISIS DE RENTABILIDAD:")
            print("-" * 45)

            precio_actual = cotizaciones_actuales[cultivo]['precio']
            margen = calcular_margen_bruto(cultivo, precio_actual, tipo_cambio)

            if margen:
                # Almacenar para análisis comparativo posterior
                resultados_margenes.append(margen)

                # Mostrar resultados detallados
                print(f"  Precio internacional: ${precio_actual:.2f} USD/bu")
                print(f"  Precio local equivalente: ${margen['precio_usd_qq']:.2f} USD/qq")
                print(f"  Rendimiento esperado: {margen['rendimiento']} qq/ha")
                print()
                print(f"  ANÁLISIS FINANCIERO (por hectárea):")
                print(f"  Ingreso bruto: ${margen['ingreso_bruto_usd']:.0f} USD")
                if tipo_cambio:
                    print(f"                 ${margen['ingreso_bruto_ars']:,.0f} ARS")

                print(f"  Costo total:   ${margen['costo_total_usd']:.0f} USD")
                if tipo_cambio:
                    print(f"                 ${margen['costo_total_ars']:,.0f} ARS")

                print(f"  Margen bruto:  ${margen['margen_bruto_usd']:.0f} USD")
                if tipo_cambio:
                    print(f"                 ${margen['margen_bruto_ars']:,.0f} ARS")

                print(f"  Margen %:      {margen['margen_porcentaje']:.1f}%")

                # Evaluación qualitativa del margen
                margen_pct = margen['margen_porcentaje']
                if margen_pct > 25:
                    evaluacion = "EXCELENTE - Muy alta rentabilidad"
                    semaforo = "Verde"
                elif margen_pct > 15:
                    evaluacion = "BUENA - Rentabilidad satisfactoria"
                    semaforo = "Verde claro"
                elif margen_pct > 5:
                    evaluacion = "MARGINAL - Evaluar riesgos cuidadosamente"
                    semaforo = "Amarillo"
                elif margen_pct > 0:
                    evaluacion = "BAJA - Rentabilidad mínima"
                    semaforo = "Naranja"
                else:
                    evaluacion = "NEGATIVA - Pérdida económica"
                    semaforo = "Rojo"

                print(f"  Evaluación:    [{semaforo}] {evaluacion}")

                # Análisis de punto de equilibrio
                precio_equilibrio = margen['costo_total_usd'] / margen['rendimiento']
                print(f"  Punto equilibrio: ${precio_equilibrio:.2f} USD/qq")
                print(f"                   (${precio_equilibrio / conversion_bu_qq[cultivo]:.2f} USD/bu)")

            else:
                print(f"  ✗ Error calculando margen para {cultivo}")
        else:
            print(f"\n{cultivo}: No se pudieron obtener cotizaciones")

    if not resultados_margenes:
        print("\n⚠ No se pudieron calcular márgenes - verificar datos de cotizaciones")
    else:
        print(f"\n\nRESUMEN: Se calcularon márgenes para {len(resultados_margenes)} cultivos")

        # Ranking de rentabilidad
        resultados_ordenados = sorted(resultados_margenes,
                                    key=lambda x: x['margen_porcentaje'],
                                    reverse=True)

        print("\nRANKING DE RENTABILIDAD:")
        for i, resultado in enumerate(resultados_ordenados, 1):
            print(f"{i}. {resultado['cultivo']}: {resultado['margen_porcentaje']:.1f}% de margen")

else:
    print("⚠ No se pueden calcular márgenes sin datos de cotizaciones actuales")
    print("Ejecutar primero la celda de obtención de cotizaciones")

"""### Ejercicios prácticos para consolidar aprendizaje

Estos ejercicios están diseñados para aplicar los conceptos aprendidos y profundizar la comprensión de los datos financieros agrícolas."""

# Ejercicios prácticos para aplicar los conceptos aprendidos
print("=" * 70)
print("EJERCICIOS PRÁCTICOS - APLICACIÓN DE CONCEPTOS")
print("=" * 70)

print("\n💡 EJERCICIO 1: Análisis de Punto de Equilibrio")
print("-" * 50)
print("Con base en los resultados de la simulación:")
print()
if 'todas_simulaciones' in locals():
    for cultivo, simulacion in todas_simulaciones.items():
        # Encontrar el escenario más cercano al punto de equilibrio
        escenario_equilibrio = min(simulacion, key=lambda x: abs(x['margen_porcentaje']))
        precio_equilibrio = escenario_equilibrio['precio_simulado']

        print(f"a) {cultivo}: ¿Cuál sería el precio de equilibrio aproximado?")
        print(f"   Respuesta: ~${precio_equilibrio:.2f} USD/bu ({escenario_equilibrio['escenario_pct']:+}% del actual)")
        print()
else:
    print("Ejecutar primero la simulación de escenarios")

print("\n💡 EJERCICIO 2: Estrategia de Riesgo")
print("-" * 50)
print("Pregunta: Si esperaras que los precios podrían caer 15%, ¿qué estrategia usarías?")
print()
print("Consideraciones a evaluar:")
print("• ¿Qué cultivos mantienen rentabilidad con -15% de precio?")
print("• ¿Cuál sería el impacto económico en USD/ha?")
print("• ¿Qué porcentaje del portafolio vendería inmediatamente?")
print("• ¿Implementarías alguna estrategia de cobertura?")

print("\n💡 EJERCICIO 3: Análisis de Oportunidades")
print("-" * 50)
print("Pregunta: Si los precios subieran 20% mañana, ¿cómo cambiaría tu plan?")
print()
print("Tareas a realizar:")
print("1. Calcular el nuevo margen para cada cultivo")
print("2. Identificar qué cultivo tendría el mayor beneficio absoluto (USD/ha)")
print("3. Evaluar si sería momento de vender todo el stock")
print("4. Considerar el impacto en las decisiones de siembra de la próxima campaña")

print("\n💡 EJERCICIO 4: Comparación de Volatilidad")
print("-" * 50)
if 'todas_simulaciones' in locals():
    print("Con base en la simulación ejecutada:")
    print()
    for cultivo, simulacion in todas_simulaciones.items():
        margenes = [r['margen_porcentaje'] for r in simulacion]
        volatilidad = max(margenes) - min(margenes)
        print(f"• {cultivo}: Volatilidad de {volatilidad:.1f} puntos porcentuales")

    print("\nPreguntas para analizar:")
    print("a) ¿Cuál cultivo es menos riesgoso (menor volatilidad)?")
    print("b) ¿Cuál ofrece mayor upside potencial?")
    print("c) ¿Cómo balancearías riesgo vs. retorno en tu portafolio?")
else:
    print("Ejecutar simulación para completar este ejercicio")

print("\n💡 EJERCICIO 5: Simulación Personalizada")
print("-" * 50)
print("Desafío avanzado:")
print("1. Modifica los costos de producción con tus datos locales")
print("2. Ejecuta una nueva simulación con escenarios específicos")
print("3. Genera un reporte personalizado con recomendaciones")
print("4. Compara los resultados con el análisis estándar")

print("\n" + "=" * 70)
print("📚 RECURSOS ADICIONALES PARA PROFUNDIZAR:")
print("=" * 70)
print("• Yahoo Finance API Documentation")
print("• Google Gemini AI Studio")
print("• Mercado de Chicago (CBOT) - Especificaciones de contratos")
print("• Análisis técnico de commodities")
print("• Gestión de riesgo en mercados agrícolas")

print("\n🎯 PRÓXIMOS PASOS SUGERIDOS:")
print("1. Ejecutar este análisis semanalmente")
print("2. Crear alertas personalizadas según tu estrategia")
print("3. Integrar con datos locales de tu región")
print("4. Desarrollar modelos predictivos más avanzados")
print("5. Automatizar reportes para toma de decisiones")
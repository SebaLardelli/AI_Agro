# Arquitectura del Sistema Agrícola Modularizado

## Diagrama de Flujo Principal

```mermaid
graph TD
    A[Usuario envía imagen por Telegram] --> B[n8n recibe imagen]
    B --> C[HTTP Request a Flask App]
    C --> D[app_flask.py]
    D --> E[AnalizadorAgricola.analizar_imagen()]
    
    E --> F[Procesar imagen PIL]
    F --> G[GeminiDetector.detectar_con_gemini()]
    G --> H[Gemini Vision API]
    H --> I[Detectar objetos individuales]
    
    I --> J[Filtrar por confianza + validar labels]
    J --> K[Second Pass: buscar plagas en zonas con moho]
    K --> L[Fusionar granos contiguos]
    L --> M[Generar imagen debug con bounding boxes]
    
    M --> N[Calcular métricas cuantitativas]
    N --> O[Generar diagnóstico técnico]
    O --> P[Generar diagnóstico agronómico global]
    P --> Q[Crear data_momento para agente]
    
    Q --> R[Devolver JSON completo]
    R --> S[n8n procesa respuesta]
    S --> T[Enviar resultado a Telegram]
```

## Arquitectura Modular

```mermaid
graph LR
    subgraph "Aplicación Principal"
        A[analizador_agricola_modular.py]
        B[app_flask.py]
    end
    
    subgraph "Módulos"
        C[modules/detection/gemini_detector.py]
        D[modules/analysis/metrics_calculator.py]
        E[modules/utils/validation.py]
        F[modules/utils/geometry.py]
        G[modules/utils/image_utils.py]
    end
    
    subgraph "Servicios Externos"
        H[Google Gemini Vision API]
        I[Supabase Database - Opcional]
    end
    
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    
    C --> H
    B --> A
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
    style H fill:#ffebee
    style I fill:#f1f8e9
```

## Flujo de Detección de Objetos

```mermaid
flowchart TD
    A[Imagen PIL] --> B[GeminiDetector.detectar_con_gemini()]
    B --> C[Prompt especializado para agricultura]
    C --> D[Gemini Vision API]
    D --> E[Array JSON con objetos detectados]
    
    E --> F[Filtrar por confianza score >= 0.6]
    F --> G[Validar labels con firewall]
    G --> H[Clasificar: categoria, especie, estado]
    
    H --> I[Second Pass: zonas sospechosas]
    I --> J[Detectar plagas en áreas con moho]
    J --> K[Fusionar granos contiguos]
    K --> L[Non-Max Suppression por label]
    
    L --> M[Lista final de objetos detectados]
    
    style A fill:#e3f2fd
    style D fill:#ffebee
    style M fill:#e8f5e8
```

## Tipos de Objetos Detectados

```mermaid
mindmap
  root((Objetos Agrícolas))
    Granos
      Maíz
        Sano
        Roto
        Con moho
      Soja
        Sano
        Roto
        Con moho
      Trigo
        Sano
        Roto
        Con moho
    Plagas
      Gusano
      Larva
      Gorgojo
      Insecto
      Polilla
    Fauna Riesgo
      Rata
      Ratón
      Paloma
      Ave
    Hongos
      Moho en grano
      Pudrición fúngica
      Hongo superficial
    Maleza
      Material vegetal extraño
```

## Métricas y Diagnósticos

```mermaid
graph TD
    A[Objetos Detectados] --> B[calcular_metricas()]
    
    B --> C[Contar por categoría]
    B --> D[Contar por especie]
    B --> E[Calcular % grano con moho]
    B --> F[Evaluar riesgos]
    
    C --> G[Métricas Cuantitativas]
    D --> G
    E --> G
    F --> G
    
    G --> H[armar_diagnostico()]
    G --> I[armar_data_momento()]
    
    H --> J[Diagnóstico Técnico]
    I --> K[Data para Agente RAG]
    
    J --> L[Recomendaciones de Acción]
    K --> M[Hallazgos Clave]
    
    style G fill:#e8f5e8
    style J fill:#fff3e0
    style K fill:#e1f5fe
```

## Respuesta JSON Completa

```mermaid
graph LR
    A[analizar_imagen()] --> B[JSON Response]
    
    B --> C[timestamp]
    B --> D[tipo_imagen]
    B --> E[objetos_detectados]
    B --> F[metricas]
    B --> G[diagnostico_texto]
    B --> H[diagnostico_global]
    B --> I[data_momento]
    B --> J[imagen_bbox_path]
    
    E --> K[Lista de objetos con bbox]
    F --> L[Conteos y porcentajes]
    G --> M[Riesgo sanitario/comercial]
    H --> N[Explicación agronómica]
    I --> O[Estructura para RAG]
    J --> P[Ruta imagen debug]
    
    style B fill:#e8f5e8
    style K fill:#fff3e0
    style L fill:#fff3e0
    style M fill:#ffebee
    style N fill:#e1f5fe
    style O fill:#f3e5f5
    style P fill:#e8f5e8
```

## Modo Fallback

```mermaid
graph TD
    A[Módulos Disponibles?] --> B{Sí}
    A --> C{No}
    
    B --> D[Usar módulos completos]
    C --> E[Modo Fallback]
    
    D --> F[GeminiDetector]
    D --> G[MetricsCalculator]
    D --> H[ImageUtils]
    
    E --> I[Métodos fallback básicos]
    E --> J[Análisis simplificado]
    E --> K[Imagen debug básica]
    
    F --> L[Análisis Completo]
    G --> L
    H --> L
    
    I --> M[Análisis Básico]
    J --> M
    K --> M
    
    style D fill:#e8f5e8
    style E fill:#fff3e0
    style L fill:#e1f5fe
    style M fill:#ffebee
```

## Docker y Despliegue

```mermaid
graph TD
    A[Dockerfile] --> B[Python 3.11-slim]
    B --> C[Instalar dependencias]
    C --> D[Copiar código modularizado]
    
    D --> E[analizador_agricola_modular.py]
    D --> F[app_flask.py]
    D --> G[modules/]
    
    G --> H[detection/]
    G --> I[analysis/]
    G --> J[utils/]
    
    E --> K[Contenedor Docker]
    F --> K
    H --> K
    I --> K
    J --> K
    
    K --> L[Puerto 5000]
    L --> M[n8n HTTP Request]
    
    style K fill:#e8f5e8
    style M fill:#e1f5fe
```

## Ventajas de la Modularización

```mermaid
mindmap
  root((Beneficios))
    Mantenibilidad
      Código organizado
      Responsabilidades claras
      Fácil debugging
    Reutilización
      Módulos independientes
      Funciones específicas
      Componentes reutilizables
    Testabilidad
      Tests por módulo
      Validación individual
      Cobertura específica
    Escalabilidad
      Nuevos detectores
      Más APIs
      Funcionalidades adicionales
    Compatibilidad
      Interfaz idéntica
      Modo fallback
      Sin breaking changes
```

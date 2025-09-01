# utn-agro-ai
Repositorio de contenido de modulos en el programa "Desarrollo Avanzado de Soluciones de IA"

## Github Cuenta

[GitHub](https://github.com/) es la plataforma de desarrollo colaborativo más popular del mundo, basada en Git. Permite a los desarrolladores:

- **Control de versiones distribuido**: Rastrea cambios en el código fuente durante el desarrollo de software
- **Colaboración en equipo**: Múltiples desarrolladores pueden trabajar en el mismo proyecto simultáneamente
- **Repositorios públicos y privados**: Almacena y organiza proyectos de código
- **Issues y Pull Requests**: Sistema de seguimiento de errores y revisión de código
- **GitHub Actions**: Automatización de flujos de trabajo CI/CD
- **GitHub Pages**: Hosting gratuito para sitios web estáticos

**Características principales:**
- Interfaz web intuitiva para gestión de repositorios
- Integración con herramientas de desarrollo
- Comunidad activa de desarrolladores
- Documentación y wikis integradas

## Instalacion de Git

Control de Versiones [Git](https://git-scm.com/)

## Instalacion de Python

Lenguaje de programacion [Python](https://www.python.org/)

Entorno Virtual de [Python Virtualvenv](https://realpython.com/python-virtual-environments-a-primer/)

## Extensiones VSCode

Lista de extensiones para el [VSCode](https://code.visualstudio.com/)

### Python

- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) - Depurador oficial de Python que permite establecer puntos de interrupciรณn, inspeccionar variables y ejecutar cรณdigo paso a paso.
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - Extensiรณn principal de Python que proporciona soporte completo para el lenguaje, incluyendo IntelliSense, linting, formateo y ejecuciรณn de cรณdigo.
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) - Servidor de lenguaje Python de alto rendimiento que ofrece autocompletado inteligente, verificaciรณn de tipos y anรกlisis de cรณdigo avanzado.
- [Python Environments](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs) - Herramienta para gestionar y cambiar fรกcilmente entre diferentes entornos virtuales de Python (venv, conda, etc.).
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort) - Formateador automรกtico que organiza y ordena las importaciones de Python segรบn las mejores prรกcticas.

### Jupyter

- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) - Soporte completo para notebooks de Jupyter, permitiendo crear, editar y ejecutar celdas de cรณdigo interactivo directamente en VSCode.

### Cline

- [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) - Asistente de IA avanzado para VSCode que permite la automatización de tareas de desarrollo mediante inteligencia artificial.

[Cline](https://cline.bot/) es una extensión de VSCode que integra modelos de lenguaje grandes (LLMs) directamente en tu entorno de desarrollo, permitiendo automatizar tareas complejas de programación y desarrollo.

**Características principales:**
- **Automatización de código**: Genera, modifica y refactoriza código automáticamente
- **Ejecución de comandos**: Puede ejecutar comandos de terminal y scripts
- **Navegación de archivos**: Lee, crea y modifica archivos en tu proyecto
- **Integración con navegador**: Puede interactuar con páginas web para testing
- **Soporte multi-modelo**: Compatible con Claude, GPT-4, modelos locales (Ollama, LM Studio)
- **Modo Plan y Acción**: Planifica tareas complejas antes de ejecutarlas
- **Control granular**: Aprobación manual de acciones críticas

**Modelos soportados:**
- **Claude 3.5 Sonnet**: Modelo recomendado para tareas de desarrollo
- **GPT-4**: Soporte completo para modelos de OpenAI
- **Modelos locales**: Integración con Ollama y LM Studio
- **Otros proveedores**: Anthropic, OpenAI, Google, AWS Bedrock

**Casos de uso:**
- Desarrollo completo de aplicaciones web
- Refactorización y optimización de código existente
- Debugging y resolución de errores
- Creación de documentación automática
- Testing y validación de funcionalidades
- Migración entre tecnologías

**Configuración básica:**
1. Instalar la extensión desde el marketplace de VSCode
2. Configurar tu API key del modelo preferido
3. Ajustar permisos y configuraciones de seguridad
4. Comenzar a interactuar mediante el panel de chat

**Comandos útiles:**
- `Ctrl+Shift+P` → "Cline: Open" para abrir el panel
- Usar `/` para comandos especiales en el chat
- Modo "Auto-approve" para tareas repetitivas
- Checkpoints para guardar estados del proyecto

**Ventajas:**
- **Productividad**: Acelera significativamente el desarrollo
- **Aprendizaje**: Explica el código y las decisiones tomadas
- **Consistencia**: Mantiene estándares de código uniformes
- **Versatilidad**: Maneja múltiples lenguajes y frameworks
- **Seguridad**: Control total sobre las acciones ejecutadas

## Ollama

[Ollama](https://ollama.com/) es una herramienta que permite ejecutar modelos de lenguaje grandes (LLMs) localmente en tu computadora de manera sencilla y eficiente.

**Características principales:**
- **Ejecución local**: Ejecuta modelos de IA sin necesidad de conexión a internet
- **Privacidad**: Tus datos permanecen en tu dispositivo
- **Múltiples modelos**: Soporte para Llama 2, Llama 3, Gemma, Mistral, Code Llama y más
- **API REST**: Interfaz programática para integrar con aplicaciones
- **Optimización automática**: Gestión eficiente de memoria y recursos del sistema

**Instalación:**
```bash
# Windows (PowerShell como administrador)
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

**Comandos básicos:**
```bash
# Descargar y ejecutar un modelo
ollama run llama3

# Listar modelos instalados
ollama list

# Eliminar un modelo
ollama rm modelo_name

# Mostrar información del modelo
ollama show modelo_name
```

**Modelos populares:**
- `llama3`: Modelo general de Meta AI
- `gemma`: Modelo de Google DeepMind
- `mistral`: Modelo eficiente de Mistral AI
- `codellama`: Especializado en programación
- `phi3`: Modelo compacto de Microsoft

## LM Studio

[LM Studio](https://lmstudio.ai/) es una aplicación de escritorio que permite descargar, instalar y ejecutar modelos de lenguaje grandes (LLMs) localmente con una interfaz gráfica intuitiva.

**Características principales:**
- **Interfaz gráfica amigable**: No requiere conocimientos técnicos avanzados
- **Amplio catálogo de modelos**: Acceso a miles de modelos desde Hugging Face
- **Chat interactivo**: Interfaz de chat similar a ChatGPT pero completamente local
- **Servidor local**: Puede funcionar como servidor API compatible con OpenAI
- **Optimización automática**: Detecta automáticamente la configuración óptima para tu hardware
- **Soporte multiplataforma**: Disponible para Windows, macOS y Linux

**Ventajas:**
- **Privacidad total**: Todos los datos permanecen en tu dispositivo
- **Sin límites de uso**: No hay restricciones de tokens o consultas
- **Personalización**: Ajusta parámetros como temperatura, top-p, y más
- **Importación de modelos**: Soporte para formatos GGUF, GGML y otros
- **Historial de conversaciones**: Guarda y organiza tus chats

**Casos de uso:**
- Desarrollo de aplicaciones de IA
- Investigación y experimentación con LLMs
- Asistente personal de programación
- Análisis de texto y generación de contenido
- Prototipado de chatbots y asistentes virtuales

**Requisitos del sistema:**
- **RAM**: Mínimo 8GB (recomendado 16GB+)
- **Almacenamiento**: 10GB+ de espacio libre
- **GPU**: Opcional pero recomendada (NVIDIA, AMD, o Apple Silicon)

# Backend - Prompt API

## Descripción del Proyecto

Este backend expone una API para procesar prompts de usuario, cachear resultados de IA (BitoService), enviar emails y registrar métricas de visitas. Utiliza MongoDB para cache y métricas, y está preparado para despliegue en Docker.

## Tecnologías principales
- Python 3.10+
- Flask
- MongoDB (vía Docker)
- PyMongo
- Jinja2 (templates)
- user-agents (detección de navegador/SO)
- Docker/Docker Compose

## Instalación y uso

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd backend_web
```

### 2. Variables de entorno
Crea un archivo `.env` con las siguientes variables si usas email:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_usuario@gmail.com
SMTP_PASSWORD=tu_password
MONGO_URI=mongodb+srv://usuario:contraseña@cluster0.xxxxx.mongodb.net/prompt_db?retryWrites=true&w=majority
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Levantar con Docker Compose
```bash
docker-compose up --build
```
Esto levanta el backend y (opcionalmente) MongoDB en la red interna `backendnet`.

### 5. Uso de la API
Puedes usar la colección de Postman incluida (`postman_collection.json`) para probar todos los endpoints.

## Endpoints principales

### POST `/prompt`
- Procesa un prompt, cachea la respuesta de BitoService (IA). Las noticias e imagen se obtienen directamente desde la IA.
- **Body:**
```json
{
  "prompt": "Energía solar",
  "lang": "es"
}
```
- **Respuesta:** JSON con datos de IA, noticias e imagen.

### POST `/test_prompt`
- Igual que `/prompt` pero usa un ejemplo de respuesta de BitoService (no consulta la IA real).

### GET `/prompt-history`
- Devuelve el historial de prompts cacheados (prompt normalizado, idioma, fecha, topic).

### GET `/metrics`
- Devuelve las últimas 100 visitas registradas (IP, user agent, SO, navegador, idioma, referrer, ruta, móvil/bot, timestamp).

### POST `/send-email`
- Envía un email usando los parámetros dados.
- **Body:**
```json
{
  "to": "destinatario@correo.com",
  "subject": "Asunto de prueba",
  "message": "Este es un mensaje de prueba."
}
```

## Estructura de carpetas
- `services/` - Lógica de negocio, cache, métricas, plantillas.
- `routes/` - Rutas de la API organizadas por funcionalidad.
- `postman_collection.json` - Colección de pruebas para Postman.
- `Dockerfile`, `docker-compose.yaml` - Contenedores y orquestación.

## Notas
- El prompt enviado se normaliza (NLP) para evitar duplicados y mejorar el cache.
- Las noticias e imagen se obtienen directamente desde la IA (BitoService), no por scraping.
- Las métricas de visitas se almacenan en MongoDB para análisis posterior.

---

¿Dudas? Contacta al equipo de desarrollo. 
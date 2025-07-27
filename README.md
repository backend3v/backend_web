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

## 🐳 Configuración de Docker

### Configuración Rápida
```bash
# Desarrollo con MongoDB
docker-compose -f docker-compose.dev.yaml up --build

# Solo Backend
docker-compose up --build

# Con nombres personalizados
docker-compose -p mi-proyecto up --build
```

### Personalización de Servicios
- **Cambiar nombres**: Modifica `container_name` y nombres de servicios
- **Redes independientes**: Configura redes separadas por entorno
- **Variables de entorno**: Usa archivos `.env` para configuraciones

Ver documentación completa en [`DOCKER_CONFIGURATION.md`](./DOCKER_CONFIGURATION.md)

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
# Desarrollo completo (Backend + MongoDB)
docker-compose -f docker-compose.dev.yaml up --build

# Solo Backend
docker-compose up --build

# Con nombres personalizados
docker-compose -p mi-proyecto up --build
```

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
- `DOCKER_CONFIGURATION.md` - Documentación completa de Docker.

## 🔧 Configuración Avanzada

### Servicios Independientes
El backend está diseñado para funcionar con servicios independientes:

```yaml
# Ejemplo de configuración personalizada
services:
  mi-backend-api:
    build: .
    container_name: mi-backend-container
    ports:
      - "8080:8080"
    networks:
      - mi-red-backend

  mi-base-datos:
    image: mongo:6.0
    container_name: mi-mongo-container
    networks:
      - mi-red-backend
```

### Redes Independientes
```yaml
networks:
  mi-red-backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Variables de Entorno por Entorno
```bash
# Desarrollo
docker-compose -f docker-compose.dev.yaml --env-file .env.development up

# Producción
docker-compose -f docker-compose.prod.yaml --env-file .env.production up
```

## 📊 Monitoreo y Logs

### Ver logs en tiempo real
```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f backend

# Con nombres personalizados
docker-compose -p mi-proyecto logs -f
```

### Gestión de recursos
```bash
# Ver uso de recursos
docker stats

# Limpiar recursos no utilizados
docker system prune -f

# Parar y limpiar todo
docker-compose down -v --remove-orphans
```

## 🚀 Despliegue

### Desarrollo
```bash
docker-compose -f docker-compose.dev.yaml up --build
```

### Producción
```bash
docker-compose -f docker-compose.prod.yaml up --build -d
```

### Múltiples entornos
```bash
# Desarrollo
docker-compose -f docker-compose.dev.yaml -p dev up --build

# Staging
docker-compose -f docker-compose.staging.yaml -p staging up --build

# Producción
docker-compose -f docker-compose.prod.yaml -p prod up --build
```

## Notas
- El prompt enviado se normaliza (NLP) para evitar duplicados y mejorar el cache.
- Las noticias e imagen se obtienen directamente desde la IA (BitoService), no por scraping.
- Las métricas de visitas se almacenan en MongoDB para análisis posterior.
- Los servicios pueden ser completamente independientes y personalizables.
- Ver [`DOCKER_CONFIGURATION.md`](./DOCKER_CONFIGURATION.md) para configuración avanzada.

---

¿Dudas? Contacta al equipo de desarrollo. 
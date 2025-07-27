# Configuración de Docker y Servicios Independientes

## 🐳 Configuración de Docker

### Estructura de Servicios

El backend está diseñado para funcionar con servicios independientes y configurables. Puedes personalizar nombres, redes y configuraciones según tus necesidades.

## 📁 Archivos de Configuración Docker

### 1. `docker-compose.yaml` - Configuración Básica
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    networks:
      - backendnet
networks:
  backendnet:
    driver: bridge
```

### 2. `docker-compose.dev.yaml` - Configuración de Desarrollo
```yaml
version: '3.8'
services:
  mongo:
    image: mongo:6.0
    container_name: mongo-dev
    ports:
      - "27017:27017"
    volumes:
      - mongo_data_dev:/data/db
    networks:
      - devnet

  backend:
    build: .
    container_name: backend-dev
    env_file:
      - .env.development
    ports:
      - "8080:8080"
    depends_on:
      - mongo
    networks:
      - devnet
    volumes:
      - .:/app

volumes:
  mongo_data_dev:

networks:
  devnet:
    driver: bridge
```

## 🔧 Personalización de Servicios

### Cambiar Nombres de Servicios

#### 1. Servicios Básicos
```yaml
# docker-compose.yaml
version: '3.8'
services:
  mi-backend-api:  # Cambiar nombre del servicio
    build: .
    container_name: mi-backend-container  # Cambiar nombre del contenedor
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    networks:
      - mi-red-backend  # Cambiar nombre de la red
networks:
  mi-red-backend:  # Cambiar nombre de la red
    driver: bridge
```

#### 2. Servicios de Desarrollo
```yaml
# docker-compose.dev.yaml
version: '3.8'
services:
  mi-base-datos:  # Cambiar nombre del servicio MongoDB
    image: mongo:6.0
    container_name: mi-mongo-container  # Cambiar nombre del contenedor
    ports:
      - "27017:27017"
    volumes:
      - mi_datos_mongo:/data/db  # Cambiar nombre del volumen
    networks:
      - mi-red-desarrollo  # Cambiar nombre de la red

  mi-backend-api:  # Cambiar nombre del servicio backend
    build: .
    container_name: mi-backend-dev-container  # Cambiar nombre del contenedor
    env_file:
      - .env.development
    ports:
      - "8080:8080"
    depends_on:
      - mi-base-datos  # Referenciar el nuevo nombre
    networks:
      - mi-red-desarrollo  # Cambiar nombre de la red
    volumes:
      - .:/app

volumes:
  mi_datos_mongo:  # Cambiar nombre del volumen

networks:
  mi-red-desarrollo:  # Cambiar nombre de la red
    driver: bridge
```

### Configuración de Redes Independientes

#### 1. Redes Separadas por Entorno
```yaml
# docker-compose.prod.yaml
version: '3.8'
services:
  backend-prod:
    build: .
    container_name: backend-produccion
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - NODE_ENV=production
    networks:
      - red-produccion

  mongo-prod:
    image: mongo:6.0
    container_name: mongo-produccion
    ports:
      - "27017:27017"
    volumes:
      - mongo_prod_data:/data/db
    networks:
      - red-produccion

volumes:
  mongo_prod_data:

networks:
  red-produccion:
    driver: bridge
```

#### 2. Redes con Configuración Avanzada
```yaml
# docker-compose.advanced.yaml
version: '3.8'
services:
  backend-api:
    build: .
    container_name: api-backend
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - MONGO_URI=mongodb://mongo-db:27017/prompt_db
    depends_on:
      - mongo-db
    networks:
      - red-api
      - red-interna

  mongo-db:
    image: mongo:6.0
    container_name: mongo-database
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    networks:
      - red-interna

  redis-cache:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    networks:
      - red-interna

volumes:
  mongo_data:

networks:
  red-api:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  red-interna:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.21.0.0/16
```

## 🚀 Configuraciones por Entorno

### Desarrollo Local
```bash
# Usar configuración de desarrollo
docker-compose -f docker-compose.dev.yaml up --build

# Con nombres personalizados
docker-compose -f docker-compose.dev.yaml -p mi-proyecto up --build
```

### Producción
```bash
# Usar configuración de producción
docker-compose -f docker-compose.prod.yaml up --build

# Con nombres personalizados
docker-compose -f docker-compose.prod.yaml -p mi-proyecto-prod up --build
```

### Múltiples Entornos
```bash
# Desarrollo
docker-compose -f docker-compose.dev.yaml -p dev up --build

# Staging
docker-compose -f docker-compose.staging.yaml -p staging up --build

# Producción
docker-compose -f docker-compose.prod.yaml -p prod up --build
```

## 🔒 Configuración de Seguridad

### Variables de Entorno
```yaml
# .env.production
MONGO_URI=mongodb://mongo-db:27017/prompt_db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_usuario@gmail.com
SMTP_PASSWORD=tu_password
NODE_ENV=production
```

### Configuración con Secrets
```yaml
# docker-compose.secure.yaml
version: '3.8'
services:
  backend-secure:
    build: .
    container_name: backend-seguro
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    env_file:
      - .env.production
    secrets:
      - db_password
      - api_key
    networks:
      - red-segura

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt

networks:
  red-segura:
    driver: bridge
```

## 📊 Monitoreo y Logs

### Configuración con Logs
```yaml
# docker-compose.monitoring.yaml
version: '3.8'
services:
  backend-monitored:
    build: .
    container_name: backend-monitoreado
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - red-monitoreo

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - red-monitoreo

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    networks:
      - red-monitoreo

networks:
  red-monitoreo:
    driver: bridge
```

## 🛠️ Comandos Útiles

### Gestión de Servicios
```bash
# Levantar servicios
docker-compose up -d

# Levantar con nombres personalizados
docker-compose -p mi-proyecto up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Reconstruir servicios
docker-compose up --build

# Limpiar recursos
docker-compose down -v --remove-orphans
```

### Gestión de Redes
```bash
# Listar redes
docker network ls

# Inspeccionar red
docker network inspect mi-red-backend

# Crear red personalizada
docker network create mi-red-personalizada

# Conectar contenedor a red
docker network connect mi-red-personalizada mi-contenedor
```

### Gestión de Volúmenes
```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect mi_datos_mongo

# Crear volumen personalizado
docker volume create mi-volumen-personalizado
```

## 🔧 Scripts de Automatización

### Script de Despliegue
```bash
#!/bin/bash
# deploy.sh

ENVIRONMENT=$1
PROJECT_NAME=$2

if [ "$ENVIRONMENT" = "dev" ]; then
    docker-compose -f docker-compose.dev.yaml -p $PROJECT_NAME up --build -d
elif [ "$ENVIRONMENT" = "prod" ]; then
    docker-compose -f docker-compose.prod.yaml -p $PROJECT_NAME up --build -d
else
    echo "Uso: ./deploy.sh [dev|prod] [nombre-proyecto]"
    exit 1
fi
```

### Script de Limpieza
```bash
#!/bin/bash
# cleanup.sh

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Uso: ./cleanup.sh [nombre-proyecto]"
    exit 1
fi

docker-compose -p $PROJECT_NAME down -v --remove-orphans
docker system prune -f
```

## 📋 Checklist de Configuración

### ✅ Configuración Básica
- [ ] Crear archivo `docker-compose.yaml` personalizado
- [ ] Cambiar nombres de servicios
- [ ] Configurar redes personalizadas
- [ ] Definir variables de entorno

### ✅ Configuración Avanzada
- [ ] Configurar múltiples entornos
- [ ] Implementar seguridad con secrets
- [ ] Configurar monitoreo y logs
- [ ] Crear scripts de automatización

### ✅ Verificación
- [ ] Probar conexión entre servicios
- [ ] Verificar logs y monitoreo
- [ ] Probar despliegue en diferentes entornos
- [ ] Validar configuración de seguridad

## 🚨 Notas Importantes

1. **Nombres de Servicios**: Deben ser únicos dentro del mismo proyecto
2. **Redes**: Los servicios en la misma red pueden comunicarse por nombre
3. **Volúmenes**: Los datos persisten entre reinicios
4. **Variables de Entorno**: Usar archivos `.env` para configuraciones sensibles
5. **Logs**: Configurar rotación de logs para evitar llenar el disco

## 📞 Soporte

Para problemas con la configuración de Docker:
1. Verificar que Docker y Docker Compose estén instalados
2. Revisar los logs con `docker-compose logs`
3. Verificar la conectividad de red con `docker network inspect`
4. Consultar la documentación oficial de Docker Compose 
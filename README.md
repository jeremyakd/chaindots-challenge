# Social API

Este es el repositorio del proyecto Social API.

## Clonar el repositorio

Para probar el proyecto, clona el repositorio usando el siguiente comando:

```bash
git clone https://github.com/tu_usuario/social_api.git
```

## Configuración del entorno virtual

1. **Instalar virtualenv si aún no está instalado:**

    ```bash
    pip install virtualenv
    ```

2. **Crear y activar el entorno virtual:**

    ```bash
    virtualenv venv 
    source venv/bin/activate 
    ```

3. **Instalar las dependencias del proyecto:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Aplicar las migraciones de la base de datos:**

    ```bash
    python manage.py migrate
    ```

5. **Crear un superusuario (opcional):**

    ```bash
    python manage.py createsuperuser
    ```

6. **Ejecutar el servidor:**

    ```bash
    python manage.py runserver
    ```

## Ejecutar la aplicación con Docker 

1. **Levantar el entorno con docker-compose:**

    ```bash
    docker-compose up --build
    ```

2. **Aplicar migraciones y crear un superusuario:**

    ```bash
    docker exec -it social_api-web-1 python manage.py migrate
    docker exec -it social_api-web-1 python manage.py createsuperuser
    ```


## Ejecutar las pruebas

Para ejecutar las pruebas del proyecto con `pytest`, sigue los pasos correspondientes según tu entorno:

### En el entorno virtual

1. **Configurar el entorno de test (opcional):**

    ```bash
    export DJANGO_SETTINGS_MODULE=config.settings.tests
    ```

2. **Ejecutar pytest:**

    ```bash
    pytest
    ```

### Con Docker

1. **Ejecutar pytest en el contenedor:**

    ```bash
    docker exec -it social_api-web-1 pytest
    ```


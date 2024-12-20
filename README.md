# Social API

Este es el repositorio del proyecto Social API.

## Clonar el repositorio

Para probar el proyecto, clona el repositorio usando el siguiente comando:

```bash
git clone https://github.com/tu_usuario/social_api.git
```

## Configuracion de variables

Debe setearse la variable SECRET_KEY.
- Se puede declarar en un *.env*
- O se puede ejecutar desde bash

```bash
export SECRET_KEY (Aquí tu SECRET_KEY)
```

### Nota

Se puede conseguir un [acá](https://theorangeone.net/projects/django-secret-key-generator/)


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

5. **Crear un superusuario (Importante para poder solicitar token e interacuar con la API):**

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

**Ejecutar pytest:**

```bash
pytest
```

### Con Docker

**Ejecutar pytest en el contenedor:**

```bash
docker exec -it social_api-web-1 pytest
```

## Datos adicionales

- El proyecto tiene un pipeline configurado. Que realiza test unitarios y buildea la imagen y la pushea al mi repositorio de *dockerhub*.(No corre)

https://hub.docker.com/r/jeremyakd/social_api

- Ademas se agrega *Swagger* para documentacion y pruebas de la API. Mas info [aca](https://swagger.io/) (Quedó a medias)

- Uso de pre-commit (herramienta de formateo y reglas de python)

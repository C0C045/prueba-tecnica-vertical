# Prueba Técnica Verticcal

> **Resumen:**
>
> Este README recoge todas las instrucciones para ejecutar **localmente** el entregable completo: API en **FastAPI**, **Postgres**, flujo en **n8n**, scripts de seeds y la **Parte D** (meta-prompt + pruebas). Sigue los pasos exactamente para reproducir el entorno tal como será evaluado.

---

## Índice

1. Requisitos (prerrequisitos)
2. Estructura del repositorio (qué incluye)
3. Variables de entorno (`.env`)
4. Levantar el stack (Docker Compose)
5. Scripts útiles (seed)
6. Endpoints relevantes y ejemplos de uso
7. n8n — Importar el flujo y configuración
8. Parte D — Meta-prompt y cómo probarlo

---

## 1) Requisitos

* Docker y Docker Compose (o Docker Desktop con Compose V2).
* (Opcional) Python 3.11 en tu máquina si quieres ejecutar scripts localmente fuera del contenedor.

---

## 2) Estructura del repositorio

```
root/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ routers/
│  │  ├─ __init__.py
│  │  ├─ external.py
│  │  └─ leads.py
│  └─ services/
│     ├─ __init__.py
│     ├─ crud.py
│     └─ external_api.py
│
├─ scripts/
│  └─ seed_leads.py
│
├─ Dockerfile
├─ requirements.txt
├─ docker-compose.yml
├─ .env
├─ n8n_flow.json      # flujo n8n que se importa en n8n (Parte C)
├─ prompt_example.md           # meta-prompt + ejemplos (Parte D)
└─ README.md
```

---

## 3) `.env`

Coloca un archivo `.env` en la misma carpeta donde está `docker-compose.yml`.

Ejemplo (`.env`):

```env
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
DATABASE_URL=...
```

**Notas:**

* Docker Compose carga automáticamente `.env` si está en la misma carpeta.
* Para pasar otro archivo `.env` usa `docker compose --env-file .env.dev up`.

---

## 4) Levantar el stack

**Comando (desde la raíz del repo):**

```bash
docker compose up --build
```

Servicios y puertos por defecto:

* Postgres → `localhost:5432`
* n8n → `http://localhost:5678`
* FastAPI → `http://localhost:8000` (Swagger: `http://localhost:8000/docs`)

**Parar y limpiar:**

```bash
CTRL + C
ó
docker compose down
```

---

## 5) Scripts útiles: seed

### Sembrar leads (seed)

Dentro del contenedor FastAPI:

```bash
docker compose exec fastapi python scripts/seed_leads.py
```

> `scripts/seed_leads.py` inserta los leads de ejemplo. Por otro lado, si así lo quieres también puedes insertar los leads de ejemplo en el flujo de n8n. **Ver:** [Usos del Webhook](#usos-del-webhook)

---

## 6) Endpoints (FastAPI) y ejemplos

### Documentación interactiva

`http://localhost:8000/docs`

### Endpoints principales implementados

* `GET /` → salud básica

* `GET /leads` → devuelve los leads desde Postgres. Query params: `skip`, `limit`

  * Ejemplo:

    ```bash
    curl http://localhost:8000/leads
    ```

* `POST /leads` → crea un lead (body: `name`, `location`, `budget`)

  * Ejemplo:

    ```bash
    curl -X POST http://localhost:8000/leads -H "Content-Type: application/json" \
      -d '{"name":"Steven Espejo","location":"Bogotá","budget":1250300}'
    ```
  * **IMPORTANTE:** `id` no debe ser enviado; Postgres crea el id automáticamente.

* `DELETE /leads/{lead_id}` → elimina un lead.

  * Ejemplo:

    ```bash
    curl -X DELETE http://localhost:8000/leads/2
    ```

* `GET /external-data` → proxy hacia la API pública (JSONPlaceholder)
    
  * Ejemplo:

    ```bash
    curl http://localhost:8000/external-data
    ```
  * **IMPORTANTE:** La API JSONPlaceholder se usó por simplicidad, además, que su estructura de datos permite hacer un buen procesamiento de datos.
    
    Tipo de dato consumido:
    ```json
    {
      "userId": 1,
      "id": 1,
      "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
      "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
    }
    ```

* `GET /external-data/filter` → filtra datos externos.  Query params: `user_id`

  * Ejemplo:

    ```bash
    curl http://localhost:8000/external-data/filter?user_id=1
    ```

---

## 7) n8n — importar flujo y configurar

### Importar

1. Abre `http://localhost:5678`.
2. Inicia sesión.
3. Crear Workflow vacio
4. ... (ajustes) → **Import from File** → Selecciona el JSON del fichero `n8n_flow.json`.
5. Edita las credenciales de los nodos Postgres (`Insertar Semillas`, `Leer Leads`):

   * Host: `postgres` (si n8n corre en Docker junto a Postgres).
   * Database: `n8n_db`
   * User: `n8n`
   * Password: `n8n_password`
   * Port: `5432`

### Arquitectura esperada después de la importación
<img width="1532" height="207" alt="image" src="https://github.com/user-attachments/assets/5654c6d8-6721-4f88-8d09-06d66c9303cf" />

### Usos del Webhook

* **Parámetros aceptados**: `location`, `budget_min`, `budget_max`, `seed=true (opcional)`
* Sembrar + consultar:
  
  `GET http://localhost:5678/webhook-test/leads?seed=true`
* Solo consultar y filtrar:

  `GET http://localhost:5678/webhook-test/leads?location=Bogotá&budget_min=100000000`
* Ejemplos de posibles consultas:

  `GET http://localhost:5678/webhook-test/leads?location=Medellín&budget_min=200000000&budget_max=500000000`

  `GET http://localhost:5678/webhook-test/leads?location=Bogotá`

**Respuesta esperada dada una consulta:**

`GET http://localhost:5678/webhook-test/leads?location=Medellín&budget_min=200000000&budget_max=500000000`
```json
  {
    "filters": {
      "location": "Medellín",
      "budget_min": "200000000",
      "budget_max": "500000000"
    },
    "count": 2,
    "total_budget": 700000000,
    "leads": [
      {
        "id": 2,
        "name": "Santiago Gallo",
        "location": "Medellín",
        "budget": "500000000",
        "_total_budget": 700000000
      },
      {
        "id": 1,
        "name": "Ana Salcedo",
        "location": "Medellín",
        "budget": "200000000",
        "_total_budget": 700000000
      }
    ]
  }
```

---

## 8) Parte D — Meta-prompt y cómo probarlo

### Archivo

`prompt_example.md` (incluido en repo) contiene la plantilla / meta-prompt + 3 ejemplos (recepción, diagnóstico, resolución).

### Probar manualmente

* Copia la plantilla y pégala en una conversación con ChatGPT (u otro LLM).
* Añade un `Input` con `Estado` y `Descripción del problema`.

**Ejemplo:**

```
[Meta-prompt...]

INPUT:
Estado: recepción
Usuario reporta: "No puedo acceder a la plataforma desde ayer"
```

---

## Ejemplos rápidos de comandos (resumen)

Levantar todo:

```bash
docker compose up --build
```

Sembrar desde FastAPI:

```bash
docker compose exec fastapi python scripts/seed_leads.py
```

Consultar leads e información externa (FastAPI Swagger):

```bash
http://localhost:8000/docs
```

Probar n8n y Sembrar desde n8n:

```bash
curl "http://localhost:5678/webhook-test/leads?seed=true"
```

Filtrado y organizado con n8n:

```bash
curl "http://localhost:5678/webhook-test/leads?location=Medellín&budget_min=200000000&budget_max=500000000"
```

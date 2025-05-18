
# TalaTrivia API

**TalaTrivia** es una API RESTful desarrollada como parte de una prueba técnica para el cargo de Software Developer Engineer en **Talana**. La API permite gestionar trivias relacionadas con recursos humanos, incluyendo creación de usuarios, preguntas, trivias, participación y ranking.

---

## 📦 Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- PostgreSQL
- Docker & docker-compose

---

## Instalación

### Requisitos

- Docker
- Docker Compose

### Pasos

1. Clonar el proyecto:
   ```bash
   git clone https://github.com/MarceloDev-code/prueba-tecnica-talana.git
   cd talatrivia
   ```

2. Construir e iniciar los contenedores:
   ```bash
   docker compose up --build
   ```

3. Acceder a la API:
   ```
   http://localhost:8000/api/
   ```

4. Swagger Docs:
   ```
   http://localhost:8000/api/docs/
   ```

---

## Credenciales por defecto

Un superusuario se crea automáticamente:

- **Usuario:** `admin`
- **Email:** `admin@example.com`
- **Contraseña:** `admin123`

---

## Endpoints principales

| Método | Ruta                                 | Descripción                           |
|--------|--------------------------------------|---------------------------------------|
| POST   | `/api/users/`                        | Crear usuario                         |
| GET    | `/api/trivias/`                      | Listar trivias                        |
| POST   | `/api/trivias/{id}/play/{user_id}/`  | Enviar respuestas a trivia            |
| GET    | `/api/trivias/{id}/ranking/`         | Ver ranking de trivia                 |
| POST   | `/api/admin/questions/bulk/`         | Cargar preguntas en lote              |
| GET    | `/api/users/{id}/trivias/`           | Ver trivias asignadas al usuario      |

---

## Notas

- Los puntajes se calculan automáticamente según la dificultad de cada pregunta (`easy=1`, `medium=2`, `hard=3`).
- Los jugadores no pueden ver cuál es la respuesta correcta al recibir la trivia.

---


## How to launch the project

1. Install `requirements.txt` via `pip` in `venv`.
2. Build an image for the database using `docker-compose.yml`.
3. Start the server. E.g. `uvicorn src.main:app --env .env`.
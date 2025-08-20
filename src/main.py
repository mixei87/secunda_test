import logging
from fastapi import FastAPI
from src.api.v1.router import api_router
from src.core.handlers import register_exception_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Справочник организаций", version="1.0")

# Регистрация обработчиков исключений
register_exception_handlers(app)
logger.info("Инициализировано приложение и обработчики исключений")

# Mount API v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}

#!/usr/bin/env bash
set -euo pipefail

echo "=== Начало выполнения entrypoint.sh ==="

# Инициализируем PYTHONPATH с пустым значением по умолчанию
PYTHONPATH="${PYTHONPATH:-}"

# Добавляем корень проекта в PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/app"

# Опциональное заполнение начальными данными
if [ "${SEED_DATA}" = "true" ]; then
    echo "Заполнение базы начальными данными..."
    if PYTHONPATH="${PYTHONPATH}" python /src/scripts/seed_data.py; then
        echo "✅ Начальные данные успешно загружены"
    else
        echo "❌ Ошибка при заполнении начальными данными!"
        exit 1
    fi
else
    echo "ℹ️  Пропуск заполнения начальными данными (SEED_DATA=false)"
fi

echo "=== Завершение entrypoint.sh ==="

# start src
exec uvicorn src.main:app --host "${API_HOST}" --port "${CONTAINER_API_PORT}" --reload

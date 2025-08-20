.PHONY: up upb d b rs migrate-create migrate-downgrade

C = docker compose
B = COMPOSE_BAKE=true

up:
	$(C) up -d

upb:
	$(B) $(C) up -d --build

d:
	$(C) down

b:
	$(B) $(C) build

rs:
	$(C) restart

# Создать новую миграцию (указать m="описание изменений")
mig_b:
	$(C) exec app alembic revision --autogenerate -m "$(m)"

# Применить последнюю миграцию
mig_up:
	$(C) exec app alembic upgrade head

# Откатить последнюю миграцию
mig_d:
	$(C) exec app alembic downgrade -1



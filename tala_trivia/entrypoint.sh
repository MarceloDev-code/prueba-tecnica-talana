#!/bin/bash

echo "⏳ Esperando a la base de datos en $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "✅ Base de datos disponible. Ejecutando migraciones..."
python manage.py migrate

sleep 2

echo "⚙️ Creando superusuario si no existe..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
EOF

echo "🚀 Iniciando servidor Django..."
exec "$@"

#!/bin/sh
set -e

# Sur un volume neuf, init.sql a déjà créé les tables avec le bon schéma.
# Si la table alembic_version n'existe pas encore, on stampe à head pour
# éviter que flask db upgrade tente de modifier des tables qui existent déjà.
HAS_ALEMBIC=$(python3 -c "
import os, pymysql
try:
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME'],
    )
    cur = conn.cursor()
    cur.execute(\"SHOW TABLES LIKE 'alembic_version'\")
    print('yes' if cur.fetchone() else 'no')
    conn.close()
except Exception as e:
    print('no')
")

if [ "$HAS_ALEMBIC" = "no" ]; then
    echo "Nouveau volume détecté — synchronisation Alembic avec le schéma existant..."
    flask db stamp head
fi

flask db upgrade

exec "$@"

-- =========================================================
-- NeuroCRM - Esquema de historial para n8n (Entregable 5)
-- =========================================================
-- Este script crea las tablas donde n8n guardará, mediante
-- el nodo Postgres, cada consulta hecha a la API de FastAPI
-- junto con el resultado devuelto por el modelo de IA.
--
-- Cómo usarlo:
--   Opción A (automático): monta este archivo en el contenedor
--   de postgres en docker-compose.yml así:
--
--   postgres:
--     volumes:
--       - postgres_data:/var/lib/postgresql/data
--       - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
--
--   (Solo se ejecuta la PRIMERA vez que se crea el volumen.
--   Si ya tienes el volumen creado, corre este archivo a mano:
--   docker exec -i neurocrm_db psql -U neuro_user -d neurocrm < database/init.sql)
--
--   Opción B (manual): pégalo directo en una query desde
--   pgAdmin, DBeaver o el nodo "Execute Query" de n8n una sola vez.
-- =========================================================

CREATE TABLE IF NOT EXISTS leads_historial (
    id                      SERIAL PRIMARY KEY,
    presupuesto_min         NUMERIC NOT NULL,
    fuente_lead             INTEGER NOT NULL,
    tipo_propiedad          INTEGER NOT NULL,
    interacciones_iniciales INTEGER NOT NULL,
    score                   INTEGER NOT NULL,
    categoria               VARCHAR(30) NOT NULL,
    creado_en               TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS churn_historial (
    id                    SERIAL PRIMARY KEY,
    antiguedad_meses      INTEGER NOT NULL,
    dias_inactividad      INTEGER NOT NULL,
    interacciones_30d     INTEGER NOT NULL,
    quejas_registradas    INTEGER NOT NULL,
    probabilidad_churn    INTEGER NOT NULL,
    riesgo_abandono       VARCHAR(10) NOT NULL,
    creado_en             TIMESTAMP NOT NULL DEFAULT NOW()
);

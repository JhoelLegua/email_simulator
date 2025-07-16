import psycopg2
import json
import os
from datetime import datetime

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'dbname': 'email_simulator',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id SERIAL PRIMARY KEY,
            sender TEXT NOT NULL,
            recipients TEXT NOT NULL,  -- JSON array
            subject TEXT,
            body_text TEXT,
            raw_message TEXT,
            status TEXT DEFAULT 'unread',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

def add_email(sender, recipients, subject, body_text, raw_message):
    """Añade un nuevo correo a la base de datos"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO emails (sender, recipients, subject, body_text, raw_message)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (sender, json.dumps(recipients), subject, body_text, raw_message))
        email_id = cursor.fetchone()[0]
        conn.commit()
        return email_id

def get_all_emails(status_filter=None):
    """Recupera todos los correos, opcionalmente filtrados por estado"""
    with get_conn() as conn:
        cursor = conn.cursor()
        if status_filter:
            cursor.execute('SELECT * FROM emails WHERE status = %s ORDER BY timestamp DESC', (status_filter,))
        else:
            cursor.execute('SELECT * FROM emails ORDER BY timestamp DESC')
        return cursor.fetchall()

def get_email_by_id(email_id):
    """Recupera un correo específico por su ID"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM emails WHERE id = %s', (email_id,))
        return cursor.fetchone()

def update_email_status(email_id, new_status):
    """Actualiza el estado de un correo"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE emails SET status = %s WHERE id = %s', (new_status, email_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_email_permanently(email_id):
    """Elimina físicamente un correo de la base de datos"""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM emails WHERE id = %s', (email_id,))
        conn.commit()
        return cursor.rowcount > 0

# Inicializar la base de datos al importar el módulo
init_db()

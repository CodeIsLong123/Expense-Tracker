import psycopg2
from psycopg2 import Error
import os


# Verbindung zur PostgreSQL-Datenbank herstellen


try:
    connection = psycopg2.connect(
        user= "username"
        password="password",
        host="localhost",
        database="test_db",
    )
    print("PostgreSQL-Datenbankverbindung erfolgreich hergestellt")
    cursor = connection.cursor()

    # SQL-Befehl zum Erstellen der Tabelle
    set_up_db = """
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        amount FLOAT NOT NULL,
        category VARCHAR(255) NOT NULL
    );
    """

    # Tabelle erstellen
    cursor.execute(set_up_db)
    connection.commit()
    print("Tabelle 'transactions' erfolgreich erstellt!")

except Error as e:
    print(f"Fehler beim Erstellen der Tabelle: {e}")

finally:
    # Verbindung schließen
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL-Verbindung wurde geschlossen")




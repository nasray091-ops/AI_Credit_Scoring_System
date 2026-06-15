import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "credit_system.db"


# ======================
# CONNECTION
# ======================

def get_connection():

    return sqlite3.connect(DB_NAME)


# ======================
# INITIALIZE DATABASE
# ======================

def init_db():

    conn = get_connection()

    cur = conn.cursor()

    # USERS

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT,

            role TEXT,

            email TEXT

        )
        """
    )

    # PREDICTIONS

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,

            age INTEGER,

            income REAL,

            credit_limit REAL,

            payment_history REAL,

            credit_score REAL,

            risk_level TEXT,

            recommendation TEXT,

            created_at TEXT

        )
        """
    )

    # ACTIVITY LOGS

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,

            action TEXT,

            details TEXT,

            created_at TEXT

        )
        """
    )

    # DEFAULT ADMIN

    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (
            username,
            password,
            role,
            email
        )
        VALUES
        (
            'admin',
            'admin123',
            'admin',
            'admin@gmail.com'
        )
        """
    )

    conn.commit()

    conn.close()


# ======================
# USERS
# ======================

def user_exists(username):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    return row is not None


def create_user(
    username,
    password,
    role,
    email
):

    try:

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                role,
                email
            )
            VALUES(?,?,?,?)
            """,
            (
                username,
                password,
                role,
                email
            )
        )

        conn.commit()

        conn.close()

        return True, "Account created successfully"

    except Exception as e:

        return False, str(e)


def authenticate(
    username,
    password
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT role
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            password
        )
    )

    row = cur.fetchone()

    conn.close()

    if row:

        return True, row[0]

    return False, None


def change_password(
    username,
    new_password
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            new_password,
            username
        )
    )

    conn.commit()

    conn.close()

    return True, "Password updated successfully"


def get_all_users():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            username,
            role,
            email
        FROM users
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df


# ======================
# PREDICTIONS
# ======================

def save_prediction(
    username,
    age,
    income,
    credit_limit,
    payment_history,
    credit_score,
    risk_level,
    recommendation
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO predictions(

            username,
            age,
            income,
            credit_limit,
            payment_history,
            credit_score,
            risk_level,
            recommendation,
            created_at

        )

        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (
            username,
            age,
            income,
            credit_limit,
            payment_history,
            credit_score,
            risk_level,
            recommendation,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()

    conn.close()


def load_predictions():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM predictions
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df


# ======================
# ACTIVITY LOGS
# ======================

def log_activity(
    username,
    action,
    details
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO activity_logs(

            username,
            action,
            details,
            created_at

        )

        VALUES(?,?,?,?)
        """,
        (
            username,
            action,
            details,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()

    conn.close()


def load_activity_logs():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM activity_logs
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df
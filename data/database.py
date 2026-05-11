import csv
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        self.migrate_tables()

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_no TEXT,
                client_name TEXT NOT NULL,
                client_phone TEXT,
                car_make TEXT,
                car_model TEXT,
                reg_no TEXT,
                vin TEXT,
                parking_spot TEXT,
                status TEXT,
                intake_date TEXT,
                due_date TEXT,
                issue_description TEXT,
                replaced_parts TEXT,
                parts_cost REAL DEFAULT 0,
                labor_cost REAL DEFAULT 0,
                is_paid INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def migrate_tables(self):
        columns = {row[1] for row in self.conn.execute("PRAGMA table_info(orders)").fetchall()}
        extra_columns = {
            "priority": "TEXT DEFAULT 'Normalna'",
            "assigned_mechanic": "TEXT",
            "parts_ordered": "TEXT",
            "customer_price": "REAL DEFAULT 0",
            "paid_amount": "REAL DEFAULT 0",
            "is_archived": "INTEGER DEFAULT 0",
            "last_contact_date": "TEXT",
        }
        for name, sql_type in extra_columns.items():
            if name not in columns:
                self.conn.execute(f"ALTER TABLE orders ADD COLUMN {name} {sql_type}")
        self.conn.commit()

    def generate_next_order_no(self):
        year = datetime.now().strftime("%Y")
        like = f"WM/{year}/%"
        rows = self.conn.execute(
            "SELECT order_no FROM orders WHERE order_no LIKE ? ORDER BY id DESC LIMIT 200", (like,)
        ).fetchall()
        max_num = 0
        for row in rows:
            order_no = row["order_no"] or ""
            parts = order_no.split("/")
            if len(parts) == 3 and parts[0] == "WM" and parts[1] == year:
                try:
                    max_num = max(max_num, int(parts[2]))
                except ValueError:
                    pass
        return f"WM/{year}/{max_num + 1:04d}"

    def add_order(self, data: dict):
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = list(data.values())
        self.conn.execute(f"INSERT INTO orders ({keys}) VALUES ({placeholders})", values)
        self.conn.commit()

    def update_order(self, order_id: int, data: dict):
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = list(data.values()) + [order_id]
        self.conn.execute(
            f"UPDATE orders SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            values,
        )
        self.conn.commit()

    def delete_order(self, order_id: int):
        self.conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        self.conn.commit()

    def fetch_orders(self, search_text: str = "", status: str = "Wszystkie", archived: int = 0):
        query = "SELECT * FROM orders WHERE is_archived = ?"
        params = [archived]
        if search_text:
            query += (
                " AND (order_no LIKE ? OR client_name LIKE ? OR client_phone LIKE ? OR assigned_mechanic LIKE ? OR "
                "car_make LIKE ? OR car_model LIKE ? OR reg_no LIKE ? OR vin LIKE ? OR issue_description LIKE ? OR notes LIKE ?)"
            )
            like = f"%{search_text}%"
            params.extend([like] * 10)
        if status != "Wszystkie":
            query += " AND status = ?"
            params.append(status)
        query += (
            " ORDER BY "
            "CASE priority WHEN 'Pilne' THEN 1 WHEN 'Wysoka' THEN 2 WHEN 'Normalna' THEN 3 ELSE 4 END, "
            "CASE status WHEN 'W trakcie' THEN 1 WHEN 'Diagnoza' THEN 2 WHEN 'Oczekuje na części' THEN 3 "
            "WHEN 'Nowe' THEN 4 WHEN 'Gotowe do odbioru' THEN 5 WHEN 'Odebrane' THEN 6 ELSE 7 END, "
            "COALESCE(due_date, ''), id DESC"
        )
        return self.conn.execute(query, params).fetchall()

    def fetch_order(self, order_id: int):
        return self.conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

    def stats(self):
        total = self.conn.execute("SELECT COUNT(*) FROM orders WHERE is_archived = 0 AND status != 'Odebrane'").fetchone()[0]
        waiting_parts = self.conn.execute("SELECT COUNT(*) FROM orders WHERE is_archived = 0 AND status = 'Oczekuje na części'").fetchone()[0]
        in_progress = self.conn.execute("SELECT COUNT(*) FROM orders WHERE is_archived = 0 AND status = 'W trakcie'").fetchone()[0]
        diagnosis = self.conn.execute("SELECT COUNT(*) FROM orders WHERE is_archived = 0 AND status = 'Diagnoza'").fetchone()[0]
        ready = self.conn.execute("SELECT COUNT(*) FROM orders WHERE is_archived = 0 AND status = 'Gotowe do odbioru'").fetchone()[0]
        unpaid_sum = self.conn.execute(
            "SELECT COALESCE(SUM((CASE WHEN customer_price > 0 THEN customer_price ELSE (parts_cost + labor_cost) END) - paid_amount), 0) "
            "FROM orders WHERE is_archived = 0 AND ((CASE WHEN customer_price > 0 THEN customer_price ELSE (parts_cost + labor_cost) END) - paid_amount) > 0"
        ).fetchone()[0]
        archived = self.conn.execute("SELECT COUNT(*) FROM orders WHERE is_archived = 1").fetchone()[0]
        return {
            "total": total,
            "waiting_parts": waiting_parts,
            "in_progress": in_progress,
            "diagnosis": diagnosis,
            "ready": ready,
            "unpaid_sum": unpaid_sum,
            "archived": archived,
        }

    def export_csv(self, filepath: str):
        rows = self.conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        if not rows:
            return 0
        headers = rows[0].keys()
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(headers)
            for row in rows:
                writer.writerow([row[h] for h in headers])
        return len(rows)

import json


class GenericRecordService:
    """Minimal storage service for future custom-section records."""

    def __init__(self, db):
        self.db = db

    def create_record(self, section_id: str, record_type_id: str | None = None, data: dict | None = None) -> int:
        section_id = self._require_id(section_id, "section_id")
        data_json = self._encode_data(data)
        cursor = self.db.conn.execute(
            """
            INSERT INTO generic_records (section_id, record_type_id, data_json)
            VALUES (?, ?, ?)
            """,
            (section_id, record_type_id, data_json),
        )
        self.db.conn.commit()
        return int(cursor.lastrowid)

    def fetch_record(self, record_id: int):
        return self.db.conn.execute(
            "SELECT * FROM generic_records WHERE id = ?",
            (record_id,),
        ).fetchone()

    def list_records(self, section_id: str, archived: int = 0):
        section_id = self._require_id(section_id, "section_id")
        return self.db.conn.execute(
            """
            SELECT * FROM generic_records
            WHERE section_id = ? AND archived = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (section_id, archived),
        ).fetchall()

    def update_record(self, record_id: int, data: dict, record_type_id: str | None = None) -> None:
        data_json = self._encode_data(data)
        if record_type_id is None:
            self.db.conn.execute(
                """
                UPDATE generic_records
                SET data_json = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (data_json, record_id),
            )
        else:
            self.db.conn.execute(
                """
                UPDATE generic_records
                SET record_type_id = ?, data_json = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (record_type_id, data_json, record_id),
            )
        self.db.conn.commit()

    def set_archived(self, record_id: int, archived: bool = True) -> None:
        self.db.conn.execute(
            """
            UPDATE generic_records
            SET archived = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (1 if archived else 0, record_id),
        )
        self.db.conn.commit()

    def delete_record(self, record_id: int) -> None:
        self.db.conn.execute("DELETE FROM generic_records WHERE id = ?", (record_id,))
        self.db.conn.commit()

    def decode_data(self, row) -> dict:
        if row is None:
            return {}
        try:
            data = json.loads(row["data_json"] or "{}")
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    def _encode_data(self, data: dict | None) -> str:
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise ValueError("Generic record data must be a dictionary.")
        return json.dumps(data, ensure_ascii=False)

    def _require_id(self, value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} is required.")
        return value.strip()

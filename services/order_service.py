from datetime import date, datetime


class OrderService:
    """Transitional record/order service for the current orders-based model."""

    def __init__(self, db):
        self.db = db

    def generate_next_order_no(self):
        return self.db.generate_next_order_no()

    def calculate_due_state(self, due_date_value: str, status: str):
        if not due_date_value or status in ("Gotowe do odbioru", "Odebrane"):
            return None, due_date_value or "", None
        try:
            days_left = (datetime.strptime(due_date_value, "%Y-%m-%d").date() - date.today()).days
        except ValueError:
            return None, due_date_value, None
        if days_left <= 3:
            return "due_overdue", f"{due_date_value} ({days_left} d)", days_left
        if days_left <= 10:
            return "due_soon", f"{due_date_value} ({days_left} d)", days_left
        return "due_ok", f"{due_date_value} ({days_left} d)", days_left

    def row_matches_search(self, row, search_text: str, search_mode: str) -> bool:
        if not search_text:
            return True
        st = search_text.lower()
        if search_mode == "Nr zlecenia":
            return st in str(row["order_no"] or "").lower()
        values = [
            row["order_no"], row["client_name"], row["client_phone"], row["assigned_mechanic"], row["car_make"], row["car_model"],
            row["reg_no"], row["vin"], row["issue_description"], row["notes"], row["parts_ordered"], row["replaced_parts"],
        ]
        return any(st in str(v or "").lower() for v in values)

    def parse_order_no_for_sort(self, order_no: str):
        if not order_no:
            return ("", 0, 0)
        parts = str(order_no).split("/")
        if len(parts) == 3:
            prefix, year, number = parts
            try:
                return (prefix, int(year), int(number))
            except ValueError:
                pass
        digits = "".join(ch for ch in str(order_no) if ch.isdigit())
        return (str(order_no), 0, int(digits) if digits else 0)

    def apply_sort(self, rows, field: str, descending: bool):
        priority_rank = {"Pilne": 4, "Wysoka": 3, "Normalna": 2, "Niska": 1}

        def due_key(row):
            return row["due_date"] or ("9999-99-99" if descending else "0000-00-00")

        if field == "ID":
            return sorted(rows, key=lambda row: int(row["id"] or 0), reverse=bool(descending))
        if field == "Nr zlecenia":
            return sorted(rows, key=lambda row: self.parse_order_no_for_sort(row["order_no"] or ""), reverse=bool(descending))
        if field == "Data dodania":
            return sorted(rows, key=lambda row: ((row["created_at"] or ""), int(row["id"] or 0)), reverse=bool(descending))
        if field == "Termin":
            return sorted(rows, key=lambda row: (due_key(row), int(row["id"] or 0)), reverse=bool(descending))
        return sorted(
            rows,
            key=lambda row: (priority_rank.get(row["priority"] or "", 0), row["due_date"] or "9999-99-99", int(row["id"] or 0)),
            reverse=bool(descending),
        )

    def parse_money(self, value: str) -> float:
        value = str(value).strip().replace(",", ".")
        if not value:
            return 0.0
        return float(value)

    def calculate_total(self, row) -> float:
        customer_price = row["customer_price"] or 0
        if customer_price > 0:
            return float(customer_price)
        return float((row["parts_cost"] or 0) + (row["labor_cost"] or 0))

    def calculate_balance(self, row) -> float:
        balance = self.calculate_total(row) - float(row["paid_amount"] or 0)
        return max(balance, 0.0)

    def calculate_paid_amount_for_checkbox(self, form_values):
        total = max(self.parse_money(form_values["customer_price"]), 0.0)
        if total <= 0:
            total = max(self.parse_money(form_values["parts_cost"]) + self.parse_money(form_values["labor_cost"]), 0.0)
        return f"{total:.2f}"

    def build_order_data(self, form_values, text_values, generated_order_no):
        try:
            parts_cost = self.parse_money(form_values["parts_cost"])
            labor_cost = self.parse_money(form_values["labor_cost"])
            customer_price = self.parse_money(form_values["customer_price"])
            paid_amount = self.parse_money(form_values["paid_amount"])
        except ValueError:
            raise ValueError("Koszty i płatności muszą być liczbami.")

        client_name = form_values["client_name"].strip()
        if not client_name:
            raise ValueError("Podaj imię i nazwisko klienta.")

        order_no = form_values["order_no"].strip() or generated_order_no
        effective_total = customer_price if customer_price > 0 else parts_cost + labor_cost
        is_paid = int(form_values["is_paid"])
        if is_paid and paid_amount < effective_total:
            paid_amount = effective_total
        if paid_amount >= effective_total and effective_total > 0:
            is_paid = 1

        return {
            "order_no": order_no,
            "client_name": client_name,
            "client_phone": form_values["client_phone"].strip(),
            "car_make": form_values["car_make"].strip(),
            "car_model": form_values["car_model"].strip(),
            "reg_no": form_values["reg_no"].strip(),
            "vin": form_values["vin"].strip(),
            "parking_spot": form_values["parking_spot"].strip(),
            "status": form_values["status"].strip(),
            "priority": form_values["priority"].strip(),
            "assigned_mechanic": form_values["assigned_mechanic"].strip(),
            "intake_date": form_values["intake_date"].strip(),
            "due_date": form_values["due_date"].strip(),
            "last_contact_date": form_values["last_contact_date"].strip(),
            "issue_description": text_values["issue_description"],
            "replaced_parts": text_values["replaced_parts"],
            "parts_ordered": text_values["parts_ordered"],
            "parts_cost": parts_cost,
            "labor_cost": labor_cost,
            "customer_price": customer_price,
            "paid_amount": paid_amount,
            "is_paid": is_paid,
            "notes": text_values["notes"],
            "is_archived": 0,
        }

    def default_form_values(self):
        return {
            "order_no": self.generate_next_order_no(),
            "status": "Nowe",
            "priority": "Normalna",
            "intake_date": datetime.now().strftime("%Y-%m-%d"),
            "parts_cost": "0",
            "labor_cost": "0",
            "customer_price": "0",
            "paid_amount": "0",
            "is_paid": 0,
        }

    def save_order(self, selected_order_id, data):
        if selected_order_id:
            current = self.db.fetch_order(selected_order_id)
            if current and current["is_archived"]:
                data["is_archived"] = 1
            self.db.update_order(selected_order_id, data)
            return "updated"
        self.db.add_order(data)
        return "created"

    def duplicate_order_data(self, source):
        data = dict(source)
        for key in ("id", "created_at", "updated_at"):
            data.pop(key, None)
        data["order_no"] = self.generate_next_order_no()
        data["status"] = "Nowe"
        data["is_archived"] = 0
        return data

    def delete_order(self, order_id):
        self.db.delete_order(order_id)

    def update_status(self, order_id, status: str):
        self.db.update_order(order_id, {"status": status})

    def archive_order(self, order_id):
        self.db.update_order(order_id, {"is_archived": 1})

    def restore_order(self, order_id):
        self.db.update_order(order_id, {"is_archived": 0})

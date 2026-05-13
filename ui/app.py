import json
import os
import tkinter as tk
from dataclasses import replace
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from data.database import Database
from services.config_service import ConfigService
from services.order_service import OrderService

APP_TITLE = "Warsztat Manager Premium"
DEFAULT_APP_TITLE = "Manager"
DB_NAME = "warsztat_manager.db"
SETTINGS_NAME = "settings.json"
STATUSES = [
    "Nowe",
    "Diagnoza",
    "Oczekuje na części",
    "W trakcie",
    "Gotowe do odbioru",
    "Odebrane",
]
PRIORITIES = ["Niska", "Normalna", "Wysoka", "Pilne"]

THEMES = {
    "light": {
        "window_bg": "#efefef",
        "panel_bg": "#f6f6f6",
        "group_bg": "#f4f4f4",
        "text": "#111111",
        "muted": "#555555",
        "entry_bg": "#ffffff",
        "header_bg": "#dcdcdc",
        "header_text": "#111111",
        "selected": "#316ac5",
        "selected_text": "#ffffff",
        "button_bg": "#e8e8e8",
        "button_active": "#dcdcdc",
        "accent": "#0a64ad",
        "danger": "#a62020",
        "tree_bg": "#ffffff",
        "alt_tree_bg": "#f8f8f8",
        "summary_bg": "#ffffff",
    },
    "dark": {
        "window_bg": "#1a1c20",
        "panel_bg": "#24272d",
        "group_bg": "#2b2f36",
        "text": "#f5f7fa",
        "muted": "#cfd5dc",
        "entry_bg": "#14161a",
        "header_bg": "#353a43",
        "header_text": "#f5f7fa",
        "selected": "#4d79c7",
        "selected_text": "#ffffff",
        "button_bg": "#343943",
        "button_active": "#424955",
        "accent": "#a7c7ff",
        "danger": "#ffaaaa",
        "tree_bg": "#1f2227",
        "alt_tree_bg": "#262a31",
        "summary_bg": "#20242a",
    },
}

PRIORITY_TAGS = {
    "Pilne": "prio_pilne",
    "Wysoka": "prio_wysoka",
    "Normalna": "prio_normalna",
    "Niska": "prio_niska",
}


def get_app_data_dir() -> str:
    app_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "WarsztatManagerPremium")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


def resource_path(filename: str) -> str:
    return os.path.join(get_app_data_dir(), filename)


def load_window_title() -> str:
    try:
        app_name = ConfigService().load_app_config().app_name.strip()
    except Exception:
        return DEFAULT_APP_TITLE
    return app_name or DEFAULT_APP_TITLE


class SettingsManager:
    def __init__(self, path: str):
        self.path = path
        self.data = {"theme": "light"}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    if isinstance(raw, dict):
                        self.data.update(raw)
            except Exception:
                pass

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value
        self.save()


class WorkshopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_title = load_window_title()
        self.title(self.app_title)
        self.geometry("1366x820")
        self.minsize(1024, 640)
        try:
            self.tk.call("tk", "scaling", 1.0)
        except Exception:
            pass

        self.settings_mgr = SettingsManager(resource_path(SETTINGS_NAME))
        self.current_theme = self.settings_mgr.get("theme", "light")
        self.colors = THEMES[self.current_theme]
        self.configure(bg=self.colors["window_bg"])
        self.style = ttk.Style(self)
        self.db = Database(resource_path(DB_NAME))
        self.order_service = OrderService(self.db)
        self.selected_order_id = None
        self.form_min_width = 660

        self.search_var = tk.StringVar()
        self.archive_search_var = tk.StringVar()
        self.status_filter_var = tk.StringVar(value="Wszystkie")
        self.priority_filter_var = tk.StringVar(value="Wszystkie")
        self.search_mode_var = tk.StringVar(value="Nr zlecenia")
        self.show_overdue_only_var = tk.IntVar(value=0)
        self.archive_status_filter_var = tk.StringVar(value="Wszystkie")
        self.theme_var = tk.BooleanVar(value=self.current_theme == "dark")
        self.sort_field_var = tk.StringVar(value=self.settings_mgr.get("sort_field", "Priorytet"))
        self.sort_desc = self.settings_mgr.get("sort_desc", True)

        self.form_vars = {
            "order_no": tk.StringVar(value=self.order_service.generate_next_order_no()),
            "client_name": tk.StringVar(),
            "client_phone": tk.StringVar(),
            "car_make": tk.StringVar(),
            "car_model": tk.StringVar(),
            "reg_no": tk.StringVar(),
            "vin": tk.StringVar(),
            "parking_spot": tk.StringVar(),
            "status": tk.StringVar(value="Nowe"),
            "priority": tk.StringVar(value="Normalna"),
            "assigned_mechanic": tk.StringVar(),
            "intake_date": tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")),
            "due_date": tk.StringVar(),
            "last_contact_date": tk.StringVar(),
            "parts_cost": tk.StringVar(value="0"),
            "labor_cost": tk.StringVar(value="0"),
            "customer_price": tk.StringVar(value="0"),
            "paid_amount": tk.StringVar(value="0"),
            "is_paid": tk.IntVar(value=0),
        }

        self.build_ui()
        self.bind_shortcuts()
        self.apply_theme(self.current_theme, initial=True)
        self.refresh_all_tables()

    def configure_style(self):
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        c = self.colors
        self.option_add("*Font", "Tahoma 9")
        self.style.configure("TFrame", background=c["window_bg"])
        self.style.configure("Panel.TFrame", background=c["panel_bg"], relief="solid", borderwidth=1)
        self.style.configure("Group.TLabelframe", background=c["group_bg"], relief="groove", borderwidth=2)
        self.style.configure("Group.TLabelframe.Label", background=c["group_bg"], foreground=c["text"], font=("Tahoma", 9, "bold"))
        self.style.configure("TLabel", background=c["window_bg"], foreground=c["text"], font=("Tahoma", 9))
        self.style.configure("Panel.TLabel", background=c["panel_bg"], foreground=c["text"], font=("Tahoma", 9))
        self.style.configure("Summary.TLabel", background=c["summary_bg"], foreground=c["text"], font=("Tahoma", 9, "bold"), anchor="center", relief="solid")
        self.style.configure("Title.TLabel", background=c["window_bg"], foreground=c["text"], font=("Tahoma", 14, "bold"))
        self.style.configure("Sub.TLabel", background=c["window_bg"], foreground=c["muted"], font=("Tahoma", 9))
        self.style.configure("TButton", background=c["button_bg"], foreground=c["text"], padding=(6, 4), relief="raised", borderwidth=1)
        self.style.map("TButton", background=[("active", c["button_active"]), ("pressed", c["button_active"])])
        self.style.configure("Primary.TButton", background=c["button_bg"], foreground=c["accent"], font=("Tahoma", 9, "bold"))
        self.style.configure("Danger.TButton", background=c["button_bg"], foreground=c["danger"], font=("Tahoma", 9, "bold"))
        self.style.configure("TCheckbutton", background=c["window_bg"], foreground=c["text"])
        self.style.map("TCheckbutton", background=[("active", c["window_bg"])], foreground=[("active", c["text"])])
        self.style.configure("TNotebook", background=c["window_bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=c["header_bg"], foreground=c["header_text"], padding=(10, 4), font=("Tahoma", 9, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", c["panel_bg"]), ("active", c["button_active"])])
        self.style.configure("Treeview", background=c["tree_bg"], fieldbackground=c["tree_bg"], foreground=c["text"], rowheight=24, font=("Tahoma", 9), borderwidth=1)
        self.style.configure("Treeview.Heading", background=c["header_bg"], foreground=c["header_text"], font=("Tahoma", 9, "bold"), relief="raised")
        self.style.map("Treeview", background=[("selected", c["selected"])], foreground=[("selected", c["selected_text"])])
        self.style.configure("TCombobox", fieldbackground=c["entry_bg"], background=c["entry_bg"], foreground=c["text"], arrowsize=14)
        self.style.configure("TEntry", fieldbackground=c["entry_bg"], foreground=c["text"])
        self.option_add("*TCombobox*Listbox.background", c["entry_bg"])
        self.option_add("*TCombobox*Listbox.foreground", c["text"])

    def build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = ttk.Frame(self, padding=8)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)
        ttk.Label(top, text="Warsztat Manager Premium", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(top, text="Prosty program warsztatowy z lokalnym zapisem danych", style="Sub.TLabel").grid(row=0, column=1, sticky="w", padx=(10, 0))
        ttk.Button(top, text="⚙", command=self.show_settings_preview).grid(row=0, column=2, sticky="e", padx=(8, 6))
        ttk.Checkbutton(top, text="Tryb ciemny", variable=self.theme_var, command=self.toggle_theme).grid(row=0, column=3, sticky="e")

        self.summary_frame = ttk.Frame(self, padding=(8, 0, 8, 8))
        self.summary_frame.grid(row=1, column=0, sticky="ew")
        self.summary_labels = {}
        summary_items = [
            ("total", "Na placu"),
            ("diagnosis", "Diagnoza"),
            ("in_progress", "W trakcie"),
            ("waiting_parts", "Czeka na części"),
            ("ready", "Gotowe"),
            ("unpaid_sum", "Do zapłaty"),
            ("archived", "Archiwum"),
        ]
        for idx, (key, title) in enumerate(summary_items):
            self.summary_frame.columnconfigure(idx, weight=1, uniform="summary")
            label = ttk.Label(self.summary_frame, text=f"{title}: 0", style="Summary.TLabel", padding=8, anchor="center")
            label.grid(row=0, column=idx, sticky="ew", padx=(0, 6 if idx < len(summary_items)-1 else 0))
            self.summary_labels[key] = label

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.orders_tab = ttk.Frame(self.notebook)
        self.archive_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Aktywne zlecenia")
        self.notebook.add(self.archive_tab, text="Archiwum")

        self.build_orders_tab()
        self.build_archive_tab()

    def load_settings_preview(
        self,
    ) -> tuple[
        list[tuple[str, str]],
        list[tuple[str, str, str, str, str]],
        list[tuple[str, str]],
        list[tuple[str, str, str, str, str]],
        str | None,
    ]:
        try:
            config = ConfigService().load_all()
        except Exception as exc:
            return [
                ("Nazwa aplikacji", DEFAULT_APP_TITLE),
                ("Aktywny typ rekordu", "Brak danych"),
                ("Liczba sekcji/kart", "Brak danych"),
            ], [], [], [], str(exc)

        sections = [
            (
                section.name,
                section.id,
                section.type,
                "Tak" if section.visible else "Nie",
                str(section.order),
            )
            for section in sorted(config.sections, key=lambda item: item.order)
        ]
        record_type = [
            ("ID typu rekordu", config.record_type.id or "Brak danych"),
            ("Nazwa typu rekordu", config.record_type.name or "Brak danych"),
            ("Przypisane pola", ", ".join(config.record_type.fields) or "Brak danych"),
        ]
        fields = [
            (
                field.name,
                field.label,
                field.field_type.value,
                "Tak" if field.required else "Nie",
                ", ".join(f"{option.label} ({option.value})" for option in field.options) or "-",
            )
            for field in config.field_definitions
        ]

        return [
            ("Nazwa aplikacji", config.app_config.app_name or DEFAULT_APP_TITLE),
            ("Aktywny typ rekordu", config.app_config.active_record_type_id or "Brak danych"),
            ("Liczba sekcji/kart", str(len(config.sections))),
        ], sections, record_type, fields, None

    def show_settings_preview(self):
        rows, sections, record_type, fields, error = self.load_settings_preview()
        values = dict(rows)

        window = tk.Toplevel(self)
        window.title("Ustawienia")
        window.transient(self)
        window.resizable(False, False)
        window.configure(bg=self.colors["window_bg"])

        container = ttk.Frame(window, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(1, weight=1)

        ttk.Label(container, text="Ustawienia", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        ttk.Label(container, text="Nazwa aplikacji:", style="TLabel").grid(row=1, column=0, sticky="w", padx=(0, 16), pady=3)
        app_name_var = tk.StringVar(value=values.get("Nazwa aplikacji", DEFAULT_APP_TITLE))
        app_name_entry = ttk.Entry(container, textvariable=app_name_var, width=30)
        app_name_entry.grid(row=1, column=1, sticky="ew", pady=3)

        details = [
            ("Aktywny typ rekordu", values.get("Aktywny typ rekordu", "Brak danych")),
            ("Liczba sekcji/kart", values.get("Liczba sekcji/kart", "Brak danych")),
        ]
        for index, (label, value) in enumerate(details, start=2):
            ttk.Label(container, text=f"{label}:", style="TLabel").grid(row=index, column=0, sticky="w", padx=(0, 16), pady=3)
            ttk.Label(container, text=value, style="TLabel").grid(row=index, column=1, sticky="w", pady=3)

        message_row = len(details) + 2
        note = "Na tym etapie edytowana jest tylko nazwa aplikacji. Karty, typy rekordow i pola zostana dodane pozniej."
        if error:
            note = f"Nie udalo sie zaladowac konfiguracji. Pokazano fallback.\n{error}"
        ttk.Label(container, text=note, style="Sub.TLabel", wraplength=360, justify="left").grid(
            row=message_row,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(12, 10),
        )

        sections_row = message_row + 1
        ttk.Label(container, text="Sekcje aplikacji", style="Panel.TLabel").grid(
            row=sections_row,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(2, 4),
        )
        section_columns = ("name", "id", "type", "visible", "order")
        sections_tree = ttk.Treeview(container, columns=section_columns, show="headings", height=5)
        for column, heading, width in [
            ("name", "Nazwa", 110),
            ("id", "ID", 90),
            ("type", "Typ", 90),
            ("visible", "Widoczna", 75),
            ("order", "Kolejnosc", 75),
        ]:
            sections_tree.heading(column, text=heading)
            sections_tree.column(column, width=width, anchor="w", stretch=False)
        if sections:
            for section in sections:
                sections_tree.insert("", "end", values=section)
        else:
            sections_tree.insert("", "end", values=("Brak danych", "-", "-", "-", "-"))
        sections_tree.grid(row=sections_row + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        record_type_row = sections_row + 2
        ttk.Label(container, text="Typ rekordu", style="Panel.TLabel").grid(
            row=record_type_row,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(2, 4),
        )
        for index, (label, value) in enumerate(record_type, start=record_type_row + 1):
            ttk.Label(container, text=f"{label}:", style="TLabel").grid(row=index, column=0, sticky="w", padx=(0, 16), pady=3)
            ttk.Label(container, text=value, style="TLabel", wraplength=360).grid(row=index, column=1, sticky="w", pady=3)

        fields_row = record_type_row + len(record_type) + 1
        ttk.Label(container, text="Pola", style="Panel.TLabel").grid(
            row=fields_row,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(8, 4),
        )
        field_columns = ("id", "label", "type", "required", "options")
        fields_tree = ttk.Treeview(container, columns=field_columns, show="headings", height=5)
        for column, heading, width in [
            ("id", "ID", 95),
            ("label", "Etykieta", 120),
            ("type", "Typ", 75),
            ("required", "Wymagane", 75),
            ("options", "Opcje", 185),
        ]:
            fields_tree.heading(column, text=heading)
            fields_tree.column(column, width=width, anchor="w", stretch=False)
        if fields:
            for field in fields:
                fields_tree.insert("", "end", values=field)
        else:
            fields_tree.insert("", "end", values=("Brak danych", "-", "-", "-", "-"))
        fields_tree.grid(row=fields_row + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        buttons_row = fields_row + 2
        ttk.Button(
            container,
            text="Zapisz",
            style="Primary.TButton",
            command=lambda: self.save_app_name(app_name_var.get(), window),
        ).grid(row=buttons_row, column=0, sticky="w")
        ttk.Button(container, text="Zamknij", command=window.destroy).grid(row=buttons_row, column=1, sticky="e")

        window.update_idletasks()
        x = self.winfo_rootx() + max((self.winfo_width() - window.winfo_width()) // 2, 0)
        y = self.winfo_rooty() + max((self.winfo_height() - window.winfo_height()) // 2, 0)
        window.geometry(f"+{x}+{y}")
        window.grab_set()

    def save_app_name(self, raw_app_name: str, window: tk.Toplevel | None = None) -> bool:
        app_name = raw_app_name.strip()
        if not app_name:
            messagebox.showerror("Ustawienia", "Nazwa aplikacji nie moze byc pusta.")
            return False

        config_service = ConfigService()
        try:
            config = config_service.load_all()
            updated_app_config = replace(config.app_config, app_name=app_name)
            updated_config = replace(config, app_config=updated_app_config)
            validation = config_service.validate_all(updated_config)
            if not validation.is_valid:
                messagebox.showerror("Ustawienia", "\n".join(validation.errors))
                return False
            config_service.save_app_config(updated_app_config)
        except Exception as exc:
            messagebox.showerror("Ustawienia", f"Nie udalo sie zapisac ustawien.\n\n{exc}")
            return False

        self.app_title = app_name
        self.title(self.app_title)
        messagebox.showinfo("Ustawienia", "Nazwa aplikacji zostala zapisana.")
        if window is not None:
            window.destroy()
        return True

    def build_orders_tab(self):
        main = ttk.Frame(self.orders_tab, padding=8)
        main.pack(fill="both", expand=True)
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        paned = ttk.Panedwindow(main, orient="horizontal")
        paned.grid(row=0, column=0, sticky="nsew")

        left = ttk.Frame(paned, style="Panel.TFrame", padding=8)
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)
        paned.add(left, weight=3)

        right = ttk.Frame(paned, style="Panel.TFrame", padding=8)
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)
        paned.add(right, weight=2)

        toolbar = ttk.Frame(left)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        for idx in range(12):
            toolbar.columnconfigure(idx, weight=0)
        toolbar.columnconfigure(11, weight=1)

        ttk.Label(toolbar, text="Szukaj:").grid(row=0, column=0, sticky="w")
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=(4, 6), sticky="w")
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())
        search_entry.focus_set()

        search_mode = ttk.Combobox(toolbar, textvariable=self.search_mode_var, values=["Nr zlecenia", "Wszystko"], state="readonly", width=12)
        search_mode.grid(row=0, column=2, padx=(0, 10), sticky="w")
        search_mode.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Label(toolbar, text="Status:").grid(row=0, column=3, sticky="w")
        status_combo = ttk.Combobox(toolbar, textvariable=self.status_filter_var, values=["Wszystkie"] + STATUSES, state="readonly", width=16)
        status_combo.grid(row=0, column=4, padx=(4, 8), sticky="w")
        status_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Label(toolbar, text="Priorytet:").grid(row=0, column=5, sticky="w")
        priority_combo = ttk.Combobox(toolbar, textvariable=self.priority_filter_var, values=["Wszystkie"] + PRIORITIES, state="readonly", width=12)
        priority_combo.grid(row=0, column=6, padx=(4, 8), sticky="w")
        priority_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Checkbutton(toolbar, text="Tylko pilne terminy", variable=self.show_overdue_only_var, command=self.refresh_table).grid(row=0, column=7, padx=(0, 10), sticky="w")
        ttk.Label(toolbar, text="Sortuj:").grid(row=0, column=8, padx=(0, 4), sticky="w")
        sort_combo = ttk.Combobox(toolbar, textvariable=self.sort_field_var, values=["Priorytet", "ID", "Nr zlecenia", "Data dodania", "Termin"], width=14, state="readonly")
        sort_combo.grid(row=0, column=9, padx=(0, 4), sticky="w")
        sort_combo.bind("<<ComboboxSelected>>", lambda e: self.on_sort_changed())
        ttk.Button(toolbar, text="Kolejność ▲▼", command=self.toggle_sort_direction).grid(row=0, column=10, padx=(0, 6))
        ttk.Button(toolbar, text="Backup", command=self.backup_database).grid(row=0, column=11, padx=(0, 6))
        ttk.Button(toolbar, text="Eksport CSV", command=self.export_csv).grid(row=0, column=12, padx=(0, 6))
        ttk.Button(toolbar, text="Archiwizuj", command=self.archive_order).grid(row=0, column=13, sticky="w")

        table_wrap = ttk.Frame(left)
        table_wrap.grid(row=1, column=0, sticky="nsew")
        table_wrap.rowconfigure(0, weight=1)
        table_wrap.columnconfigure(0, weight=1)

        columns = (
            "id", "order_no", "priority", "client_name", "car", "reg_no", "assigned_mechanic",
            "parking_spot", "status", "due_date", "created_at", "total", "balance"
        )
        self.tree = ttk.Treeview(table_wrap, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": "ID", "order_no": "Nr zlecenia", "priority": "Priorytet", "client_name": "Klient",
            "car": "Auto", "reg_no": "Rej.", "assigned_mechanic": "Mechanik", "parking_spot": "Miejsce",
            "status": "Status", "due_date": "Termin", "created_at": "Dodano", "total": "Suma", "balance": "Do zapłaty",
        }
        widths = {
            "id": 55, "order_no": 125, "priority": 90, "client_name": 170, "car": 210, "reg_no": 90,
            "assigned_mechanic": 120, "parking_spot": 80, "status": 150, "due_date": 120, "created_at": 145, "total": 90, "balance": 95,
        }
        anchors = {
            "id": "center", "order_no": "center", "priority": "center", "client_name": "w", "car": "w",
            "reg_no": "center", "assigned_mechanic": "w", "parking_spot": "center", "status": "center", "due_date": "center",
            "created_at": "center", "total": "e", "balance": "e",
        }
        heading_commands = {
            "priority": lambda: self.set_sort_field("Priorytet"),
            "id": lambda: self.set_sort_field("ID"),
            "order_no": lambda: self.set_sort_field("Nr zlecenia"),
            "created_at": lambda: self.set_sort_field("Data dodania"),
            "due_date": lambda: self.set_sort_field("Termin"),
        }
        for col in columns:
            if col in heading_commands:
                self.tree.heading(col, text=headings[col], command=heading_commands[col])
            else:
                self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], minwidth=max(70, widths[col] - 40), stretch=False, anchor=anchors[col])
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_wrap, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.build_form_area(right)

    def build_form_area(self, parent):
        form_canvas_wrap = ttk.Frame(parent)
        form_canvas_wrap.grid(row=0, column=0, sticky="nsew")
        form_canvas_wrap.rowconfigure(0, weight=1)
        form_canvas_wrap.columnconfigure(0, weight=1)

        self.form_canvas = tk.Canvas(form_canvas_wrap, highlightthickness=0)
        self.form_canvas.grid(row=0, column=0, sticky="nsew")
        form_vscroll = ttk.Scrollbar(form_canvas_wrap, orient="vertical", command=self.form_canvas.yview)
        form_hscroll = ttk.Scrollbar(form_canvas_wrap, orient="horizontal", command=self.form_canvas.xview)
        form_vscroll.grid(row=0, column=1, sticky="ns")
        form_hscroll.grid(row=1, column=0, sticky="ew")
        self.form_canvas.configure(yscrollcommand=form_vscroll.set, xscrollcommand=form_hscroll.set)

        self.form_inner = ttk.Frame(self.form_canvas)
        self.form_window = self.form_canvas.create_window((0, 0), window=self.form_inner, anchor="nw")
        self.form_inner.bind("<Configure>", self.on_form_configure)
        self.form_canvas.bind("<Configure>", self.on_canvas_configure)

        self.build_form(self.form_inner)

    def build_form(self, parent):
        basic = ttk.LabelFrame(parent, text="Dane podstawowe", style="Group.TLabelframe", padding=8)
        basic.pack(fill="x", pady=(0, 8))
        basic.columnconfigure(1, weight=1)

        self.add_form_row(basic, 0, "Nr zlecenia", "order_no")
        self.add_form_row(basic, 1, "Klient", "client_name")
        self.add_form_row(basic, 2, "Telefon", "client_phone")
        self.add_form_row(basic, 3, "Mechanik", "assigned_mechanic")
        self.add_form_row(basic, 4, "Marka", "car_make")
        self.add_form_row(basic, 5, "Model", "car_model")
        self.add_form_row(basic, 6, "Rejestracja", "reg_no")
        self.add_form_row(basic, 7, "VIN", "vin")
        self.add_form_row(basic, 8, "Miejsce", "parking_spot")

        ops = ttk.LabelFrame(parent, text="Obsługa zlecenia", style="Group.TLabelframe", padding=8)
        ops.pack(fill="x", pady=(0, 8))
        ops.columnconfigure(1, weight=1)
        self.add_combo_row(ops, 0, "Status", "status", STATUSES)
        self.add_combo_row(ops, 1, "Priorytet", "priority", PRIORITIES)
        self.add_form_row(ops, 2, "Przyjęcie", "intake_date")
        self.add_form_row(ops, 3, "Termin", "due_date")
        self.add_form_row(ops, 4, "Kontakt z klientem", "last_contact_date")

        money = ttk.LabelFrame(parent, text="Koszty i płatności", style="Group.TLabelframe", padding=8)
        money.pack(fill="x", pady=(0, 8))
        money.columnconfigure(1, weight=1)
        self.add_form_row(money, 0, "Koszt części", "parts_cost")
        self.add_form_row(money, 1, "Robocizna", "labor_cost")
        self.add_form_row(money, 2, "Cena dla klienta", "customer_price")
        self.add_form_row(money, 3, "Wpłacono", "paid_amount")
        ttk.Checkbutton(money, text="Opłacone w całości", variable=self.form_vars["is_paid"], command=self.sync_payment_checkbox).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        notes_group = ttk.LabelFrame(parent, text="Opis i części", style="Group.TLabelframe", padding=8)
        notes_group.pack(fill="both", expand=True, pady=(0, 8))
        self.issue_text = self.create_text_block(notes_group, "Opis usterki / zakres prac")
        self.parts_text = self.create_text_block(notes_group, "Wymienione części")
        self.parts_ordered_text = self.create_text_block(notes_group, "Części do zamówienia / brakujące")
        self.notes_text = self.create_text_block(notes_group, "Notatki wewnętrzne")

        actions = ttk.Frame(parent)
        actions.pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="Nowe zlecenie", command=self.clear_form).pack(side="left")
        ttk.Button(actions, text="Duplikuj", command=self.duplicate_order).pack(side="left", padx=(6, 0))
        ttk.Button(actions, text="Zapisz / Aktualizuj", style="Primary.TButton", command=self.save_order).pack(side="left", padx=6)
        ttk.Button(actions, text="Usuń", style="Danger.TButton", command=self.delete_order).pack(side="left")
        ttk.Button(actions, text="W trakcie", command=lambda: self.quick_status("W trakcie")).pack(side="right")
        ttk.Button(actions, text="Gotowe", command=lambda: self.quick_status("Gotowe do odbioru")).pack(side="right", padx=6)
        ttk.Button(actions, text="Czeka na części", command=lambda: self.quick_status("Oczekuje na części")).pack(side="right")

    def build_archive_tab(self):
        root = ttk.Frame(self.archive_tab, padding=8)
        root.pack(fill="both", expand=True)
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        top = ttk.Frame(root, style="Panel.TFrame", padding=8)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(top, text="Szukaj w archiwum:").pack(side="left")
        archive_entry = ttk.Entry(top, textvariable=self.archive_search_var, width=30)
        archive_entry.pack(side="left", padx=(4, 10))
        archive_entry.bind("<KeyRelease>", lambda e: self.refresh_archive_table())
        ttk.Label(top, text="Status:").pack(side="left")
        archive_status = ttk.Combobox(top, textvariable=self.archive_status_filter_var, values=["Wszystkie"] + STATUSES, state="readonly", width=20)
        archive_status.pack(side="left", padx=(4, 10))
        archive_status.bind("<<ComboboxSelected>>", lambda e: self.refresh_archive_table())
        ttk.Button(top, text="Odśwież", command=self.refresh_archive_table).pack(side="left")
        ttk.Button(top, text="Przywróć do aktywnych", command=self.restore_archived_order).pack(side="right")

        table_wrap = ttk.Frame(root, style="Panel.TFrame", padding=8)
        table_wrap.grid(row=1, column=0, sticky="nsew")
        table_wrap.rowconfigure(0, weight=1)
        table_wrap.columnconfigure(0, weight=1)

        columns = ("id", "order_no", "client_name", "car", "status", "due_date", "updated_at")
        self.archive_tree = ttk.Treeview(table_wrap, columns=columns, show="headings", selectmode="browse")
        for col, title, width in [
            ("id", "ID", 60), ("order_no", "Nr zlecenia", 140), ("client_name", "Klient", 220),
            ("car", "Auto", 240), ("status", "Status", 180), ("due_date", "Termin", 120), ("updated_at", "Aktualizacja", 180),
        ]:
            self.archive_tree.heading(col, text=title)
            self.archive_tree.column(col, width=width, minwidth=max(70, width - 40), stretch=False, anchor="center")
        self.archive_tree.column("client_name", anchor="w")
        self.archive_tree.column("car", anchor="w")
        self.archive_tree.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.archive_tree.yview)
        hsb = ttk.Scrollbar(table_wrap, orient="horizontal", command=self.archive_tree.xview)
        self.archive_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

    def create_text_block(self, parent, title: str):
        c = self.colors
        ttk.Label(parent, text=title, style="Panel.TLabel").pack(anchor="w", pady=(8, 3))
        txt = tk.Text(parent, height=4, relief="sunken", borderwidth=1, wrap="word", bg=c["entry_bg"], fg=c["text"], insertbackground=c["text"])
        txt.pack(fill="x")
        self.bind_tab_navigation(txt)
        return txt

    def add_form_row(self, parent, row: int, label: str, var_name: str):
        ttk.Label(parent, text=label, style="Panel.TLabel").grid(row=row, column=0, sticky="w", padx=(0, 6), pady=3)
        entry = ttk.Entry(parent, textvariable=self.form_vars[var_name])
        entry.grid(row=row, column=1, sticky="ew", pady=3)
        self.bind_tab_navigation(entry)
        return entry

    def add_combo_row(self, parent, row: int, label: str, var_name: str, values):
        ttk.Label(parent, text=label, style="Panel.TLabel").grid(row=row, column=0, sticky="w", padx=(0, 6), pady=3)
        combo = ttk.Combobox(parent, textvariable=self.form_vars[var_name], values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", pady=3)
        self.bind_tab_navigation(combo)
        return combo

    def on_form_configure(self, event=None):
        req_w = max(self.form_inner.winfo_reqwidth(), self.form_min_width)
        req_h = self.form_inner.winfo_reqheight()
        self.form_canvas.configure(scrollregion=(0, 0, req_w, req_h))
        self.form_canvas.itemconfigure(self.form_window, width=req_w)

    def on_canvas_configure(self, event=None):
        req_w = max(self.form_inner.winfo_reqwidth(), self.form_min_width, event.width)
        self.form_canvas.itemconfigure(self.form_window, width=req_w)

    def bind_shortcuts(self):
        self.bind_all("<Control-s>", lambda e: self.save_order())
        self.bind_all("<Control-n>", lambda e: self.clear_form())
        self.bind_all("<F5>", lambda e: self.refresh_all_tables())

    def bind_tab_navigation(self, widget):
        widget.configure(takefocus=True)
        widget.bind("<Tab>", self.focus_next_widget)
        widget.bind("<Shift-Tab>", self.focus_prev_widget)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus_set()
        return "break"

    def focus_prev_widget(self, event):
        event.widget.tk_focusPrev().focus_set()
        return "break"

    def configure_tree_tags(self):
        c = self.colors
        self.tree.tag_configure("alt", background=c["alt_tree_bg"])
        self.tree.tag_configure("prio_pilne", background="#ffd2d2" if self.current_theme == "light" else "#5f2626", foreground=c["text"], font=("Tahoma", 9, "bold"))
        self.tree.tag_configure("prio_wysoka", background="#ffe9c9" if self.current_theme == "light" else "#5f4821", foreground=c["text"])
        self.tree.tag_configure("prio_normalna", background=c["tree_bg"], foreground=c["text"])
        self.tree.tag_configure("prio_niska", background="#edf5e8" if self.current_theme == "light" else "#243626", foreground=c["text"])
        self.tree.tag_configure("due_overdue", background="#ffcccc" if self.current_theme == "light" else "#6b2a2a", foreground=c["text"], font=("Tahoma", 9, "bold"))
        self.tree.tag_configure("due_soon", background="#fff0b8" if self.current_theme == "light" else "#6a5820", foreground=c["text"])
        self.tree.tag_configure("due_ok", background="#edf5e8" if self.current_theme == "light" else "#24402a", foreground=c["text"])

    def calculate_due_state(self, due_date_value: str, status: str):
        return self.order_service.calculate_due_state(due_date_value, status)

    def on_sort_changed(self):
        self.settings_mgr.set("sort_field", self.sort_field_var.get())
        self.refresh_table()

    def set_sort_field(self, field_name: str):
        current = self.sort_field_var.get()
        if current == field_name:
            self.toggle_sort_direction()
            return
        self.sort_field_var.set(field_name)
        self.on_sort_changed()

    def toggle_sort_direction(self):
        self.sort_desc = not bool(self.sort_desc)
        self.settings_mgr.set("sort_desc", bool(self.sort_desc))
        self.refresh_table()

    def apply_theme(self, theme_name: str, initial: bool = False):
        self.current_theme = theme_name
        self.colors = THEMES[theme_name]
        self.configure(bg=self.colors["window_bg"])
        self.configure_style()
        self.repaint_widgets(self)
        self.configure_tree_tags()
        self.update_idletasks()
        if not initial:
            self.refresh_all_tables()
        self.settings_mgr.set("theme", theme_name)

    def repaint_widgets(self, widget):
        c = self.colors
        if isinstance(widget, tk.Text):
            widget.configure(bg=c["entry_bg"], fg=c["text"], insertbackground=c["text"])
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg=c["panel_bg"])
        for child in widget.winfo_children():
            self.repaint_widgets(child)

    def toggle_theme(self):
        current_geometry = self.geometry()
        self.apply_theme("dark" if self.theme_var.get() else "light")
        self.geometry(current_geometry)

    def refresh_stats(self):
        stats = self.db.stats()
        labels = {
            "total": f"Na placu: {stats['total']}",
            "diagnosis": f"Diagnoza: {stats['diagnosis']}",
            "in_progress": f"W trakcie: {stats['in_progress']}",
            "waiting_parts": f"Czeka na części: {stats['waiting_parts']}",
            "ready": f"Gotowe: {stats['ready']}",
            "unpaid_sum": f"Do zapłaty: {stats['unpaid_sum']:.2f} zł",
            "archived": f"Archiwum: {stats['archived']}",
        }
        for key, text in labels.items():
            self.summary_labels[key].configure(text=text)

    def row_matches_search(self, row, search_text: str) -> bool:
        return self.order_service.row_matches_search(row, search_text, self.search_mode_var.get())

    def parse_order_no_for_sort(self, order_no: str):
        return self.order_service.parse_order_no_for_sort(order_no)

    def apply_sort(self, rows):
        return self.order_service.apply_sort(rows, self.sort_field_var.get(), self.sort_desc)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.db.fetch_orders("", self.status_filter_var.get(), archived=0)
        search_text = self.search_var.get().strip()
        rows = [row for row in rows if self.row_matches_search(row, search_text)]
        priority_filter = self.priority_filter_var.get()
        if priority_filter != "Wszystkie":
            rows = [row for row in rows if (row["priority"] or "") == priority_filter]
        if self.show_overdue_only_var.get():
            filtered = []
            for row in rows:
                _tag, _display, days_left = self.calculate_due_state(row["due_date"], row["status"])
                if days_left is not None and days_left <= 10:
                    filtered.append(row)
            rows = filtered

        rows = self.apply_sort(rows)
        self.configure_tree_tags()
        for idx, row in enumerate(rows):
            total = self.calculate_total(row)
            balance = self.calculate_balance(row)
            car = f"{row['car_make'] or ''} {row['car_model'] or ''}".strip()
            tags = []
            due_tag, display_due, _days_left = self.calculate_due_state(row["due_date"], row["status"])
            priority_tag = PRIORITY_TAGS.get(row["priority"] or "")
            if due_tag:
                tags.append(due_tag)
            elif priority_tag:
                tags.append(priority_tag)
            elif idx % 2 == 1:
                tags.append("alt")
            self.tree.insert(
                "",
                "end",
                iid=str(row["id"]),
                tags=tuple(tags),
                values=(
                    row["id"], row["order_no"] or "", row["priority"] or "", row["client_name"] or "", car,
                    row["reg_no"] or "", row["assigned_mechanic"] or "", row["parking_spot"] or "", row["status"] or "",
                    display_due, (row["created_at"] or "")[:16].replace("T", " "), f"{total:.2f} zł", f"{balance:.2f} zł",
                ),
            )
        self.refresh_stats()

    def refresh_archive_table(self):
        for item in self.archive_tree.get_children():
            self.archive_tree.delete(item)
        rows = self.db.fetch_orders(self.archive_search_var.get().strip(), self.archive_status_filter_var.get(), archived=1)
        for row in rows:
            car = f"{row['car_make'] or ''} {row['car_model'] or ''}".strip()
            self.archive_tree.insert(
                "", "end", iid=str(row["id"]),
                values=(row["id"], row["order_no"] or "", row["client_name"] or "", car, row["status"] or "", row["due_date"] or "", row["updated_at"] or "")
            )

    def refresh_all_tables(self):
        self.refresh_table()
        self.refresh_archive_table()

    def get_text(self, widget: tk.Text) -> str:
        return widget.get("1.0", "end").strip()

    def set_text(self, widget: tk.Text, text: str):
        widget.delete("1.0", "end")
        widget.insert("1.0", text or "")

    def parse_money(self, value: str) -> float:
        return self.order_service.parse_money(value)

    def calculate_total(self, row) -> float:
        return self.order_service.calculate_total(row)

    def calculate_balance(self, row) -> float:
        return self.order_service.calculate_balance(row)

    def sync_payment_checkbox(self):
        try:
            if self.form_vars["is_paid"].get():
                form_values = {key: var.get() for key, var in self.form_vars.items()}
                self.form_vars["paid_amount"].set(self.order_service.calculate_paid_amount_for_checkbox(form_values))
        except Exception:
            pass

    def form_data(self):
        form_values = {key: var.get() for key, var in self.form_vars.items()}
        text_values = {
            "issue_description": self.get_text(self.issue_text),
            "replaced_parts": self.get_text(self.parts_text),
            "parts_ordered": self.get_text(self.parts_ordered_text),
            "notes": self.get_text(self.notes_text),
        }
        return self.order_service.build_order_data(
            form_values,
            text_values,
            self.order_service.generate_next_order_no(),
        )

    def save_order(self):
        try:
            data = self.form_data()
            result = self.order_service.save_order(self.selected_order_id, data)
            if result == "updated":
                messagebox.showinfo(APP_TITLE, "Zlecenie zostało zaktualizowane.")
            else:
                messagebox.showinfo(APP_TITLE, "Dodano nowe zlecenie.")
            self.refresh_all_tables()
            self.clear_form()
        except ValueError as e:
            messagebox.showerror(APP_TITLE, str(e))
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Nie udało się zapisać danych.\n\n{e}")

    def on_tree_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        order_id = int(selection[0])
        self.load_order_to_form(order_id)

    def load_order_to_form(self, order_id: int):
        row = self.db.fetch_order(order_id)
        if not row:
            return
        self.selected_order_id = order_id
        for key, var in self.form_vars.items():
            if key == "is_paid":
                var.set(int(row[key] or 0))
            else:
                var.set("" if row[key] is None else str(row[key]))
        self.set_text(self.issue_text, row["issue_description"])
        self.set_text(self.parts_text, row["replaced_parts"])
        self.set_text(self.parts_ordered_text, row["parts_ordered"])
        self.set_text(self.notes_text, row["notes"])
        self.notebook.select(self.orders_tab)

    def clear_form(self):
        self.selected_order_id = None
        defaults = self.order_service.default_form_values()
        for key, var in self.form_vars.items():
            var.set(defaults.get(key, ""))
        self.set_text(self.issue_text, "")
        self.set_text(self.parts_text, "")
        self.set_text(self.parts_ordered_text, "")
        self.set_text(self.notes_text, "")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def duplicate_order(self):
        if not self.selected_order_id:
            messagebox.showwarning(APP_TITLE, "Najpierw wybierz zlecenie z tabeli.")
            return
        source = self.db.fetch_order(self.selected_order_id)
        if not source:
            return
        data = self.order_service.duplicate_order_data(source)
        self.db.add_order(data)
        self.refresh_all_tables()
        self.clear_form()
        messagebox.showinfo(APP_TITLE, "Zlecenie zostało zduplikowane jako nowe.")

    def delete_order(self):
        if not self.selected_order_id:
            messagebox.showwarning(APP_TITLE, "Najpierw wybierz zlecenie z tabeli.")
            return
        if not messagebox.askyesno(APP_TITLE, "Na pewno usunąć wybrane zlecenie?"):
            return
        self.order_service.delete_order(self.selected_order_id)
        self.refresh_all_tables()
        self.clear_form()

    def quick_status(self, status: str):
        if not self.selected_order_id:
            messagebox.showwarning(APP_TITLE, "Najpierw wybierz zlecenie z tabeli.")
            return
        self.order_service.update_status(self.selected_order_id, status)
        self.refresh_all_tables()
        row = self.db.fetch_order(self.selected_order_id)
        if row:
            self.form_vars["status"].set(row["status"])

    def archive_order(self):
        if not self.selected_order_id:
            messagebox.showwarning(APP_TITLE, "Najpierw wybierz zlecenie z tabeli.")
            return
        if not messagebox.askyesno(APP_TITLE, "Przenieść zlecenie do archiwum?"):
            return
        self.order_service.archive_order(self.selected_order_id)
        self.refresh_all_tables()
        self.clear_form()

    def restore_archived_order(self):
        selection = self.archive_tree.selection()
        if not selection:
            messagebox.showwarning(APP_TITLE, "Wybierz zlecenie z archiwum.")
            return
        order_id = int(selection[0])
        self.order_service.restore_order(order_id)
        self.refresh_all_tables()
        self.load_order_to_form(order_id)

    def export_csv(self):
        filepath = filedialog.asksaveasfilename(
            title="Zapisz eksport CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"warsztat_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        )
        if not filepath:
            return
        count = self.db.export_csv(filepath)
        messagebox.showinfo(APP_TITLE, f"Wyeksportowano {count} rekordów do pliku CSV.")

    def backup_database(self):
        target = filedialog.asksaveasfilename(
            title="Zapisz kopię bazy danych",
            defaultextension=".db",
            filetypes=[("Baza danych SQLite", "*.db"), ("Wszystkie pliki", "*.*")],
            initialfile=f"warsztat_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db",
        )
        if not target:
            return
        try:
            self.db.conn.commit()
            src = resource_path(DB_NAME)
            with open(src, "rb") as fsrc, open(target, "wb") as fdst:
                fdst.write(fsrc.read())
            messagebox.showinfo(APP_TITLE, "Kopia zapasowa została zapisana.")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Nie udało się wykonać kopii zapasowej.\n\n{e}")

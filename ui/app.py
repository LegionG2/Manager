import json
import os
import tkinter as tk
from dataclasses import replace
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from data.database import Database
from domain.app_section import AppSectionDefinition
from domain.field_definition import FieldDefinition, FieldOption, FieldType
from services.config_service import ConfigService
from services.generic_record_service import GenericRecordService
from services.order_service import OrderService

DEFAULT_APP_TITLE = "Manager"
APP_TITLE = DEFAULT_APP_TITLE
BASE_SECTION_IDS = {"dashboard", "records", "archive", "settings"}
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


def load_main_sections() -> list[AppSectionDefinition]:
    try:
        sections = ConfigService().load_sections()
    except Exception:
        return [
            AppSectionDefinition(id="records", name="Aktywne zlecenia", type="records", visible=True, order=0),
            AppSectionDefinition(id="archive", name="Archiwum", type="archive", visible=True, order=1),
        ]

    visible_sections = [section for section in sections if section.visible]
    visible_sections.sort(key=lambda section: section.order)
    return visible_sections or [
        AppSectionDefinition(id="records", name="Aktywne zlecenia", type="records", visible=True, order=0),
        AppSectionDefinition(id="archive", name="Archiwum", type="archive", visible=True, order=1),
    ]


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
        self.generic_record_service = GenericRecordService(self.db)
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
        self.header_title_label = ttk.Label(top, text=self.app_title, style="Title.TLabel")
        self.header_title_label.grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="⚙", command=self.show_settings_preview).grid(row=0, column=2, sticky="e", padx=(8, 6))
        ttk.Checkbutton(top, text="Tryb ciemny", variable=self.theme_var, command=self.toggle_theme).grid(row=0, column=3, sticky="e")

        self.summary_labels = {}
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.orders_tab = ttk.Frame(self.notebook)
        self.archive_tab = ttk.Frame(self.notebook)
        self.placeholder_tabs = {}
        self.section_tab_frames = {}
        self.custom_record_refreshers = {}
        self.refresh_configured_tabs()

        self.build_orders_tab()
        self.build_archive_tab()

    def refresh_configured_tabs(self):
        selected_section_id = None
        try:
            selected_tab = self.notebook.select()
            for section_id, frame in self.section_tab_frames.items():
                if str(frame) == selected_tab:
                    selected_section_id = section_id
                    break
        except tk.TclError:
            selected_section_id = None

        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)
        for frame in self.placeholder_tabs.values():
            frame.destroy()

        self.placeholder_tabs = {}
        self.section_tab_frames = {}
        self.custom_record_refreshers = {}
        self.config_sections = load_main_sections()
        section_frames = {
            "records": self.orders_tab,
            "archive": self.archive_tab,
        }

        for section in self.config_sections:
            frame = section_frames.get(section.type)
            if frame is None:
                frame = ttk.Frame(self.notebook)
                self.build_section_tab(frame, section)
                self.placeholder_tabs[section.id] = frame
            self.notebook.add(frame, text=section.name)
            self.section_tab_frames[section.id] = frame

        if selected_section_id in self.section_tab_frames:
            self.notebook.select(self.section_tab_frames[selected_section_id])

    def build_section_tab(self, parent, section: AppSectionDefinition):
        if section.type == "dashboard":
            self.build_dashboard_tab(parent, section.name)
            return
        if section.type == "settings":
            self.build_settings_section_tab(parent, section.name)
            return
        if section.type == "custom":
            self.build_custom_section_tab(parent, section)
            return
        self.build_placeholder_tab(parent, section.name, "Sekcja w przygotowaniu.")

    def build_dashboard_tab(self, parent, title: str):
        wrapper = ttk.Frame(parent, padding=16)
        wrapper.pack(fill="both", expand=True)
        ttk.Label(wrapper, text=title, style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(wrapper, text="Dashboard w przygotowaniu.", style="Sub.TLabel").pack(anchor="w")

    def build_settings_section_tab(self, parent, title: str):
        wrapper = ttk.Frame(parent, padding=16)
        wrapper.pack(fill="both", expand=True)
        ttk.Label(wrapper, text=title, style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(wrapper, text="Ustawienia aplikacji są dostępne w osobnym oknie.", style="Sub.TLabel").pack(anchor="w", pady=(0, 12))
        ttk.Button(wrapper, text="Otwórz ustawienia", command=self.show_settings_preview).pack(anchor="w")

    def build_placeholder_tab(self, parent, title: str, message: str):
        wrapper = ttk.Frame(parent, padding=16)
        wrapper.pack(fill="both", expand=True)
        ttk.Label(wrapper, text=title, style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(wrapper, text=message, style="Sub.TLabel").pack(anchor="w")

    def build_custom_section_tab(self, parent, section: AppSectionDefinition):
        field_definitions = self.load_custom_field_definitions()
        wrapper = ttk.Frame(parent, padding=16)
        wrapper.pack(fill="both", expand=True)
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(3, weight=1)

        ttk.Label(wrapper, text=section.name, style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))

        form = ttk.Frame(wrapper)
        form.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        form.columnconfigure(1, weight=1)
        field_widgets = {}
        for row_index, field_definition in enumerate(field_definitions):
            ttk.Label(form, text=field_definition.label, style="Panel.TLabel").grid(
                row=row_index,
                column=0,
                sticky="w",
                padx=(0, 8),
                pady=3,
            )
            field_widgets[field_definition.name] = self.build_custom_field_widget(form, row_index, field_definition)

        list_label = ttk.Label(wrapper, text="Rekordy", style="Panel.TLabel")
        list_label.grid(row=2, column=0, sticky="w", pady=(0, 4))

        table_wrap = ttk.Frame(wrapper)
        table_wrap.grid(row=3, column=0, sticky="nsew")
        table_wrap.rowconfigure(0, weight=1)
        table_wrap.columnconfigure(0, weight=1)

        columns = ("id", *[field_definition.name for field_definition in field_definitions], "created_at")
        tree = ttk.Treeview(table_wrap, columns=columns, show="headings", selectmode="browse")
        headings = {"id": "ID", "created_at": "Dodano"}
        headings.update({field_definition.name: field_definition.label for field_definition in field_definitions})
        widths = {"id": 60, "created_at": 160}
        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(column, width=widths.get(column, 180), minwidth=50, anchor="w")
        tree.column("id", anchor="center")
        tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        def refresh_custom_records():
            for item in tree.get_children():
                tree.delete(item)
            rows = self.generic_record_service.list_records(section.id, archived=0)
            for row in rows:
                data = self.generic_record_service.decode_data(row)
                tree.insert(
                    "",
                    "end",
                    values=(row["id"], *self.format_custom_record_values(field_definitions, data), row["created_at"] or ""),
                )

        def add_custom_record():
            data = {}
            for field_definition in field_definitions:
                try:
                    value = self.read_custom_field_value(field_definition, field_widgets[field_definition.name])
                except ValueError as exc:
                    messagebox.showerror(section.name, str(exc))
                    return
                data[field_definition.name] = value
            try:
                self.generic_record_service.create_record(
                    section_id=section.id,
                    record_type_id=section.record_type_id,
                    data=data,
                )
            except Exception as exc:
                messagebox.showerror(section.name, f"Nie udało się dodać rekordu.\n\n{exc}")
                return
            for field_definition in field_definitions:
                self.reset_custom_field_value(field_definition, field_widgets[field_definition.name])
            refresh_custom_records()

        ttk.Button(form, text="Dodaj rekord", command=add_custom_record).grid(
            row=len(field_definitions),
            column=1,
            sticky="w",
            pady=(6, 0),
        )
        self.custom_record_refreshers[section.id] = refresh_custom_records
        refresh_custom_records()

    def load_custom_field_definitions(self) -> list[FieldDefinition]:
        try:
            fields = ConfigService().load_field_definitions()
        except Exception:
            return [
                FieldDefinition(name="title", label="Title", field_type=FieldType.TEXT, required=True, default=""),
                FieldDefinition(name="description", label="Description", field_type=FieldType.TEXT, required=False, default=""),
            ]
        return fields or [
            FieldDefinition(name="title", label="Title", field_type=FieldType.TEXT, required=True, default=""),
        ]

    def build_custom_field_widget(self, parent, row_index: int, field_definition: FieldDefinition):
        field_type = field_definition.field_type
        if field_type == FieldType.BOOLEAN:
            variable = tk.BooleanVar(value=bool(field_definition.default))
            widget = ttk.Checkbutton(parent, variable=variable)
            widget.grid(row=row_index, column=1, sticky="w", pady=3)
            return {"widget": widget, "variable": variable}

        if field_type == FieldType.SELECT:
            options_by_label = {option.label: option.value for option in field_definition.options}
            default_label = next(
                (option.label for option in field_definition.options if option.value == field_definition.default),
                field_definition.options[0].label if field_definition.options else "",
            )
            variable = tk.StringVar(value=default_label)
            widget = ttk.Combobox(parent, textvariable=variable, values=list(options_by_label.keys()), state="readonly")
            widget.grid(row=row_index, column=1, sticky="ew", pady=3)
            self.bind_tab_navigation(widget)
            return {"widget": widget, "variable": variable, "options_by_label": options_by_label}

        variable = tk.StringVar(value="" if field_definition.default is None else str(field_definition.default))
        widget = ttk.Entry(parent, textvariable=variable)
        widget.grid(row=row_index, column=1, sticky="ew", pady=3)
        self.bind_tab_navigation(widget)
        return {"widget": widget, "variable": variable}

    def read_custom_field_value(self, field_definition: FieldDefinition, field_widget: dict):
        field_type = field_definition.field_type
        variable = field_widget["variable"]
        if field_type == FieldType.BOOLEAN:
            return bool(variable.get())

        raw_value = variable.get().strip()
        if field_definition.required and not raw_value:
            raise ValueError(f"Pole \"{field_definition.label}\" jest wymagane.")

        if field_type == FieldType.NUMBER:
            if not raw_value:
                return None
            try:
                return float(raw_value.replace(",", "."))
            except ValueError:
                raise ValueError(f"Pole \"{field_definition.label}\" musi być liczbą.")

        if field_type == FieldType.SELECT:
            options_by_label = field_widget.get("options_by_label", {})
            return options_by_label.get(raw_value, raw_value)

        return raw_value

    def reset_custom_field_value(self, field_definition: FieldDefinition, field_widget: dict):
        variable = field_widget["variable"]
        if field_definition.field_type == FieldType.BOOLEAN:
            variable.set(bool(field_definition.default))
        elif field_definition.field_type == FieldType.SELECT:
            options_by_label = field_widget.get("options_by_label", {})
            default_label = next(
                (label for label, value in options_by_label.items() if value == field_definition.default),
                next(iter(options_by_label), ""),
            )
            variable.set(default_label)
        else:
            variable.set("" if field_definition.default is None else str(field_definition.default))

    def format_custom_record_values(self, field_definitions: list[FieldDefinition], data: dict) -> list[str]:
        values = []
        for field_definition in field_definitions:
            value = data.get(field_definition.name, "")
            if field_definition.field_type == FieldType.BOOLEAN:
                values.append("Tak" if value else "Nie")
            elif field_definition.field_type == FieldType.SELECT:
                label_by_value = {option.value: option.label for option in field_definition.options}
                values.append(label_by_value.get(str(value), "" if value is None else str(value)))
            else:
                values.append("" if value is None else str(value))
        return values

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
                ", ".join(option.label for option in field.options),
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
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text="Ustawienia", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        general_frame = ttk.LabelFrame(container, text="Ogólne", style="Group.TLabelframe", padding=8)
        general_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        general_frame.columnconfigure(1, weight=1)

        ttk.Label(general_frame, text="Nazwa aplikacji:", style="TLabel").grid(row=0, column=0, sticky="w", padx=(0, 16), pady=3)
        app_name_var = tk.StringVar(value=values.get("Nazwa aplikacji", DEFAULT_APP_TITLE))
        app_name_entry = ttk.Entry(general_frame, textvariable=app_name_var, width=30)
        app_name_entry.grid(row=0, column=1, sticky="ew", pady=3)

        details = [
            ("Aktywny typ rekordu", values.get("Aktywny typ rekordu", "Brak danych")),
            ("Liczba sekcji/kart", values.get("Liczba sekcji/kart", "Brak danych")),
        ]
        for index, (label, value) in enumerate(details, start=1):
            ttk.Label(general_frame, text=f"{label}:", style="TLabel").grid(row=index, column=0, sticky="w", padx=(0, 16), pady=3)
            ttk.Label(general_frame, text=value, style="TLabel").grid(row=index, column=1, sticky="w", pady=3)

        note = "Na tym etapie edytowana jest tylko nazwa aplikacji. Karty, typy rekordow i pola zostana dodane pozniej."
        if error:
            note = f"Nie udalo sie zaladowac konfiguracji. Pokazano fallback.\n{error}"
        ttk.Label(general_frame, text=note, style="Sub.TLabel", wraplength=460, justify="left").grid(
            row=len(details) + 1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(10, 0),
        )

        sections_frame = ttk.LabelFrame(container, text="Sekcje aplikacji", style="Group.TLabelframe", padding=8)
        sections_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for column, weight in [(0, 1), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]:
            sections_frame.columnconfigure(column, weight=weight)
        for column, heading in enumerate(["Nazwa", "ID", "Typ", "Widoczna", "Kolejnosc", ""]):
            ttk.Label(sections_frame, text=heading, style="Panel.TLabel").grid(row=0, column=column, sticky="w", padx=(0, 8), pady=(0, 4))
        section_editors = []
        if sections:
            for row_index, (name, section_id, section_type, visible, order) in enumerate(sections, start=1):
                name_var = tk.StringVar(value=name)
                visible_var = tk.BooleanVar(value=visible == "Tak")
                order_var = tk.StringVar(value=order)
                ttk.Entry(sections_frame, textvariable=name_var, width=18).grid(row=row_index, column=0, sticky="ew", padx=(0, 8), pady=2)
                ttk.Label(sections_frame, text=section_id, style="TLabel").grid(row=row_index, column=1, sticky="w", padx=(0, 8), pady=2)
                ttk.Label(sections_frame, text=section_type, style="TLabel").grid(row=row_index, column=2, sticky="w", padx=(0, 8), pady=2)
                ttk.Checkbutton(sections_frame, variable=visible_var).grid(row=row_index, column=3, sticky="w", padx=(0, 8), pady=2)
                ttk.Entry(sections_frame, textvariable=order_var, width=8).grid(row=row_index, column=4, sticky="w", pady=2)
                delete_button = ttk.Button(
                    sections_frame,
                    text="Usuń",
                    command=lambda section_id=section_id, name=name: self.delete_section_settings(section_id, name, window),
                )
                delete_button.grid(row=row_index, column=5, sticky="w", padx=(8, 0), pady=2)
                if section_id in BASE_SECTION_IDS:
                    delete_button.configure(state="disabled")
                section_editors.append({
                    "id": section_id,
                    "name_var": name_var,
                    "visible_var": visible_var,
                    "order_var": order_var,
                })
        else:
            ttk.Label(sections_frame, text="Brak danych", style="TLabel").grid(row=1, column=0, columnspan=5, sticky="w", pady=2)
        add_row = len(sections) + 1 if sections else 2
        next_order = add_row
        for _name, _section_id, _section_type, _visible, order in sections:
            try:
                next_order = max(next_order, int(order) + 1)
            except ValueError:
                pass
        new_section_vars = {
            "id_var": tk.StringVar(),
            "name_var": tk.StringVar(),
            "type_var": tk.StringVar(value="custom"),
            "visible_var": tk.BooleanVar(value=True),
            "order_var": tk.StringVar(value=str(next_order)),
        }
        ttk.Entry(sections_frame, textvariable=new_section_vars["name_var"], width=18).grid(row=add_row, column=0, sticky="ew", padx=(0, 8), pady=(8, 2))
        ttk.Entry(sections_frame, textvariable=new_section_vars["id_var"], width=14).grid(row=add_row, column=1, sticky="w", padx=(0, 8), pady=(8, 2))
        ttk.Entry(sections_frame, textvariable=new_section_vars["type_var"], width=12).grid(row=add_row, column=2, sticky="w", padx=(0, 8), pady=(8, 2))
        ttk.Checkbutton(sections_frame, variable=new_section_vars["visible_var"]).grid(row=add_row, column=3, sticky="w", padx=(0, 8), pady=(8, 2))
        ttk.Entry(sections_frame, textvariable=new_section_vars["order_var"], width=8).grid(row=add_row, column=4, sticky="w", pady=(8, 2))
        ttk.Button(
            sections_frame,
            text="Dodaj sekcje",
            command=lambda: self.add_section_settings(new_section_vars, window),
        ).grid(row=add_row, column=5, sticky="w", padx=(8, 0), pady=(8, 2))
        ttk.Button(
            sections_frame,
            text="Zapisz sekcje",
            command=lambda: self.save_sections_settings(section_editors, window),
        ).grid(row=add_row + 1, column=0, sticky="w", pady=(8, 0))

        record_type_frame = ttk.LabelFrame(container, text="Typ rekordu", style="Group.TLabelframe", padding=8)
        record_type_frame.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        record_type_frame.columnconfigure(1, weight=1)
        for index, (label, value) in enumerate(record_type):
            ttk.Label(record_type_frame, text=f"{label}:", style="TLabel").grid(row=index, column=0, sticky="w", padx=(0, 16), pady=3)
            ttk.Label(record_type_frame, text=value, style="TLabel", wraplength=460).grid(row=index, column=1, sticky="w", pady=3)

        fields_frame = ttk.LabelFrame(container, text="Pola", style="Group.TLabelframe", padding=8)
        fields_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        for column, weight in [(0, 0), (1, 1), (2, 0), (3, 0), (4, 1)]:
            fields_frame.columnconfigure(column, weight=weight)
        for column, heading in enumerate(["ID", "Etykieta", "Typ", "Wymagane", "Opcje select"]):
            ttk.Label(fields_frame, text=heading, style="Panel.TLabel").grid(row=0, column=column, sticky="w", padx=(0, 8), pady=(0, 4))
        field_editors = []
        field_type_values = [field_type.value for field_type in FieldType]
        if fields:
            for row_index, (field_id, label, field_type, required, options) in enumerate(fields, start=1):
                label_var = tk.StringVar(value=label)
                type_var = tk.StringVar(value=field_type)
                required_var = tk.BooleanVar(value=required == "Tak")
                options_var = tk.StringVar(value=options)
                ttk.Label(fields_frame, text=field_id, style="TLabel").grid(row=row_index, column=0, sticky="w", padx=(0, 8), pady=2)
                ttk.Entry(fields_frame, textvariable=label_var, width=20).grid(row=row_index, column=1, sticky="ew", padx=(0, 8), pady=2)
                ttk.Combobox(fields_frame, textvariable=type_var, values=field_type_values, state="readonly", width=10).grid(row=row_index, column=2, sticky="w", padx=(0, 8), pady=2)
                ttk.Checkbutton(fields_frame, variable=required_var).grid(row=row_index, column=3, sticky="w", padx=(0, 8), pady=2)
                ttk.Entry(fields_frame, textvariable=options_var, width=24).grid(row=row_index, column=4, sticky="ew", pady=2)
                field_editors.append({
                    "id": field_id,
                    "label_var": label_var,
                    "type_var": type_var,
                    "required_var": required_var,
                    "options_var": options_var,
                })
        else:
            ttk.Label(fields_frame, text="Brak danych", style="TLabel").grid(row=1, column=0, columnspan=5, sticky="w", pady=2)

        add_field_row = len(fields) + 1 if fields else 2
        new_field_vars = {
            "id_var": tk.StringVar(),
            "label_var": tk.StringVar(),
            "type_var": tk.StringVar(value=FieldType.TEXT.value),
            "required_var": tk.BooleanVar(value=False),
            "options_var": tk.StringVar(),
        }
        ttk.Entry(fields_frame, textvariable=new_field_vars["id_var"], width=14).grid(row=add_field_row, column=0, sticky="w", padx=(0, 8), pady=(8, 2))
        ttk.Entry(fields_frame, textvariable=new_field_vars["label_var"], width=20).grid(row=add_field_row, column=1, sticky="ew", padx=(0, 8), pady=(8, 2))
        ttk.Combobox(fields_frame, textvariable=new_field_vars["type_var"], values=field_type_values, state="readonly", width=10).grid(row=add_field_row, column=2, sticky="w", padx=(0, 8), pady=(8, 2))
        ttk.Checkbutton(fields_frame, variable=new_field_vars["required_var"]).grid(row=add_field_row, column=3, sticky="w", padx=(0, 8), pady=(8, 2))
        ttk.Entry(fields_frame, textvariable=new_field_vars["options_var"], width=24).grid(row=add_field_row, column=4, sticky="ew", pady=(8, 2))
        ttk.Button(
            fields_frame,
            text="Dodaj pole",
            command=lambda: self.add_field_settings(new_field_vars, window),
        ).grid(row=add_field_row + 1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(
            fields_frame,
            text="Zapisz pola",
            command=lambda: self.save_field_settings(field_editors, window),
        ).grid(row=add_field_row + 1, column=1, sticky="w", pady=(8, 0))

        buttons = ttk.Frame(container)
        buttons.grid(row=5, column=0, sticky="ew")
        buttons.columnconfigure(1, weight=1)
        ttk.Button(
            buttons,
            text="Zapisz",
            style="Primary.TButton",
            command=lambda: self.save_app_name(app_name_var.get(), window),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(buttons, text="Zamknij", command=window.destroy).grid(row=0, column=1, sticky="e")

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
        self.header_title_label.configure(text=self.app_title)
        messagebox.showinfo("Ustawienia", "Nazwa aplikacji zostala zapisana.")
        if window is not None:
            window.destroy()
        return True

    def save_sections_settings(self, section_editors, window: tk.Toplevel | None = None) -> bool:
        if not section_editors:
            messagebox.showerror("Ustawienia", "Brak sekcji do zapisania.")
            return False

        edited_sections = {}
        for editor in section_editors:
            name = editor["name_var"].get().strip()
            if not name:
                messagebox.showerror("Ustawienia", "Nazwa sekcji nie moze byc pusta.")
                return False
            try:
                order = int(editor["order_var"].get().strip())
            except ValueError:
                messagebox.showerror("Ustawienia", "Kolejnosc sekcji musi byc liczba calkowita.")
                return False
            edited_sections[editor["id"]] = {
                "name": name,
                "visible": bool(editor["visible_var"].get()),
                "order": order,
            }

        config_service = ConfigService()
        try:
            config = config_service.load_all()
            updated_sections = [
                replace(
                    section,
                    name=edited_sections[section.id]["name"],
                    visible=edited_sections[section.id]["visible"],
                    order=edited_sections[section.id]["order"],
                )
                if section.id in edited_sections
                else section
                for section in config.sections
            ]
            updated_config = replace(config, sections=updated_sections)
            validation = config_service.validate_all(updated_config)
            if not validation.is_valid:
                messagebox.showerror("Ustawienia", "\n".join(validation.errors))
                return False
            config_service.save_sections(updated_sections)
        except Exception as exc:
            messagebox.showerror("Ustawienia", f"Nie udalo sie zapisac sekcji.\n\n{exc}")
            return False

        self.refresh_configured_tabs()
        messagebox.showinfo("Ustawienia", "Sekcje zostaly zapisane.")
        if window is not None:
            window.destroy()
            self.show_settings_preview()
        return True

    def save_field_settings(self, field_editors, window: tk.Toplevel | None = None) -> bool:
        if not field_editors:
            messagebox.showerror("Ustawienia", "Brak pól do zapisania.")
            return False

        updated_fields = []
        for editor in field_editors:
            label = editor["label_var"].get().strip()
            field_type = editor["type_var"].get().strip()
            if not label:
                messagebox.showerror("Ustawienia", "Etykieta pola nie może być pusta.")
                return False
            try:
                updated_fields.append(
                    FieldDefinition(
                        name=editor["id"],
                        label=label,
                        field_type=FieldType(field_type),
                        required=bool(editor["required_var"].get()),
                        default="",
                        options=self.parse_field_options(editor["options_var"].get()),
                    )
                )
            except ValueError as exc:
                messagebox.showerror("Ustawienia", str(exc))
                return False

        return self.save_field_definitions(updated_fields, window, "Pola zostały zapisane.")

    def add_field_settings(self, new_field_vars, window: tk.Toplevel | None = None) -> bool:
        field_id = new_field_vars["id_var"].get().strip()
        label = new_field_vars["label_var"].get().strip()
        field_type = new_field_vars["type_var"].get().strip()
        if not field_id:
            messagebox.showerror("Ustawienia", "ID pola nie może być puste.")
            return False
        if not label:
            messagebox.showerror("Ustawienia", "Etykieta pola nie może być pusta.")
            return False

        config_service = ConfigService()
        try:
            config = config_service.load_all()
            if any(field.name == field_id for field in config.field_definitions):
                messagebox.showerror("Ustawienia", "Pole o takim ID już istnieje.")
                return False
            new_field = FieldDefinition(
                name=field_id,
                label=label,
                field_type=FieldType(field_type),
                required=bool(new_field_vars["required_var"].get()),
                default="",
                options=self.parse_field_options(new_field_vars["options_var"].get()),
            )
            updated_fields = [*config.field_definitions, new_field]
        except ValueError as exc:
            messagebox.showerror("Ustawienia", str(exc))
            return False
        except Exception as exc:
            messagebox.showerror("Ustawienia", f"Nie udało się dodać pola.\n\n{exc}")
            return False

        return self.save_field_definitions(updated_fields, window, "Pole zostało dodane.")

    def save_field_definitions(self, field_definitions: list[FieldDefinition], window: tk.Toplevel | None, success_message: str) -> bool:
        config_service = ConfigService()
        try:
            config = config_service.load_all()
            updated_config = replace(config, field_definitions=field_definitions)
            validation = config_service.validate_all(updated_config)
            if not validation.is_valid:
                messagebox.showerror("Ustawienia", "\n".join(validation.errors))
                return False
            config_service.save_field_definitions(field_definitions)
        except Exception as exc:
            messagebox.showerror("Ustawienia", f"Nie udało się zapisać pól.\n\n{exc}")
            return False

        self.refresh_configured_tabs()
        messagebox.showinfo("Ustawienia", success_message)
        if window is not None:
            window.destroy()
            self.show_settings_preview()
        return True

    def parse_field_options(self, raw_options: str) -> list[FieldOption]:
        options = []
        seen_values = set()
        for raw_option in raw_options.split(","):
            label = raw_option.strip()
            if not label:
                continue
            value = self.option_value_from_label(label)
            if value in seen_values:
                continue
            seen_values.add(value)
            options.append(FieldOption(value=value, label=label))
        return options

    def option_value_from_label(self, label: str) -> str:
        value = label.strip().lower().replace(" ", "_")
        value = "".join(character for character in value if character.isalnum() or character == "_")
        return value or "option"

    def add_section_settings(self, new_section_vars, window: tk.Toplevel | None = None) -> bool:
        section_id = new_section_vars["id_var"].get().strip()
        name = new_section_vars["name_var"].get().strip()
        section_type = new_section_vars["type_var"].get().strip()
        if not section_id:
            messagebox.showerror("Ustawienia", "ID sekcji nie moze byc puste.")
            return False
        if not name:
            messagebox.showerror("Ustawienia", "Nazwa sekcji nie moze byc pusta.")
            return False
        if not section_type:
            messagebox.showerror("Ustawienia", "Typ sekcji nie moze byc pusty.")
            return False
        try:
            order = int(new_section_vars["order_var"].get().strip())
        except ValueError:
            messagebox.showerror("Ustawienia", "Kolejnosc sekcji musi byc liczba calkowita.")
            return False

        config_service = ConfigService()
        try:
            config = config_service.load_all()
            if any(section.id == section_id for section in config.sections):
                messagebox.showerror("Ustawienia", "Sekcja o takim ID juz istnieje.")
                return False
            updated_sections = config.sections + [
                AppSectionDefinition(
                    id=section_id,
                    name=name,
                    type=section_type,
                    visible=bool(new_section_vars["visible_var"].get()),
                    order=order,
                )
            ]
            updated_config = replace(config, sections=updated_sections)
            validation = config_service.validate_all(updated_config)
            if not validation.is_valid:
                messagebox.showerror("Ustawienia", "\n".join(validation.errors))
                return False
            config_service.save_sections(updated_sections)
        except Exception as exc:
            messagebox.showerror("Ustawienia", f"Nie udalo sie dodac sekcji.\n\n{exc}")
            return False

        self.refresh_configured_tabs()
        messagebox.showinfo("Ustawienia", "Sekcja zostala dodana.")
        if window is not None:
            window.destroy()
            self.show_settings_preview()
        return True

    def delete_section_settings(self, section_id: str, section_name: str, window: tk.Toplevel | None = None) -> bool:
        if section_id in BASE_SECTION_IDS:
            messagebox.showinfo("Ustawienia", "Sekcje bazowe nie moga byc usuwane.")
            return False
        if not messagebox.askyesno("Ustawienia", f"Usunac sekcje \"{section_name}\"?"):
            return False

        config_service = ConfigService()
        try:
            config = config_service.load_all()
            updated_sections = [section for section in config.sections if section.id != section_id]
            if len(updated_sections) == len(config.sections):
                messagebox.showerror("Ustawienia", "Nie znaleziono sekcji do usuniecia.")
                return False
            updated_config = replace(config, sections=updated_sections)
            validation = config_service.validate_all(updated_config)
            if not validation.is_valid:
                messagebox.showerror("Ustawienia", "\n".join(validation.errors))
                return False
            config_service.save_sections(updated_sections)
        except Exception as exc:
            messagebox.showerror("Ustawienia", f"Nie udalo sie usunac sekcji.\n\n{exc}")
            return False

        self.refresh_configured_tabs()
        messagebox.showinfo("Ustawienia", "Sekcja zostala usunieta.")
        if window is not None:
            window.destroy()
            self.show_settings_preview()
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
        if not self.summary_labels:
            return
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
            label = self.summary_labels.get(key)
            if label is not None:
                label.configure(text=text)

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
        for refresh_custom_records in self.custom_record_refreshers.values():
            refresh_custom_records()

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

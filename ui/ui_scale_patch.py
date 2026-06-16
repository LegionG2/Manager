import tkinter as tk
from tkinter import ttk, messagebox


UI_SIZE_OPTIONS = {
    "Mały": {
        "tk_scaling": 0.95,
        "base_font": 9,
        "title_font": 14,
        "tree_row_height": 24,
        "button_padding": (6, 4),
        "entry_padding": 2,
    },
    "Normalny": {
        "tk_scaling": 1.0,
        "base_font": 10,
        "title_font": 16,
        "tree_row_height": 28,
        "button_padding": (8, 5),
        "entry_padding": 3,
    },
    "Duży": {
        "tk_scaling": 1.1,
        "base_font": 11,
        "title_font": 18,
        "tree_row_height": 32,
        "button_padding": (10, 6),
        "entry_padding": 4,
    },
    "Bardzo duży": {
        "tk_scaling": 1.2,
        "base_font": 12,
        "title_font": 20,
        "tree_row_height": 36,
        "button_padding": (12, 7),
        "entry_padding": 5,
    },
}

DEFAULT_UI_SIZE = "Normalny"


def install_ui_scale_patch(app_class):
    """Adds user-configurable UI size without touching the current data model."""

    original_configure_style = app_class.configure_style
    original_repaint_widgets = app_class.repaint_widgets
    original_configure_tree_tags = app_class.configure_tree_tags
    original_show_settings_preview = app_class.show_settings_preview

    def get_ui_size_key(self) -> str:
        settings_mgr = getattr(self, "settings_mgr", None)
        current = getattr(self, "current_ui_size", None)
        if not current and settings_mgr is not None:
            current = settings_mgr.get("ui_size", DEFAULT_UI_SIZE)
        if current not in UI_SIZE_OPTIONS:
            current = DEFAULT_UI_SIZE
        return current

    def get_ui_size_config(self) -> dict:
        return UI_SIZE_OPTIONS[get_ui_size_key(self)]

    def font_tuple(self, delta: int = 0, bold: bool = False):
        config = get_ui_size_config(self)
        weight = "bold" if bold else "normal"
        return ("Tahoma", max(8, int(config["base_font"]) + delta), weight)

    def apply_ui_size(self, size_key: str, save: bool = True, refresh: bool = True):
        if size_key not in UI_SIZE_OPTIONS:
            size_key = DEFAULT_UI_SIZE
        self.current_ui_size = size_key
        config = UI_SIZE_OPTIONS[size_key]
        try:
            self.tk.call("tk", "scaling", float(config["tk_scaling"]))
        except Exception:
            pass

        if save and hasattr(self, "settings_mgr"):
            self.settings_mgr.set("ui_size", size_key)

        self.configure_style()
        self.repaint_widgets(self)
        try:
            self.configure_tree_tags()
        except Exception:
            pass
        if refresh:
            try:
                self.refresh_all_tables()
            except Exception:
                pass
        self.update_idletasks()

    def configure_style(self):
        original_configure_style(self)
        c = self.colors
        config = get_ui_size_config(self)
        base_font = font_tuple(self)
        bold_font = font_tuple(self, bold=True)
        title_font = ("Tahoma", int(config["title_font"]), "bold")
        sub_font = font_tuple(self, -1)
        button_padding = config["button_padding"]
        entry_padding = config["entry_padding"]

        self.option_add("*Font", base_font)
        self.option_add("*TCombobox*Listbox.font", base_font)

        self.style.configure("Group.TLabelframe.Label", font=bold_font)
        self.style.configure("TLabel", font=base_font)
        self.style.configure("Panel.TLabel", font=base_font)
        self.style.configure("Summary.TLabel", font=bold_font)
        self.style.configure("Title.TLabel", font=title_font)
        self.style.configure("Sub.TLabel", font=sub_font)
        self.style.configure("TButton", font=base_font, padding=button_padding)
        self.style.configure("Primary.TButton", font=bold_font, padding=button_padding)
        self.style.configure("Danger.TButton", font=bold_font, padding=button_padding)
        self.style.configure("TCheckbutton", font=base_font)
        self.style.configure("TNotebook.Tab", font=bold_font, padding=(12, 6))
        self.style.configure(
            "Treeview",
            font=base_font,
            rowheight=int(config["tree_row_height"]),
            background=c["tree_bg"],
            fieldbackground=c["tree_bg"],
            foreground=c["text"],
        )
        self.style.configure("Treeview.Heading", font=bold_font)
        self.style.configure("TEntry", font=base_font, padding=entry_padding)
        self.style.configure("TCombobox", font=base_font, padding=entry_padding)

    def repaint_widgets(self, widget):
        original_repaint_widgets(self, widget)
        c = self.colors
        base_font = font_tuple(self)
        if isinstance(widget, tk.Text):
            widget.configure(
                font=base_font,
                bg=c["entry_bg"],
                fg=c["text"],
                insertbackground=c["text"],
            )
        elif isinstance(widget, tk.Listbox):
            widget.configure(font=base_font, bg=c["entry_bg"], fg=c["text"])

    def configure_tree_tags(self):
        original_configure_tree_tags(self)
        if not hasattr(self, "tree"):
            return
        bold_font = font_tuple(self, bold=True)
        try:
            self.tree.tag_configure("prio_pilne", font=bold_font)
            self.tree.tag_configure("due_overdue", font=bold_font)
        except Exception:
            pass

    def add_appearance_controls(self, window: tk.Toplevel):
        containers = [child for child in window.winfo_children() if isinstance(child, ttk.Frame)]
        if not containers:
            return
        container = containers[0]

        for child in container.grid_slaves():
            grid_info = child.grid_info()
            row = int(grid_info.get("row", 0))
            if row >= 5:
                child.grid_configure(row=row + 1)

        appearance_frame = ttk.LabelFrame(container, text="Wygląd", style="Group.TLabelframe", padding=8)
        appearance_frame.grid(row=5, column=0, sticky="ew", pady=(0, 8))
        appearance_frame.columnconfigure(1, weight=1)

        ttk.Label(appearance_frame, text="Rozmiar interfejsu:", style="TLabel").grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 16),
            pady=3,
        )
        ui_size_var = tk.StringVar(value=get_ui_size_key(self))
        ui_size_combo = ttk.Combobox(
            appearance_frame,
            textvariable=ui_size_var,
            values=list(UI_SIZE_OPTIONS.keys()),
            state="readonly",
            width=16,
        )
        ui_size_combo.grid(row=0, column=1, sticky="w", pady=3)

        ttk.Label(
            appearance_frame,
            text="Zmiana powiększa czcionkę, przyciski, pola formularzy i wiersze tabel. Ustawienie zapisuje się dla tego użytkownika.",
            style="Sub.TLabel",
            wraplength=560,
            justify="left",
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(6, 8))

        def save_appearance():
            apply_ui_size(self, ui_size_var.get(), save=True, refresh=True)
            messagebox.showinfo("Ustawienia", "Rozmiar interfejsu został zapisany.")

        ttk.Button(
            appearance_frame,
            text="Zastosuj wygląd",
            style="Primary.TButton",
            command=save_appearance,
        ).grid(row=0, column=2, sticky="e", padx=(12, 0), pady=3)

        window.update_idletasks()
        try:
            x = self.winfo_rootx() + max((self.winfo_width() - window.winfo_width()) // 2, 0)
            y = self.winfo_rooty() + max((self.winfo_height() - window.winfo_height()) // 2, 0)
            window.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def show_settings_preview(self, *args, **kwargs):
        before_windows = set(self.winfo_children())
        result = original_show_settings_preview(self, *args, **kwargs)
        after_windows = [
            child
            for child in self.winfo_children()
            if child not in before_windows and isinstance(child, tk.Toplevel)
        ]
        if after_windows:
            try:
                add_appearance_controls(self, after_windows[-1])
            except Exception:
                pass
        return result

    app_class.get_ui_size_key = get_ui_size_key
    app_class.get_ui_size_config = get_ui_size_config
    app_class.ui_font = font_tuple
    app_class.apply_ui_size = apply_ui_size
    app_class.configure_style = configure_style
    app_class.repaint_widgets = repaint_widgets
    app_class.configure_tree_tags = configure_tree_tags
    app_class.show_settings_preview = show_settings_preview

import re
import tkinter as tk


GEOMETRY_PATTERN = re.compile(r"^(\d+)x(\d+)([+-]\d+)([+-]\d+)$")
DEFAULT_SAVE_DELAY_MS = 500
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 560


def enable_window_state_settings(app_class):
    """Persists the main window size and placement in the local user settings."""

    original_init = app_class.__init__

    def is_valid_geometry(geometry: str | None) -> bool:
        if not isinstance(geometry, str):
            return False
        match = GEOMETRY_PATTERN.match(geometry.strip())
        if not match:
            return False
        width = int(match.group(1))
        height = int(match.group(2))
        return width >= MIN_WINDOW_WIDTH and height >= MIN_WINDOW_HEIGHT

    def restore_window_state(self):
        settings_mgr = getattr(self, "settings_mgr", None)
        if settings_mgr is None:
            return
        geometry = settings_mgr.get("window_geometry")
        if is_valid_geometry(geometry):
            try:
                self.geometry(geometry)
            except tk.TclError:
                pass
        window_state = settings_mgr.get("window_state", "normal")
        if window_state == "zoomed":
            try:
                self.after(100, lambda: self.state("zoomed"))
            except tk.TclError:
                pass

    def save_window_state(self):
        settings_mgr = getattr(self, "settings_mgr", None)
        if settings_mgr is None:
            return
        try:
            window_state = self.state()
            if window_state == "iconic":
                return
            geometry = self.geometry()
        except tk.TclError:
            return
        if not is_valid_geometry(geometry):
            return
        settings_mgr.data["window_geometry"] = geometry
        settings_mgr.data["window_state"] = "zoomed" if window_state == "zoomed" else "normal"
        settings_mgr.save()

    def schedule_window_state_save(self, event=None):
        if event is not None and event.widget is not self:
            return
        if getattr(self, "_restoring_window_state", False):
            return
        after_id = getattr(self, "_window_state_after_id", None)
        if after_id is not None:
            try:
                self.after_cancel(after_id)
            except tk.TclError:
                pass
        self._window_state_after_id = self.after(DEFAULT_SAVE_DELAY_MS, lambda: save_window_state(self))

    def close_with_window_state_save(self):
        save_window_state(self)
        self.destroy()

    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self._window_state_after_id = None
        self._restoring_window_state = True
        try:
            restore_window_state(self)
        finally:
            self._restoring_window_state = False
        self.bind("<Configure>", lambda event: schedule_window_state_save(self, event), add="+")
        self.protocol("WM_DELETE_WINDOW", lambda: close_with_window_state_save(self))

    app_class.__init__ = __init__
    app_class.restore_window_state = restore_window_state
    app_class.save_window_state = save_window_state

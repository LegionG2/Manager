"""Tkinter UI package for Manager."""

from .app import WorkshopApp
from .ui_size_settings import enable_ui_size_settings
from .window_state_settings import enable_window_state_settings


enable_ui_size_settings(WorkshopApp)
enable_window_state_settings(WorkshopApp)

__all__ = ["WorkshopApp"]

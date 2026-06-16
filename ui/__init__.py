"""Tkinter UI package for Manager."""

from .app import WorkshopApp
from .ui_size_settings import enable_ui_size_settings


enable_ui_size_settings(WorkshopApp)

__all__ = ["WorkshopApp"]

"""View: Переиспользуемые UI-компоненты (без бизнес-логики)."""
import tkinter as tk
from tkinter import ttk


class LabeledEntry(ttk.Frame):
    """Компонент: метка + поле ввода."""

    def __init__(self, parent, label: str, **entry_kwargs):
        super().__init__(parent)
        ttk.Label(self, text=label).pack(anchor='w')
        self.entry = ttk.Entry(self, **entry_kwargs)
        self.entry.pack(fill='x', pady=2)

    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)


class StatusLabel(ttk.Label):
    """Компонент: статус с цветовой индикацией."""
    COLORS = {
        'ready': 'blue',
        'running': 'orange',
        'done': 'green',
        'error': 'red',
        'stopped': 'gray'
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.set_status('ready')

    def set_status(self, status: str, text: str = None) -> None:
        self.config(
            text=text or status.capitalize(),
            foreground=self.COLORS.get(status, 'black')
        )
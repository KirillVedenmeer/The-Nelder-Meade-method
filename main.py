#!/usr/bin/env python3
"""Точка входа приложения."""
import tkinter as tk
from ui.app import NelderMeadApp


def main():
    root = tk.Tk()
    # Центрирование окна
    root.update_idletasks()
    w, h = 1100, 750
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    app = NelderMeadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
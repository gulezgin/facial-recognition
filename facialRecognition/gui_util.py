import tkinter as tk
from tkinter import filedialog, ttk, Toplevel
from PIL import Image, ImageTk

def create_popup_window(root, title, width, height):
    popup_window = Toplevel(root)
    popup_window.title(title)
    popup_window.geometry(f"{width}x{height}")
    return popup_window

def create_canvas(parent, width, height):
    canvas = tk.Canvas(parent, width=width, height=height)
    canvas.pack(pady=20)
    return canvas

# Diğer yardımcı işlevler buraya eklenebilir

"""
===========================================
Autor: fiegraf
GitHub: https://github.com/fiegraf
Proyecto: Generador de Códigos QR
Versión: 1.1
Año: 2026
Licencia: Uso personal – No redistribuir sin permiso
===========================================
"""

import qrcode
import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import hashlib

# ---- FIRMA DIGITAL OCULTA ----
def firma_digital():
    texto = "fiegraf|QR_GENERATOR|2026"
    return hashlib.sha256(texto.encode()).hexdigest()

FIRMA_SOFTWARE = firma_digital()

# ---- ESTILOS Y COLORES DEL QR ----
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    RoundedModuleDrawer,
    CircleModuleDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask

print("=== GENERADOR DE CÓDIGOS QR ===")
# print("Firma digital:", FIRMA_SOFTWARE)  # ← solo para verificación

# Ventana principal (oculta)
root = tk.Tk()
root.withdraw()

# Pedir enlace
enlace = simpledialog.askstring(
    "Enlace",
    "Ingresá el enlace para generar el QR:"
)

if not enlace:
    messagebox.showerror("Error", "No se ingresó ningún enlace.")
    exit()

# Nombre del archivo
nombre_archivo = simpledialog.askstring(
    "Archivo",
    "Nombre del archivo (sin .png):"
)

if not nombre_archivo or nombre_archivo.strip() == "":
    nombre_archivo = "codigo_qr"

# Elegir estilo del QR
estilo = simpledialog.askstring(
    "Estilo del QR",
    "Elegí el estilo:\n\n"
    "1 - Cuadrado\n"
    "2 - Redondeado\n"
    "3 - Circular\n\n"
    "Ingresá 1, 2 o 3:"
)

if estilo == "2":
    drawer = RoundedModuleDrawer()
elif estilo == "3":
    drawer = CircleModuleDrawer()
else:
    drawer = SquareModuleDrawer()

# Color QR
messagebox.showinfo("Color del QR", "Seleccioná el color del QR")
color_qr = colorchooser.askcolor(title="Color del QR")[0]
if not color_qr:
    exit()

# Color fondo
messagebox.showinfo("Color de fondo", "Seleccioná el color de fondo")
color_fondo = colorchooser.askcolor(title="Color de fondo")[0]
if not color_fondo:
    exit()

# Logo
usar_logo = messagebox.askyesno("Logo", "¿Deseás agregar un logo al centro?")
logo = None

if usar_logo:
    ruta_logo = filedialog.askopenfilename(
        title="Seleccioná el logo",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp")]
    )
    if ruta_logo:
        logo = Image.open(ruta_logo).convert("RGBA")

# Crear QR
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)

qr.add_data(enlace)
qr.make(fit=True)

imagen_qr = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=drawer,
    color_mask=SolidFillColorMask(
        front_color=color_qr,
        back_color=color_fondo
    )
).convert("RGBA")

# Insertar logo
if logo:
    qr_ancho, qr_alto = imagen_qr.size
    tamaño_logo = qr_ancho // 5
    logo = logo.resize((tamaño_logo, tamaño_logo), Image.LANCZOS)

    pos = (
        (qr_ancho - tamaño_logo) // 2,
        (qr_alto - tamaño_logo) // 2
    )
    imagen_qr.paste(logo, pos, logo)

# ---------------- VISTA PREVIA ----------------
preview = tk.Toplevel()
preview.title("Vista previa del QR")
preview.resizable(False, False)

img_preview = ImageTk.PhotoImage(imagen_qr.resize((300, 300)))
label_img = tk.Label(preview, image=img_preview)
label_img.pack(padx=10, pady=10)

# ---- FIRMA VISIBLE ----
tk.Label(
    preview,
    text="Desarrollado por fiegraf • GitHub © 2026",
    font=("Arial", 9),
    fg="gray"
).pack(pady=4)

def guardar():
    archivo_final = f"{nombre_archivo}.png"
    imagen_qr.save(archivo_final)
    messagebox.showinfo("Éxito", f"QR guardado como:\n{archivo_final}")
    preview.destroy()

def cancelar():
    preview.destroy()

btn_frame = tk.Frame(preview)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Guardar QR", command=guardar, width=15).pack(side="left", padx=5)
tk.Button(btn_frame, text="Cancelar", command=cancelar, width=15).pack(side="right", padx=5)

preview.mainloop()

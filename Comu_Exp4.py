import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class SimuladorContextoRealUNEMI:
    """Simulador interactivo de transmisión de datos para UNEMI (Comunicación de Datos)."""

    TAG_COLORS = {"ESCENARIO": "#00d2ff", "APLICACIÓN": "#ffffff", "TEORÍA U3": "#ffcc00",
                  "PARIDAD": "#33ff33", "SISTEMA": "#ff66cc", "ERROR": "#ff4b2b"}

    def __init__(self, root):
        self.root = root
        self.root.title("PROYECTO: COMUNICACIÓN DE DATOS - UNEMI")
        self._maximizar_ventana()
        self.root.minsize(1000, 700)
        self.root.configure(bg="#1e1e2f")

        self.pausado = self.transmitiendo = False
        self.tour_ventana = self.tour_widget_resaltado = self.tour_resaltado_original = None

        # Ejemplos de contexto real vinculados a la teoría de la Unidad 3
        self.detalles_reales = [
            {"ejemplo": "WHATSAPP (WI-FI)", "explicacion": "Los bits de tu mensaje se modulan en ondas de radio de 2.4GHz. Aquí aplicas el Subtema 1: datos digitales viajando en señales analógicas.", "teoria": "Teorema de Nyquist: define la tasa máxima de bits en el aire."},
            {"ejemplo": "NETFLIX (FIBRA ÓPTICA)", "explicacion": "La luz se enciende y apaga (bits) para viajar por el vidrio. Es una señal periódica (Subtema 2) de altísima frecuencia.", "teoria": "Ancho de banda: es masivo, permitiendo video en 4K sin retrasos."},
            {"ejemplo": "LLAMADA CELULAR", "explicacion": "Tu voz (analógica) se digitaliza para procesarse y luego vuelve a ser onda para salir por la antena.", "teoria": "Relación Señal/Ruido (SNR): si hay interferencia, la calidad de voz baja."},
            {"ejemplo": "CONTROL DE TV (INFRARROJO)", "explicacion": "Pulsas un botón (dato discreto) y un LED emite ráfagas de luz invisible que el TV interpreta.", "teoria": "Codificación: cada botón tiene una secuencia de bits única."},
            {"ejemplo": "TRANSACCIÓN CAJERO (ATM)", "explicacion": "Tus datos bancarios viajan encriptados por cables de cobre usando módems DSL.", "teoria": "Ciberseguridad: es una vulnerabilidad compartida en redes públicas."},
        ]

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)
        self._build_header()
        self._build_panel_capas()
        self._build_area_graficos()
        self._build_consola()
        self._build_controles()
        self.root.after(500, self._iniciar_tour)

    # --- Construcción de la interfaz ---

    def _maximizar_ventana(self):
        try:
            self.root.state('zoomed')          # Windows
        except tk.TclError:
            try:
                self.root.attributes('-zoomed', True)   # Linux
            except tk.TclError:
                self.root.geometry("1200x800")           # Respaldo universal

    def _build_header(self):
        header = tk.Frame(self.root, bg="#002147", pady=10)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(header, text="UNIVERSIDAD ESTATAL DE MILAGRO (UNEMI)", font=("Helvetica", 16, "bold"), bg="#002147", fg="white").pack()
        tk.Label(header, text="Materia: Comunicación de Datos | Docente: Ing. Alex Armando Ávila Coello, Mgtr.", font=("Helvetica", 10), bg="#002147", fg="#ffcc00").pack()
        tk.Label(header, text="Simulador interactivo: observa cómo un texto se convierte en señal y viaja por la red", font=("Helvetica", 9, "italic"), bg="#002147", fg="#cfd8dc").pack(pady=(4, 0))

    def _build_panel_capas(self):
        cont = tk.Frame(self.root, bg="#1e1e2f", pady=8)
        cont.grid(row=1, column=0, sticky="ew", padx=20)
        cont.columnconfigure((0, 1, 2), weight=1)
        tk.Label(cont, text="RECORRIDO DEL MENSAJE POR EL MODELO OSI", font=("Helvetica", 10, "bold"), bg="#1e1e2f", fg="#00d2ff").grid(row=0, column=0, columnspan=3, pady=(0, 6))
        textos_capas = [
            ("CAPA DE APLICACIÓN", "El usuario escribe el texto en el Entry"),
            ("CAPA DE PRESENTACIÓN", "El texto se codifica: carácter → ASCII → binario"),
            ("CAPA FÍSICA", "Los bits se convierten en una onda analógica (portadora)"),
        ]
        self.capa_labels = []
        for i, (titulo, desc) in enumerate(textos_capas):
            box = tk.Label(cont, text=f"{titulo}\n{desc}", font=("Helvetica", 9, "bold"), bg="#2a2a40", fg="white",
                            bd=2, relief=tk.RIDGE, padx=8, pady=8, wraplength=260, justify="center")
            box.grid(row=1, column=i, sticky="ew", padx=6)
            self.capa_labels.append(box)
        self.lbl_binario = tk.Label(cont, text="Esperando transmisión...", font=("Consolas", 11, "bold"), bg="#1e1e2f", fg="#33ff33")
        self.lbl_binario.grid(row=2, column=0, columnspan=3, pady=(8, 0))

    def _build_area_graficos(self):
        self.main = tk.Frame(self.root, bg="#1e1e2f")
        self.main.grid(row=3, column=0, sticky="nsew", padx=20)
        self.main.columnconfigure(0, weight=1)
        self.fig, (self.ax_dig, self.ax_ana) = plt.subplots(2, 1, figsize=(6, 4))
        self.fig.patch.set_facecolor('#2a2a40')
        self.fig.subplots_adjust(hspace=0.6)
        for ax in (self.ax_dig, self.ax_ana):
            ax.set_facecolor('#1e1e2f')
            ax.tick_params(colors='white', labelsize=8)
            ax.title.set_color('white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=40)

    def _build_consola(self):
        self.consola = tk.Text(self.main, height=9, bg="#0d0d0d", fg="#33ff33", font=("Consolas", 10), padx=15, pady=10)
        self.consola.pack(fill=tk.X, padx=40, pady=10)

    def _build_controles(self):
        footer = tk.Frame(self.root, bg="#1e1e2f", pady=10)
        footer.grid(row=4, column=0, sticky="ew")
        footer.columnconfigure(5, weight=1)
        self.entry_msg = tk.Entry(footer, font=("Arial", 14), width=15, justify='center')
        self.entry_msg.grid(row=0, column=0, padx=(30, 10), pady=5)
        self.entry_msg.insert(0, "UNEMI")
        self.entry_msg.bind("<Return>", lambda e: self.transmitir())
        self.btn_tx = tk.Button(footer, text="⚡ TRANSMITIR Y ANALIZAR", command=self.transmitir, bg="#00d2ff", width=22, font=("Arial", 10, "bold"))
        self.btn_tx.grid(row=0, column=1, padx=5)
        self.btn_pausa = tk.Button(footer, text="⏸ PAUSAR", command=self.pausar_reanudar, bg="#ffcc00", width=12, state=tk.DISABLED)
        self.btn_pausa.grid(row=0, column=2, padx=5)
        self.btn_reset = tk.Button(footer, text="🔄 RESET", command=self.reset, bg="#ff4b2b", fg="white", width=10)
        self.btn_reset.grid(row=0, column=3, padx=5)
        self.btn_info = tk.Button(footer, text="ℹ️ GUÍA", command=self._iniciar_tour, bg="#3a3a55", fg="white", width=10)
        self.btn_info.grid(row=0, column=4, padx=5)
        vel_frame = tk.Frame(footer, bg="#1e1e2f")
        vel_frame.grid(row=0, column=5, padx=20, sticky="e")
        tk.Label(vel_frame, text="Velocidad:", bg="#1e1e2f", fg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.velocidad = tk.Scale(vel_frame, from_=300, to=2500, orient=tk.HORIZONTAL, bg="#1e1e2f", fg="white",
                                   troughcolor="#2a2a40", highlightthickness=0, length=160, showvalue=False)
        self.velocidad.set(1200)
        self.velocidad.pack(side=tk.LEFT, padx=5)
        progreso_frame = tk.Frame(self.root, bg="#1e1e2f")
        progreso_frame.grid(row=5, column=0, sticky="ew", padx=30, pady=(0, 10))
        progreso_frame.columnconfigure(0, weight=1)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Sim.Horizontal.TProgressbar", troughcolor="#2a2a40", background="#00d2ff", thickness=12)
        self.progreso = ttk.Progressbar(progreso_frame, style="Sim.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.progreso.grid(row=0, column=0, sticky="ew")
        self.lbl_estado = tk.Label(progreso_frame, text="Listo para transmitir.", bg="#1e1e2f", fg="#cfd8dc", font=("Arial", 9))
        self.lbl_estado.grid(row=1, column=0, sticky="w", pady=(4, 0))

    # --- Guía interactiva paso a paso (señala cada control y explica qué hace) ---

    def _construir_pasos_tour(self):
        # Cada paso: (widget a señalar, título, texto, posición preferida del globo)
        return [
            (self.entry_msg, "1. Escribe tu mensaje", "Aquí escribes el texto a transmitir. Solo letras, números y símbolos ASCII (máx. 25 caracteres).", "arriba"),
            (self.btn_tx, "2. Botón Transmitir", "Al presionarlo, tu mensaje recorre las 3 capas del modelo OSI, letra por letra, en tiempo real.", "arriba"),
            (self.capa_labels[1], "3. Capas del modelo OSI", "Estas 3 cajas se iluminan en secuencia (Aplicación → Presentación → Física) según la capa activa.", "abajo"),
            (self.canvas.get_tk_widget(), "4. Gráficas de la señal", "Arriba: señal digital (bits). Abajo: la onda analógica (portadora) con Modulación ASK.", "arriba"),
            (self.consola, "5. Consola de análisis", "Muestra un ejemplo real (Wi-Fi, fibra óptica, etc.) y el bit de paridad de cada letra.", "arriba"),
            (self.velocidad, "6. Velocidad de transmisión", "Deslízalo para ajustar el ritmo de la animación entre letra y letra.", "arriba"),
            (self.btn_pausa, "7. Pausar / Reanudar", "Congela la animación en el momento exacto que necesites para tus capturas.", "arriba"),
            (self.btn_reset, "8. Reset", "Limpia gráficas, consola y progreso para iniciar una nueva transmisión.", "arriba"),
            (self.btn_info, "9. Volver a ver esta guía", "Si quieres repasar estos pasos, presiona aquí en cualquier momento.", "arriba"),
        ]

    def _iniciar_tour(self):
        self.root.update_idletasks()
        self.tour_pasos = self._construir_pasos_tour()
        self.tour_indice = 0
        self._mostrar_paso_tour()

    def _mostrar_paso_tour(self):
        self._cerrar_popup_tour()
        widget, titulo, texto, preferida = self.tour_pasos[self.tour_indice]
        self._resaltar_widget_tour(widget)
        BORDE, AF, HF = "#00d2ff", 18, 7
        self.tour_ventana = tk.Toplevel(self.root)
        self.tour_ventana.overrideredirect(True)
        self.tour_ventana.attributes("-topmost", True)
        self.tour_ventana.configure(bg="#1e1e2f")
        contenido = tk.Frame(self.tour_ventana, bg="#1e1e2f", highlightthickness=2,
                              highlightbackground=BORDE, highlightcolor=BORDE, padx=14, pady=12)
        tk.Label(contenido, text=titulo, font=("Helvetica", 11, "bold"), bg="#1e1e2f", fg=BORDE, anchor="w", justify="left").pack(fill="x")
        tk.Label(contenido, text=texto, font=("Helvetica", 9), wraplength=300, bg="#1e1e2f", fg="white", justify="left", anchor="w").pack(fill="x", pady=(6, 10))
        nav = tk.Frame(contenido, bg="#1e1e2f")
        nav.pack(fill="x")
        tk.Label(nav, text=f"Paso {self.tour_indice + 1} de {len(self.tour_pasos)}", bg="#1e1e2f", fg="#8a8aa3", font=("Helvetica", 8)).pack(side=tk.LEFT)
        tk.Button(nav, text="Saltar", command=self._cerrar_tour, bg="#3a3a55", fg="white", font=("Helvetica", 9), bd=0, padx=8).pack(side=tk.RIGHT, padx=(4, 0))
        texto_btn = "Siguiente ▶" if self.tour_indice < len(self.tour_pasos) - 1 else "Entendido ✔"
        accion_btn = self._avanzar_tour if self.tour_indice < len(self.tour_pasos) - 1 else self._cerrar_tour
        tk.Button(nav, text=texto_btn, command=accion_btn, bg="#33cc66", fg="white", font=("Helvetica", 9, "bold"), bd=0, padx=10).pack(side=tk.RIGHT)
        if self.tour_indice > 0:
            tk.Button(nav, text="◀ Atrás", command=self._retroceder_tour, bg="#3a3a55", fg="white", font=("Helvetica", 9), bd=0, padx=8).pack(side=tk.RIGHT, padx=(0, 4))

        self.root.update_idletasks()
        cw, ch = contenido.winfo_reqwidth(), contenido.winfo_reqheight()
        posicion = self._decidir_posicion(widget, preferida, ch + HF)
        x, y = self._calcular_posicion(widget, cw, ch + HF, posicion)
        self.tour_ventana.geometry(f"{cw}x{ch + HF}+{x}+{y}")
        contenido.place(x=0, y=0 if posicion == "arriba" else HF)

        # Flechita que apunta al centro real del widget, aunque el globo se haya movido por falta de espacio
        cx_widget = widget.winfo_rootx() + widget.winfo_width() // 2 - x
        ax = max(8, min(cx_widget - AF // 2, cw - AF - 8))
        flecha = tk.Canvas(self.tour_ventana, width=AF, height=HF, bg="#1e1e2f", highlightthickness=0)
        if posicion == "abajo":
            flecha.create_polygon(AF / 2, 0, 0, HF, AF, HF, fill=BORDE, outline="")
            flecha.place(x=ax, y=0)
        else:
            flecha.create_polygon(0, 0, AF, 0, AF / 2, HF, fill=BORDE, outline="")
            flecha.place(x=ax, y=ch)

    def _decidir_posicion(self, widget, preferida, alto_total):
        # Voltea el globo al lado opuesto si no cabe en el lado preferido
        wy, wh = widget.winfo_rooty(), widget.winfo_height()
        pantalla_h = self.root.winfo_screenheight()
        espacio_abajo, espacio_arriba = pantalla_h - (wy + wh), wy
        necesario = alto_total
        if preferida == "abajo" and espacio_abajo < necesario and espacio_arriba > espacio_abajo:
            return "arriba"
        if preferida == "arriba" and espacio_arriba < necesario and espacio_abajo > espacio_arriba:
            return "abajo"
        return preferida

    def _calcular_posicion(self, widget, pw, ph, posicion):
        wx, wy, ww, wh = widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_width(), widget.winfo_height()
        pantalla_w, pantalla_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = wx + ww // 2 - pw // 2
        y = wy + wh if posicion == "abajo" else wy - ph
        x = max(10, min(x, pantalla_w - pw - 10))
        y = max(10, min(y, pantalla_h - ph - 10))
        return x, y

    def _avanzar_tour(self):
        self.tour_indice += 1
        self._mostrar_paso_tour()

    def _retroceder_tour(self):
        self.tour_indice -= 1
        self._mostrar_paso_tour()

    def _cerrar_tour(self):
        self._cerrar_popup_tour()
        self._quitar_resaltado()

    def _cerrar_popup_tour(self):
        if self.tour_ventana is not None:
            self.tour_ventana.destroy()
            self.tour_ventana = None

    def _resaltar_widget_tour(self, widget):
        self._quitar_resaltado()
        try:
            self.tour_resaltado_original = (widget.cget("highlightthickness"), widget.cget("highlightbackground"))
            widget.config(highlightthickness=3, highlightbackground="#00d2ff", highlightcolor="#00d2ff")
            self.tour_widget_resaltado = widget
        except tk.TclError:
            self.tour_widget_resaltado = None

    def _quitar_resaltado(self):
        if self.tour_widget_resaltado is not None and self.tour_resaltado_original is not None:
            try:
                grosor, color = self.tour_resaltado_original
                self.tour_widget_resaltado.config(highlightthickness=grosor, highlightbackground=color)
            except tk.TclError:
                pass
        self.tour_widget_resaltado = self.tour_resaltado_original = None

    # --- Consola ---

    def log(self, tag, msg):
        color = self.TAG_COLORS.get(tag, "#33ff33")
        tagname = f"tag_{tag}"
        if tagname not in self.consola.tag_names():
            self.consola.tag_configure(tagname, foreground=color, font=("Consolas", 10, "bold"))
        self.consola.insert(tk.END, f"[{tag}] ", tagname)
        self.consola.insert(tk.END, f"{msg}\n")
        self.consola.see(tk.END)

    # --- Pausa / Reset ---

    def pausar_reanudar(self):
        self.pausado = not self.pausado
        self.btn_pausa.config(text="▶ REANUDAR" if self.pausado else "⏸ PAUSAR")
        self.lbl_estado.config(text="⏸ Transmisión en pausa." if self.pausado else "▶ Transmitiendo...")

    def reset(self):
        self.transmitiendo = self.pausado = False
        for ax in (self.ax_dig, self.ax_ana):
            ax.clear()
        self.canvas.draw()
        self.consola.delete(1.0, tk.END)
        self.progreso['value'] = 0
        self.lbl_estado.config(text="Listo para transmitir.")
        self.lbl_binario.config(text="Esperando transmisión...")
        self._resaltar_capa(-1)
        self.btn_tx.config(state=tk.NORMAL)
        self.btn_pausa.config(state=tk.DISABLED, text="⏸ PAUSAR")

    def _resaltar_capa(self, indice):
        for i, box in enumerate(self.capa_labels):
            box.config(bg="#00d2ff" if i == indice else "#2a2a40", fg="#1e1e2f" if i == indice else "white")

    def _despues(self, ms, callback, *args):
        # Como root.after(), pero respeta la pausa antes de seguir avanzando
        def _intento():
            if self.pausado:
                self.root.after(200, _intento)
            else:
                callback(*args)
        self.root.after(int(ms), _intento)

    # --- Transmisión (animada con after(), sin congelar la interfaz) ---

    def transmitir(self):
        texto = self.entry_msg.get().upper().strip()
        if not texto:
            messagebox.showwarning("Atención", "Escribe un mensaje antes de transmitir.")
            return
        if not texto.isascii():
            messagebox.showwarning("Atención", "Usa solo caracteres ASCII (letras, números y símbolos básicos).")
            return
        if len(texto) > 25:
            messagebox.showwarning("Atención", "Usa un mensaje de máximo 25 caracteres para que las gráficas se vean claras.")
            return
        self.transmitiendo, self.pausado = True, False
        self.btn_tx.config(state=tk.DISABLED)
        self.btn_pausa.config(state=tk.NORMAL, text="⏸ PAUSAR")
        self.consola.delete(1.0, tk.END)
        self.progreso['maximum'] = len(texto)
        self.progreso['value'] = 0
        self.lbl_estado.config(text="▶ Transmitiendo...")
        self._procesar_indice(texto, 0)

    def _procesar_indice(self, texto, i):
        if not self.transmitiendo:
            return
        if i >= len(texto):
            self._finalizar(texto)
            return
        letra = texto[i]
        self.progreso['value'] = i + 1
        self.lbl_estado.config(text=f"Procesando carácter {i + 1} de {len(texto)}: '{letra}'")
        self._resaltar_capa(0)
        self.lbl_binario.config(text=f"Capa de Aplicación: el usuario escribió '{letra}'")
        self._despues(self.velocidad.get() / 3, self._paso_presentacion, texto, i, letra)

    def _paso_presentacion(self, texto, i, letra):
        bits = [int(b) for b in format(ord(letra), '08b')]
        self._resaltar_capa(1)
        self.lbl_binario.config(text=f"Capa de Presentación: '{letra}' → ASCII {ord(letra)} → {''.join(map(str, bits))}")
        self._despues(self.velocidad.get() / 3, self._paso_fisica, texto, i, letra, bits)

    def _paso_fisica(self, texto, i, letra, bits):
        self._resaltar_capa(2)
        self.lbl_binario.config(text=f"Capa Física: '{letra}' viaja como onda analógica (ASK)")
        self._graficar(letra, bits)
        paridad = sum(bits) % 2
        estado_paridad = "PAR" if paridad == 0 else "IMPAR"
        detalle = self.detalles_reales[i % len(self.detalles_reales)]
        self.log("ESCENARIO", detalle['ejemplo'])
        self.log("APLICACIÓN", detalle['explicacion'])
        self.log("TEORÍA U3", detalle['teoria'])
        self.log("PARIDAD", f"Bits en 1: {sum(bits)} → paridad {estado_paridad} (bit calculado: {paridad})")
        self.consola.insert(tk.END, "-" * 60 + "\n")
        self._despues(self.velocidad.get(), self._procesar_indice, texto, i + 1)

    def _graficar(self, letra, bits):
        self.ax_dig.clear()
        self.ax_ana.clear()
        self.ax_dig.step(range(len(bits)), bits, where='post', color='#00d2ff', lw=2)
        self.ax_dig.set_title(f"DOMINIO DIGITAL: Carácter '{letra}' procesado en CPU")
        self.ax_dig.set_ylim(-0.2, 1.2)
        t = np.linspace(0, len(bits), 1000)
        frecuencia = 5
        senal = np.sin(2 * np.pi * frecuencia * t) * np.repeat(bits, 1000 // len(bits))
        self.ax_ana.plot(t, senal, color='#ff4b2b', lw=1)
        self.ax_ana.set_title(f"MEDIO FÍSICO: Onda Analógica (ASK) transportando '{letra}'")
        self.canvas.draw()

    def _finalizar(self, texto):
        total_bits = len(texto) * 8
        self.log("SISTEMA", f"Mensaje '{texto}' transmitido completo: {len(texto)} caracteres, {total_bits} bits enviados.")
        self.lbl_estado.config(text="✅ Transmisión completa.")
        self.lbl_binario.config(text=f"Transmisión de '{texto}' finalizada con éxito")
        self._resaltar_capa(-1)
        self.transmitiendo = False
        self.btn_tx.config(state=tk.NORMAL)
        self.btn_pausa.config(state=tk.DISABLED, text="⏸ PAUSAR")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorContextoRealUNEMI(root)
    root.mainloop()
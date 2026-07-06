# CD_TPE_4_Simulador-de-Transmisi-n-de-Datos-en-Python-con-Contexto-Real
# Simulador de Transmisión de Datos - UNEMI

Simulador interactivo desarrollado en Python con Tkinter para la materia Comunicación de Datos en la Universidad Estatal de Milagro (UNEMI). Muestra en tiempo real cómo un mensaje de texto atraviesa las capas del modelo OSI, se codifica en binario y se transforma en una onda analógica mediante modulación ASK.

## Descripción

La aplicación toma un mensaje escrito por el usuario y lo procesa carácter por carácter, animando su recorrido por tres capas

- **Capa de Aplicación** - el usuario escribe el texto
- **Capa de Presentación** - cada carácter se convierte a su valor ASCII y luego a binario
- **Capa Física** - los bits se transforman en una señal analógica portadora usando modulación ASK

Cada letra procesada muestra además un ejemplo de contexto real (WhatsApp, Netflix, llamadas celulares, control remoto, cajeros automáticos) relacionado con la teoría de la Unidad 3, junto con el cálculo del bit de paridad correspondiente.

## Características principales

- Animación paso a paso sin congelar la interfaz, usando `root.after()` en lugar de hilos o bucles bloqueantes
- Gráficas en tiempo real de la señal digital (bits) y la señal analógica modulada, generadas con Matplotlib
- Consola de análisis con colores por categoría (escenario, aplicación, teoría, paridad, sistema, error)
- Control de velocidad de transmisión mediante un deslizador
- Botones de pausa y reanudación que congelan la animación en cualquier punto
- Barra de progreso y estado textual de la transmisión
- Tour guiado interactivo que señala cada control de la interfaz con una explicación, con posicionamiento adaptativo según el espacio disponible en pantalla
- Validación de entrada, solo caracteres ASCII y un máximo de 25 caracteres

## Requisitos

- Python 3.8 o superior
- matplotlib
- numpy

## Instalación

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
pip install matplotlib numpy
```

## Uso

```bash
python Comu_Exp4.py
```

Al iniciar, la aplicación abre en pantalla completa y despliega automáticamente un tour guiado que explica cada parte de la interfaz. Para transmitir un mensaje

1. Escribe un texto en el campo de entrada (por defecto aparece "UNEMI")
2. Presiona **TRANSMITIR Y ANALIZAR**
3. Observa cómo el mensaje recorre las capas del modelo OSI, letra por letra
4. Usa el deslizador de velocidad para ajustar el ritmo de la animación
5. Pausa o reinicia la simulación con los botones correspondientes
6. Presiona **GUÍA** en cualquier momento para volver a ver el tour

## Licencia

Uso académico. Libre para consulta y adaptación con fines educativos.

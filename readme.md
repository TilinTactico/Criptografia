#  Motor de Criptoanálisis por Hill Climbing

Práctica de criptografia en Python capaz de cifrar, descifrar y romper cifrados de sustitución simple utilizando análisis estadístico de lenguaje (trigramas) y el algoritmo heurístico de búsqueda local Hill Climbing.

## Características Principales

* **Criptoanálisis Estadístico:** Entrena un modelo de lenguaje basado en un corpus de texto en español para evaluar la aptitud (score logarítmico) de posibles claves.
* **Algoritmo Hill Climbing:** Búsqueda heurística con soporte para múltiples reinicios (restarts) aleatorios para evitar estancamientos en máximos locales.
* **Medición de Hardware:** Calcula el rendimiento del ataque utilizando los ciclos de reloj exactos del procesador (CPU) mediante la lectura directa del registro del sistema operativo.
* **Reportes Dinámicos:** Genera reportes detallados que incluyen la clave inicial, clave final, score logarítmico y porcentaje de efectividad exacto si se provee un texto de referencia.
* **Interfaz de Línea de Comandos (CLI):** Completamente modular y ejecutable desde la terminal mediante argumentos personalizados.

##  Requisitos del Sistema

* **Python 3.x** instalado en el sistema.
* No requiere instalación de dependencias externas (utiliza únicamente librerías nativas de la biblioteca estándar de Python: `os`, `math`, `random`, `re`, `collections`, `time`, `argparse`, `platform`, `winreg`).
* Diseñado y optimizado para entornos **Windows (PowerShell/CMD)**, aunque compatible con Linux/macOS.

##  Estructura del Proyecto

* `criptografia_final.py`: Script principal y motor del proyecto.
* `/corpus`: Carpeta que contiene los textos en claro utilizados para entrenar el modelo de trigramas.
* `/textos_pruebas`: Textos de ejemplo para realizar pruebas de cifrado y ataques.
* `/resultados_cifrados`: Directorio autogenerado donde se guardan los criptogramas.
* `/resultados_descifrados`: Directorio autogenerado para los textos recuperados y reportes de ataque.

---

##  Comandos de Ejecución

El script principal se ejecuta a través de la terminal. Debes indicar la operación deseada (`cifrar`, `decifrar`, `romper_cifrado`) seguida de sus argumentos correspondientes.

###  Cifrar (`cifrar`)
Cifra un archivo de texto en claro.

**Parámetros:**
* `-i` (`--input`): Ruta del archivo `.txt` de entrada. *(Obligatorio)*
* `-o` (`--output`): Ruta del archivo `.txt` cifrado de salida. *(Obligatorio)*
* `-k` (`--key`): Clave de 27 letras para cifrar. Si se omite, se usará la clave QWERTY por defecto. *(Opcional)*

**Ejemplos de uso:**
```powershell
# Cifrado básico usando clave por defecto
python .\criptografia_final.py cifrar -i "texto_a_cifrar.txt" -o "texto_cifrado.txt"

# Cifrado usando una clave personalizada
python .\criptografia_final.py cifrar -i .\textos_pruebas\resident_evil_arcano.txt -o .\resultados_cifrados\resident_cifrado.txt -k "VÑKPWXJMBYFCDUHQAZNOLTRISGE"
```

###  Descifrar (`descifrar`)
Descifra un texto cifrado si ya conoces la clave correcta.

**Parámetros:**
* `-i` (`--input`): Ruta del archivo `.txt` cifrado de entrada. *(Obligatorio)*
* `-o` (`--output`): Ruta del archivo `.txt` descifrado de salida. *(Obligatorio)*
* `-k` (`--key`): Clave de 27 letras para descifrar. Si se omite, se usará la clave QWERTY por defecto. *(Opcional)*

**Ejemplos de uso:**
```powershell
# Descifrado básico
python .\criptografia_final.py decifrar -i "texto_cifrado.txt" -o "texto_descifrado.txt"

# Descifrado con clave específica
python .\criptografia_final.py decifrar -i "texto_cifrado.txt" -o "texto_descifrado.txt" -k "VÑKPWXJMBYFCDUHQAZNOLTRISGE"
```

###  Romper Cifrado (`romper_cifrado`)
Ejecuta el criptoanálisis estadístico mediante el algoritmo *Hill Climbing* para descubrir la clave sin conocerla previamente.

**Parámetros principales:**
* `-i` (`--input`): Ruta del archivo `.txt` cifrado. *(Obligatorio)*
* `-o` (`--output`): Ruta para guardar el texto recuperado. *(Obligatorio)*
* `-c` (`--chars`): Número de caracteres a evaluar. Si se omite, analiza todo el texto. *(Opcional)*
* `-ref` (`--reference`): Archivo de texto original en claro para que el reporte calcule el % de efectividad exacto. *(Opcional)*
* `-co` (`--corpus`): Carpeta que contiene los textos para entrenar el modelo. Por defecto usa `corpus`. *(Opcional)*

**Parámetros de ataque y salida:**
* `-rs` (`--restarts`): Número de reinicios del algoritmo. Por defecto: `15`. *(Opcional)*
* `-it` (`--iterations`): Iteraciones por reinicio. Por defecto: `3000`. *(Opcional)*
* `-r` (`--report`): Carpeta para exportar el reporte `.txt`. Si se omite, el reporte solo se imprime en consola. *(Opcional)*
* `-v` (`--verbose`): Imprime el progreso del descifrado en tiempo real. *(Opcional)*

**Ejemplos de uso:**
```powershell
# 1. Ataque rápido y directo mostrando reporte en consola
python .\criptografia_final.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt"

# 2. Ataque evaluando solo 1000 letras y guardando el reporte en carpeta
python .\criptografia_final.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -c 1000 -r "carpeta_resultados"

# 3. Ataque profundo con parámetros personalizados, calculando % de éxito y progreso en vivo
python .\criptografia_final.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -c 5000 -rs 20 -it 4000 -ref "texto_original.txt" -v
```
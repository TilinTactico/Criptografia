import os
import math
import random
import re
from collections import Counter
import time
import argparse


# Clave por defecto
alfabeto_normal = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
alfabeto_qwerty = "QWERTYUIOPASDFGHJKLÑZXCVBNM"
clave_qwerty = dict(zip(alfabeto_normal, alfabeto_qwerty))

# Frecuencia del procesador para obtener los ciclos de reloj
FRECUENCIA_CPU_HZ = 2_400_000_000


# Se aplican las reglas:
# Todo en mayusculas
# Se eliminan acentos
# Se eliminan caracteres especiales, espacios y numeros
def normalizar_texto(texto: str):
    texto_normalizado = texto.upper()
    tabla_acentos = str.maketrans('ÁÉÍÓÚ', 'AEIOU')
    texto_normalizado = texto_normalizado.translate(tabla_acentos)
    texto_normalizado = re.sub(r'[^A-ZÑ]', '', texto_normalizado)
    return texto_normalizado


def obtener_trigramas(texto: str) -> list:
    return [texto[i:i + 3] for i in range(len(texto) - 2)]


def leer_textos_de_corpus(ruta_carpeta: str) -> str:
    texto_unido = ""
    if not os.path.exists(ruta_carpeta):
        print(f"Error: No se encontró la carpeta '{ruta_carpeta}'")
        return ""

    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                texto_unido += archivo.read()
    return texto_unido


def calcular_estadisticas(coleccion) -> tuple:
    total_elementos = len(coleccion)
    frecuencias = Counter(coleccion)
    probabilidades = {
        elemento: (frecuencia / total_elementos)
        for elemento, frecuencia in frecuencias.items()
    }
    return total_elementos, frecuencias, probabilidades


def calcular_entropia_letras(probabilidades_letras: dict) -> float:
    entropia = -sum(probabilidad * math.log2(probabilidad) for probabilidad in probabilidades_letras.values())
    return entropia


def construir_modelo_trigramas(probabilidades_trigramas: dict, total_trigramas: int) -> dict:
    B = total_trigramas
    p_min = 1 / (10 * B)
    modelo = {
        "probabilidades": probabilidades_trigramas,
        "p_min": p_min
    }
    return modelo


def puntuacion_trigramas(texto: str, modelo: dict) -> float:
    trigramas_texto = obtener_trigramas(texto)
    probabilidades = modelo["probabilidades"]
    p_min = modelo["p_min"]
    score = 0.0
    for trigrama in trigramas_texto:
        probabilidad = probabilidades.get(trigrama, p_min)
        score += math.log2(probabilidad)
    return score


def cifrar(texto: str, clave: dict) -> str:
    return "".join(clave[letra] for letra in texto)


def descifrar(texto_cifrado: str, clave: dict) -> str:
    clave_invertida = {valor: llave for llave, valor in clave.items()}
    return "".join(clave_invertida[letra] for letra in texto_cifrado)


def generar_clave_aleatoria(alfabeto: str) -> dict:
    alfabeto_lista = list(alfabeto)
    alfabeto_mezclado = alfabeto_lista.copy()
    random.shuffle(alfabeto_mezclado)
    return dict(zip(alfabeto_lista, alfabeto_mezclado))


def generar_vecino(clave_actual: dict) -> dict:
    nueva_clave = clave_actual.copy()
    letras = list(nueva_clave.keys())
    letra1, letra2 = random.sample(letras, 2)
    nueva_clave[letra1], nueva_clave[letra2] = nueva_clave[letra2], nueva_clave[letra1]
    return nueva_clave


def hill_climbing(criptograma: str, modelo: dict, alfabeto: str, iteraciones: int) -> tuple:
    clave_inicial = generar_clave_aleatoria(alfabeto)
    mejor_clave = clave_inicial.copy()
    mejor_texto = descifrar(criptograma, mejor_clave)
    mejor_score = puntuacion_trigramas(mejor_texto, modelo)

    for _ in range(iteraciones):
        nueva_clave = generar_vecino(mejor_clave)
        nuevo_texto = descifrar(criptograma, nueva_clave)
        nuevo_score = puntuacion_trigramas(nuevo_texto, modelo)

        if nuevo_score > mejor_score:
            mejor_clave = nueva_clave
            mejor_texto = nuevo_texto
            mejor_score = nuevo_score

    return clave_inicial, mejor_clave, mejor_texto, mejor_score


def romper_sustitucion(criptograma: str, modelo: dict, alfabeto: str, reinicios: int,
                       iteraciones: int, verbose: bool = False) -> tuple:
    mejor_clave_global = None
    mejor_texto_global = ""
    mejor_score_global = float('-inf')

    historial_reinicios = []

    for i in range(reinicios):
        clave_inicial, clave_local, texto_local, score_local = hill_climbing(criptograma, modelo, alfabeto, iteraciones)

        if score_local > mejor_score_global:
            mejor_score_global = score_local
            mejor_clave_global = clave_local
            mejor_texto_global = texto_local

        str_clave_inicial = "".join(clave_inicial[letra] for letra in alfabeto)
        str_clave_local = "".join(clave_local[letra] for letra in alfabeto)

        historial_reinicios.append((i + 1, score_local, str_clave_inicial, str_clave_local, texto_local))

        if verbose:
            print(f"[-] Reinicio {i + 1}/{reinicios} completado | Mejor score local: {score_local:.2f}")
            print(f"    Descifrado parcial: {texto_local[:80]}...\n")

    return mejor_clave_global, mejor_texto_global, mejor_score_global, historial_reinicios


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor de Criptoanálisis - Sustitución Simple")
    subparsers = parser.add_subparsers(dest="comando", required=True, help="Operación a realizar")

    # Comando 1: cifrar
    parser_cifrar = subparsers.add_parser("cifrar", help="Cifra un archivo de texto")
    parser_cifrar.add_argument("-i", "--input", required=True, help="Ruta del archivo .txt de entrada")
    parser_cifrar.add_argument("-o", "--output", required=True, help="Ruta del archivo .txt de salida")
    parser_cifrar.add_argument("-k", "--key", type=str, help="Clave de 27 letras para cifrar (Si se omite, usa QWERTY)")

    # Comando 2: decifrar
    parser_decifrar = subparsers.add_parser("decifrar", help="Descifra un archivo de texto cifrado")
    parser_decifrar.add_argument("-i", "--input", required=True, help="Ruta del archivo .txt cifrado de entrada")
    parser_decifrar.add_argument("-o", "--output", required=True, help="Ruta del archivo .txt descifrado de salida")
    parser_decifrar.add_argument("-k", "--key", type=str,
                                 help="Clave de 27 letras para descifrar (Si se omite, usa QWERTY)")

    # Comando 3: romper_cifrado
    parser_romper = subparsers.add_parser("romper_cifrado", help="Rompe el cifrado usando estadística (Hill Climbing)")
    parser_romper.add_argument("-i", "--input", required=True, help="Ruta del archivo .txt cifrado de entrada")
    parser_romper.add_argument("-o", "--output", required=True, help="Ruta para guardar el texto puro descifrado")
    parser_romper.add_argument("-r", "--report", type=str,
                               help="Carpeta para el reporte. Si se omite, se muestra en pantalla")
    parser_romper.add_argument("-c", "--chars", type=int,
                               help="Número de caracteres a procesar (Si se omite, usa todo el texto)")
    parser_romper.add_argument("-co", "--corpus", default="corpus",
                               help="Ruta de la carpeta del corpus (default: 'corpus')")
    parser_romper.add_argument("-rs", "--restarts", type=int, default=15, help="Número de reinicios (default: 15)")
    parser_romper.add_argument("-it", "--iterations", type=int, default=3000,
                               help="Iteraciones por reinicio (default: 3000)")
    parser_romper.add_argument("-v", "--verbose", action="store_true", help="Muestra el progreso detallado en pantalla")
    parser_romper.add_argument("-ref", "--reference", type=str,
                               help="Ruta del texto original (Para calcular porcentaje de efectividad)")

    args = parser.parse_args()

    # LÓGICA PARA CIFRAR
    if args.comando == "cifrar":
        if not os.path.exists(args.input):
            print(f"Error: El archivo '{args.input}' no existe.")
            exit(1)

        with open(args.input, 'r', encoding='utf-8') as f:
            texto_crudo = f.read()
        texto_limpio = normalizar_texto(texto_crudo)

        if args.key:
            clave_limpia = args.key.upper()
            if len(clave_limpia) != 27:
                print("Error: La clave proporcionada mediante -k debe tener exactamente 27 caracteres.")
                exit(1)
            clave_usada = dict(zip(alfabeto_normal, clave_limpia))
        else:
            clave_usada = clave_qwerty

        criptograma = cifrar(texto_limpio, clave_usada)

        directorio_salida = os.path.dirname(args.output)
        if directorio_salida and not os.path.exists(directorio_salida):
            os.makedirs(directorio_salida)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(criptograma)

        print(f"[*] Cifrado completado con éxito.")
        print(f"[*] Archivo guardado en: {args.output}")
        print(f"[*] Clave utilizada: {''.join(clave_usada[letra] for letra in alfabeto_normal)}")


    # LÓGICA PARA DESCIFRAR
    elif args.comando == "decifrar":
        if not os.path.exists(args.input):
            print(f"Error: El archivo '{args.input}' no existe.")
            exit(1)

        with open(args.input, 'r', encoding='utf-8') as f:
            criptograma_crudo = f.read()
        criptograma_limpio = normalizar_texto(criptograma_crudo)

        if args.key:
            clave_limpia = args.key.upper()
            if len(clave_limpia) != 27:
                print("Error: La clave proporcionada mediante -k debe tener exactamente 27 caracteres.")
                exit(1)
            clave_usada = dict(zip(alfabeto_normal, clave_limpia))
        else:
            clave_usada = clave_qwerty

        texto_claro = descifrar(criptograma_limpio, clave_usada)

        directorio_salida = os.path.dirname(args.output)
        if directorio_salida and not os.path.exists(directorio_salida):
            os.makedirs(directorio_salida)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(texto_claro)

        print(f"[*] Descifrado completado con éxito.")
        print(f"[*] Archivo guardado en: {args.output}")


    # LÓGICA PARA ROMPER CIFRADO (CRIPTOANÁLISIS)
    elif args.comando == "romper_cifrado":
        if not os.path.exists(args.input):
            print(f"Error: El archivo '{args.input}' no existe.")
            exit(1)

        with open(args.input, 'r', encoding='utf-8') as f:
            criptograma_crudo = f.read()
        criptograma_limpio = normalizar_texto(criptograma_crudo)

        if args.chars:
            if args.chars > len(criptograma_limpio):
                print(
                    f"[!] Advertencia: Solicitaste {args.chars} caracteres, pero el texto solo tiene {len(criptograma_limpio)}. Se usará el texto completo.")
            else:
                criptograma_limpio = criptograma_limpio[:args.chars]

        texto_referencia = None
        if args.reference:
            if not os.path.exists(args.reference):
                print(f"Error: El archivo de referencia '{args.reference}' no existe.")
                exit(1)
            with open(args.reference, 'r', encoding='utf-8') as f:
                ref_crudo = f.read()
            texto_referencia = normalizar_texto(ref_crudo)
            if args.chars:
                texto_referencia = texto_referencia[:args.chars]

        print(f"[*] Entrenando modelo estadístico con corpus en '{args.corpus}'...")
        texto_crudo_corpus = leer_textos_de_corpus(args.corpus)
        if not texto_crudo_corpus:
            print("Error fatal: No se pudo cargar el corpus para el análisis.")
            exit(1)

        texto_limpio_corpus = normalizar_texto(texto_crudo_corpus)
        lista_trigramas_corpus = obtener_trigramas(texto_limpio_corpus)
        total_tri, _, prob_tri = calcular_estadisticas(lista_trigramas_corpus)
        modelo_estadistico = construir_modelo_trigramas(prob_tri, total_tri)

        print(f"[*] Iniciando ataque Hill Climbing a un texto de {len(criptograma_limpio)} caracteres...")
        print(f"[*] Reinicios: {args.restarts} | Iteraciones por reinicio: {args.iterations}")
        if args.verbose:
            print("[*] Modo Verbose activado. Mostrando progreso en tiempo real...\n")

        inicio_cpu = time.process_time()

        clave_recup, texto_recup, mejor_score, historial = romper_sustitucion(
            criptograma_limpio, modelo_estadistico, alfabeto_normal,
            reinicios=args.restarts, iteraciones=args.iterations, verbose=args.verbose
        )

        tiempo_cpu = time.process_time() - inicio_cpu
        ciclos_estimados = int(tiempo_cpu * FRECUENCIA_CPU_HZ)

        directorio_salida = os.path.dirname(args.output)
        if directorio_salida and not os.path.exists(directorio_salida):
            os.makedirs(directorio_salida)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(texto_recup)
        print(f"[*] Texto descifrado guardado en: {args.output}")


        bloque_historial = "\n--- HISTORIAL DE REINICIOS ---\n"
        for num, score, clave_ini_str, clave_fin_str, texto_local in historial:
            if texto_referencia:
                longitud_eval = min(len(texto_referencia), len(texto_local))
                correctas = sum(1 for i in range(longitud_eval) if texto_referencia[i] == texto_local[i])
                porcentaje = (correctas / len(texto_local)) * 100 if len(texto_local) > 0 else 0
                bloque_historial += (f"Reinicio {num:02d} | Score: {score:10.2f} | Efectividad: {porcentaje:6.2f}%\n"
                                     f"            | C. Inicial: {clave_ini_str}\n"
                                     f"            | C. Final:   {clave_fin_str}\n")
            else:
                bloque_historial += (f"Reinicio {num:02d} | Score: {score:10.2f}\n"
                                     f"            | C. Inicial: {clave_ini_str}\n"
                                     f"            | C. Final:   {clave_fin_str}\n")

        linea_efectividad_final = ""
        if texto_referencia:
            longitud_eval = min(len(texto_referencia), len(texto_recup))
            correctas = sum(1 for i in range(longitud_eval) if texto_referencia[i] == texto_recup[i])
            efectividad_final = (correctas / len(texto_recup)) * 100 if len(texto_recup) > 0 else 0
            linea_efectividad_final = f"Efectividad final: {efectividad_final:.2f}%\n"

        str_clave_recuperada = "".join(clave_recup[letra] for letra in alfabeto_normal)
        reporte = (
            f"\n=================================================\n"
            f" REPORTE DE CRIPTOANÁLISIS ESTADÍSTICO\n"
            f"=================================================\n"
            f"Archivo atacado:   {args.input}\n"
            f"Caracteres eval.:  {len(criptograma_limpio)}\n"
            f"Archivo generado:  {args.output}\n"
            f"Tiempo de CPU:     {tiempo_cpu:.4f} segundos\n"
            f"Ciclos de CPU:     {ciclos_estimados:,} ciclos\n"
            f"Score logarítmico: {mejor_score:.2f}\n"
            f"{linea_efectividad_final}"
            f"Alfabeto base:     {alfabeto_normal}\n"
            f"Clave recuperada:  {str_clave_recuperada}\n"
            f"{bloque_historial}"
            f"=================================================\n"
        )

        if args.report:
            if not os.path.exists(args.report):
                os.makedirs(args.report)
            nombre_base = os.path.basename(args.input)
            nombre_sin_ext = os.path.splitext(nombre_base)[0]
            ruta_reporte = os.path.join(args.report, f"{nombre_sin_ext}_resultado.txt")

            with open(ruta_reporte, 'w', encoding='utf-8') as f:
                f.write(reporte)
            print(f"[*] Reporte de operaciones guardado en: {ruta_reporte}")
        else:
            print(reporte)

        print(f"\n[*] ¡Ataque completado con éxito en {ciclos_estimados:,} ciclos de CPU!")
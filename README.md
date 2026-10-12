# Comandos para su ejecucion
## cifrar 
-i: texto de entrada para cifrar, debe estar en un .txt
-o: texto de salida cifrado, sale en formato .txt
-k clave para cifrar, si no se coloca, se usara una por default
´´´CMD
python .\criptografia.py cifrar -i "texto_a_cifrar.txt" -o "texto_cifrado.txt"

python .\criptografia.py cifrar -i .\textos_pruebas\resident_evil_arcano.txt -o .\resultados_cifrados\resident_cifrado_clave_diferente.txt -k "CLAVE_ALEATORIA"
´´´

## Descifrar
-i: texto de entrada para descifrar, debe estar en un .txt
-o: texto de salida descifrado, sale en formato .txt
-k clave para descifrar, si no se coloca, se usara una por default

´´´CMD
python .\criptografia.py descifrar -i "texto_cifrado.txt" -o "texto_descifrado.txt"

python .\criptografia.py descifrar -i "texto_cifrado" -o "texto_descifrado" -k "CLAVE_ALEATORIA"
´´´

## Romper cifrado
-i: texto de entrada cifrado, debe de estar en un .txt
-o: texto de salida descifrado, sale en formato .txt
-r: carpeta donde se guardara la informacion del resultado del hill climb, si no se coloca se mostrara el resultado en pantalla
-c: numero de caracteres que se tomaran para realizar el ataque, si no se coloca, se usara todo el archivo para el ataque
-rs: numero de veces que se reiniciara el hill climb, cada reinicio crea una clave aleatoria e itera esa clave n veces, si no se coloca se usara un numero por default
-it: numero de iteraciones de cada reinicio, cada iteracion hace un cambio de dos caracteres a clave, si no se coloca se usara un numero por default
-ref: archivo de referencia para mostrar el porcentaje de efectividad del ataque, se coloca el archivo original
´´´CMD
python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt"

python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -r "carpeta_resultados"

python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -c caracteres

python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -r "carpeta_resultados" -c caracteres

python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -c caracteres -c 1000 -rs intentos

python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -c caracteres -c 1000 -rs intentos -it iteraciones 

python .\criptografia.py romper_cifrado -i "texto_cifrado.txt" -o "texto_descifrado.txt" -c caracteres -c 1000 -rs intentos -it iteraciones -ref "texto_original.txt"

´´´

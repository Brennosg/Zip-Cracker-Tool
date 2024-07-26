import pyzipper
import itertools
from datetime import datetime
import zlib

# Função que gera combinações de palavras dentro de um intervalo de tamanhos
def gerar_combinacoes(words, minimo, maximo):
    # Para cada comprimento no intervalo especificado
    for length in range(minimo, maximo + 1):
        # Gera todas as combinações possíveis de palavras com o comprimento atual
        for comb in itertools.product(words, repeat=length):
            # Concatena a tupla de caracteres em uma string e retorna
            yield ''.join(comb)

# Função que conta o número total de combinações possíveis dentro de um intervalo de tamanhos
def contar_combinacoes(words, minimo, maximo):
    total = 0
    # Para cada comprimento no intervalo especificado
    for length in range(minimo, maximo + 1):
        # Calcula o número de combinações possíveis para o comprimento atual
        total += len(words) ** length
    return total

# Função principal para descompactar o arquivo usando um ataque de dicionário
def descompactar_arquivo(nome, minimo, maximo):
    words = 'abcdefghijklmnopqrstuvwxyz'  # Conjunto de caracteres usados para gerar combinações
    total_combinacoes = contar_combinacoes(words, minimo, maximo)  # Conta o número total de combinações
    print(f'\n{datetime.strftime(datetime.now(), "%H:%M:%S")} >> Gerando e Processando {total_combinacoes} Combinacoes, Aguarde...')
    
    combinacoes = gerar_combinacoes(words, minimo, maximo)  # Gera as combinações
    combinacao_numero = 0  # Contador de combinações testadas
    
    # Para cada tentativa de combinação gerada
    for tentativa in combinacoes:
        combinacao_numero += 1  # Incrementa o contador de combinações testadas
        print(f'{datetime.strftime(datetime.now(), "%H:%M:%S")} >> Tentando combinação {combinacao_numero}/{total_combinacoes}: {tentativa}')
        resultado = tentar_descompactar(nome, tentativa)  # Tenta descompactar o arquivo com a senha atual
        if resultado:
            # Se a senha correta for encontrada, imprime e termina a função
            print(f'\n{datetime.strftime(datetime.now(), "%H:%M:%S")} >> Senha encontrada: {tentativa}')
            return
    # Se nenhuma senha correta for encontrada, informa ao usuário
    print(f'\n{datetime.strftime(datetime.now(), "%H:%M:%S")} >> Nenhuma senha encontrada no intervalo especificado.')

# Função que tenta descompactar o arquivo com uma senha específica
def tentar_descompactar(nome, senha):
    try:
        # Tenta abrir o arquivo ZIP com a senha fornecida
        with pyzipper.AESZipFile(nome, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as ziper:
            ziper.extractall(pwd=str.encode(senha), path='data')  # Extrai o conteúdo do arquivo ZIP se a senha estiver correta
            return True  # Retorna True se a descompactação for bem-sucedida
    except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile, pyzipper.zipfile.BadZipFile, zlib.error):
        # Captura exceções relacionadas a erros de descompactação e continua
        return False  # Retorna False se ocorrer uma exceção

# Ponto de entrada do programa
if __name__ == "__main__":
    descompactar_arquivo("Zip.zip", 4, 5)  # Chama a função principal com o nome do arquivo e o intervalo de tamanhos das senhas

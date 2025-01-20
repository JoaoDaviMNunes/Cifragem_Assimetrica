# === server.py ===
import socket  # Biblioteca para comunicação de rede
import random  # Biblioteca para geração de números aleatórios
from math import gcd  # Função para calcular o máximo divisor comum

# Função para gerar as chaves RSA
def gerar_chaves_rsa():
    p = 61  # Primeiro número primo
    q = 53  # Segundo número primo
    n = p * q  # Produto dos primos, usado como módulo
    phi = (p - 1) * (q - 1)  # Totiente de Euler
    e = 17  # Expoente público, escolhido coprimo com phi
    d = pow(e, -1, phi)  # Expoente privado, inverso modular de e
    return (e, n), (d, n)  # Retorna chave pública (e, n) e privada (d, n)

# Função para decifrar uma mensagem RSA
def decifrar_rsa(mensagem_cifrada, chave_privada):
    d, n = chave_privada  # Extrai chave privada
    # Decifra cada elemento da mensagem cifrada e converte para caractere
    return ''.join([chr(pow(caractere, d, n)) for caractere in mensagem_cifrada])

# Função para calcular a troca de chaves Diffie-Hellman
def troca_chave_diffie_hellman(primo, gerador, chave_privada):
    # pow (base, exp, mod)
    return pow(gerador, chave_privada, primo)  # Calcula a chave pública

# Código do servidor
def servidor():
    # Gera as chaves RSA do servidor
    chave_publica, chave_privada = gerar_chaves_rsa()
    print("Chave Pública do Servidor (RSA):", chave_publica)

    # Parâmetros da troca Diffie-Hellman
    primo = 23  # Número primo de 6 dígitos usado no cálculo
    gerador = 5  # Gerador usado no cálculo
    chave_privada_servidor = random.randint(1, primo - 1)  # Chave privada do servidor
    chave_publica_servidor = troca_chave_diffie_hellman(primo, gerador, chave_privada_servidor)
    print("Chave Pública do Servidor (Diffie-Hellman):", chave_publica_servidor)

    # Configuração do socket para comunicação
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 12345))  # Vincula o servidor ao endereço e porta
        s.listen(1)  # Aguarda conexões
        print("Aguardando conexão de um cliente...")
        conn, addr = s.accept()  # Aceita a conexão do cliente
        with conn:
            print("Conexão estabelecida com", addr)  # Informa o endereço do cliente

            # Envia a chave pública RSA para o cliente
            conn.sendall(str(chave_publica).encode())

            # Recebe a chave pública Diffie-Hellman e a mensagem cifrada do cliente
            dados_recebidos = conn.recv(1024).decode()  # Decodifica os dados recebidos do cliente

            # Divide os dados recebidos em chave pública e mensagem cifrada
            partes = dados_recebidos.split('|')  # Separador customizado para distinguir as partes
            chave_publica_cliente = int(partes[0])  # Converte a primeira parte na chave pública do cliente
            mensagem_cifrada = eval(partes[1])  # Avalia a segunda parte como uma lista

            print("Chave Pública do Cliente (Diffie-Hellman):", chave_publica_cliente)

            # Calcula o segredo compartilhado usando Diffie-Hellman
            segredo_compartilhado = pow(chave_publica_cliente, chave_privada_servidor, primo)
            print("Segredo Compartilhado:", segredo_compartilhado)

            # Decifra a mensagem usando RSA
            mensagem_decifrada = decifrar_rsa(mensagem_cifrada, chave_privada)
            print("Mensagem Decifrada:", mensagem_decifrada)

            # Exibe todas as informações
            print("Chave Pública do Servidor (RSA):", chave_publica)
            print("Chave Pública do Cliente (Diffie-Hellman):", chave_publica_cliente)
            print("Mensagem Recebida:", mensagem_decifrada)

if __name__ == "__main__":
    servidor()
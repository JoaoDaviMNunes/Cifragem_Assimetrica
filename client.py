import socket  # Biblioteca para comunicação de rede
import random  # Biblioteca para geração de números aleatórios

# Função para cifrar uma mensagem usando RSA
def cifrar_rsa(mensagem, chave_publica):
    e, n = chave_publica  # Extrai a chave pública
    # Cifra cada caractere da mensagem e retorna como lista
    return [pow(ord(caractere), e, n) for caractere in mensagem]

# Função para calcular a troca de chaves Diffie-Hellman
def troca_chave_diffie_hellman(primo, gerador, chave_privada):
    # pow (base, exp, mod)
    return pow(gerador, chave_privada, primo)  # Calcula a chave pública

# Código do cliente
def cliente():
    # Parâmetros da troca Diffie-Hellman
    primo = 999983  # Número primo de 6 dígitos usado no cálculo
    gerador = 5  # Gerador usado no cálculo
    chave_privada_cliente = random.randint(1, primo - 1)  # Chave privada do cliente
    chave_publica_cliente = troca_chave_diffie_hellman(primo, gerador, chave_privada_cliente)
    print("Chave Pública do Cliente (Diffie-Hellman):", chave_publica_cliente)

    # Configuração do socket para comunicação
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 12345))  # Conecta ao servidor

        # Recebe a chave pública RSA do servidor
        chave_publica_servidor = eval(s.recv(1024).decode())  # Decodifica a mensagem recebida
        print("Chave Pública do Servidor (RSA):", chave_publica_servidor)

        # Calcula o segredo compartilhado usando Diffie-Hellman
        segredo_compartilhado = pow(chave_publica_cliente, chave_privada_cliente, primo)
        print("Segredo Compartilhado:", segredo_compartilhado)

        # Mensagem a ser enviada ao servidor
        mensagem = "RSA e DH são os algoritmos do momento!"
        mensagem_cifrada = cifrar_rsa(mensagem, chave_publica_servidor)  # Cifra a mensagem
        print("Mensagem Cifrada Enviada:", mensagem_cifrada)

        # Envia a chave pública Diffie-Hellman e a mensagem cifrada juntas
        dados_para_enviar = f"{chave_publica_cliente}|{mensagem_cifrada}"  # Junta os dados com um separador
        s.sendall(dados_para_enviar.encode())  # Envia os dados como uma única string

        # Exibe todas as informações
        print("Chave Pública do Cliente (Diffie-Hellman):", chave_publica_cliente)
        print("Chave Pública do Servidor (RSA):", chave_publica_servidor)
        print("Mensagem Enviada:", mensagem)

if __name__ == "__main__":
    cliente()

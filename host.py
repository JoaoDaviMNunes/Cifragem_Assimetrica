# Importa as bibliotecas necessárias
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number
import random
import sys

# Função para gerar números primos (simplificação para primos pequenos)
def gerar_primo(tamanho=512):
    return number.getPrime(tamanho)

# Geração de chaves RSA
def gerar_chaves_RSA(tamanho=2048):
    print("Gerando chaves RSA...")
    chave = RSA.generate(tamanho)
    chave_privada = chave.export_key()
    chave_publica = chave.publickey().export_key()
    return chave_privada, chave_publica

# Criptografia e descriptografia RSA
def criptografar_RSA(mensagem, chave_publica):
    chave_pub = RSA.import_key(chave_publica)
    cifra = PKCS1_OAEP.new(chave_pub)
    mensagem_cifrada = cifra.encrypt(mensagem.encode())
    return mensagem_cifrada

def descriptografar_RSA(mensagem_cifrada, chave_privada):
    chave_priv = RSA.import_key(chave_privada)
    cifra = PKCS1_OAEP.new(chave_priv)
    mensagem = cifra.decrypt(mensagem_cifrada)
    return mensagem.decode()

# Troca de chaves Diffie-Hellman
def diffie_hellman():
    print("Realizando a troca de chaves Diffie-Hellman...")
    # Simplificação: primos pequenos e gerador fixo
    p = gerar_primo(512)
    g = random.randint(2, p-1)
    a = random.randint(1, p-1)
    A = pow(g, a, p)
    return p, g, a, A

def calcular_chave_compartilhada(p, g, A, b):
    B = pow(g, b, p)
    chave_compartilhada = pow(A, b, p)
    return chave_compartilhada

# Função principal
if __name__ == "__main__":
    # Geração das chaves RSA
    chave_privada, chave_publica = gerar_chaves_RSA()
    print("Chave Pública RSA:\n", chave_publica.decode())
    print("Chave Privada RSA:\n", chave_privada.decode())
    
    # Exemplo de criptografia e descriptografia RSA
    mensagem = "Mensagem secreta"
    print("Mensagem original:", mensagem)
    mensagem_cifrada = criptografar_RSA(mensagem, chave_publica)
    print("Mensagem cifrada RSA:", mensagem_cifrada)
    mensagem_decifrada = descriptografar_RSA(mensagem_cifrada, chave_privada)
    print("Mensagem decifrada RSA:", mensagem_decifrada)
    
    # Exemplo de troca de chaves Diffie-Hellman
    p, g, a, A = diffie_hellman()
    b = random.randint(1, p-1)
    chave_compartilhada = calcular_chave_compartilhada(p, g, A, b)
    print("Chave Compartilhada (Diffie-Hellman):", chave_compartilhada)

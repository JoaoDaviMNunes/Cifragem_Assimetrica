import random
from math import gcd

# === Diffie-Hellman Key Exchange ===
def diffie_hellman():
    # Simplifications: Small prime and generator for clarity
    p = 23  # Prime number (simplified for understanding)
    g = 5   # Generator (simplified for understanding)

    # Private keys (secret)
    a = int(input('DH Private Key A: '))
    b = int(input('DH Private Key B: '))

    # Public keys
    A = (g ** a) % p  # User A's public key
    B = (g ** b) % p  # User B's public key

    # Shared secret
    shared_secret_A = (B ** a) % p  # Calculated by User A
    shared_secret_B = (A ** b) % p  # Calculated by User B

    assert shared_secret_A == shared_secret_B
    print("Diffie-Hellman Key Exchange")
    print(f"Prime (p): {p}, Generator (g): {g}")
    print(f"User A Private/Public: ({a}, {A})")
    print(f"User B Private/Public: ({b}, {B})")
    print(f"Shared Secret: {shared_secret_A}\n")

# === RSA Encryption ===
def generate_rsa_keys():
    # Simplifications: Small prime numbers
    p = 61  # Prime 1 (simplified for understanding)
    q = 53  # Prime 2 (simplified for understanding)
    n = p * q  # Modulus
    phi = (p - 1) * (q - 1)  # Euler's Totient

    # Public key generation (e)
    e = 17  # Small prime coprime to phi, commonly used value

    # Private key generation (d)
    d = pow(e, -1, phi)  # Modular multiplicative inverse

    return (e, n), (d, n)  # Public and private keys

def rsa_encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

def rsa_demo():
    public_key, private_key = generate_rsa_keys()
    message = "Hello"

    ciphertext = rsa_encrypt(message, public_key)
    decrypted_message = rsa_decrypt(ciphertext, private_key)

    print("RSA Encryption")
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    print(f"Message: {message}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {decrypted_message}")

# Run implementations
diffie_hellman()
rsa_demo()

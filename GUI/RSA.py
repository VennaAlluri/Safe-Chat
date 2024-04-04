import random
import math

def is_prime(n, k=5):
    if n <= 1 or n % 2 == 0:
        return False
    if n == 2 or n == 3:
        return True

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_random_prime(bit_length=128):
    while True:
        candidate = random.getrandbits(bit_length)
        if candidate % 2 == 0:
            candidate += 1  
        if is_prime(candidate):
            return candidate

def generate_keypair():
    p = generate_random_prime()
    q=p
    while p==q :
     q = generate_random_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    d = mod_inv(e, phi)

    public_key = (n, e)
    private_key = (n, d)

    return [public_key, private_key]

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None  
    else:
        return (x % m + m) % m

def RSA_sign(digest, priv):
    n, d = priv
    signature = pow(digest, d, n)
    return signature

def RSA_decrypt(ciphertext, priv):
    decrypted_message = ""
    n, d = priv
    for i in ciphertext.split(" "):
     if i:
      decrypted_message += chr(pow(int(i), d, n))
    return decrypted_message

def RSA_verify(signature, pub):
    n, e = pub
    verified_signature = pow(signature, e, n)
    return verified_signature

def RSA_encrypt(plaintext, pub):
    encrypted_message = ""
    n, e = pub
    for i in plaintext:
     encrypted_message += str(pow(ord(i), e, n))+" "
    return encrypted_message

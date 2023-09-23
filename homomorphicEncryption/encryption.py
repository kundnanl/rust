# Import necessary modules from Cryptodome library
from Cryptodome.Util.number import *
from Cryptodome import Random
import Cryptodome
import random
import libnum
import sys
import hashlib

# Define a function to get a generator for a prime number 'p'
def get_generator(p: int):
    while True:
        # Find a generator which doesn't share factors with 'p'
        generator = random.randrange(3, p)
        # Check if the generator satisfies certain conditions
        if pow(generator, 2, p) == 1:
            continue
        if pow(generator, p, p) == 1:
            continue
        return generator

# Set default values for some variables
bits = 512  # Number of bits for prime number
v1 = 10    # Default value for v1
v2 = 5     # Default value for v2

# Check if command-line arguments are provided and update variables accordingly
if len(sys.argv) > 1:
    v1 = int(sys.argv[1])
if len(sys.argv) > 2:
    v2 = int(sys.argv[2])
if len(sys.argv) > 3:
    bits = int(sys.argv[3])

# Generate a random prime number 'p' with 'bits' number of bits
p = Cryptodome.Util.number.getPrime(bits, randfunc=Cryptodome.Random.get_random_bytes)

# Find a generator 'g' for the prime number 'p'
g = get_generator(p)

# Generate a random private key 'x' within the range (3, p)
x = random.randrange(3, p)

# Calculate the public key 'Y' using the generator 'g' and private key 'x'
Y = pow(g, x, p)

# Print information about v1, v2, public key, and private key
print(f"v1={v1}\nv2={v2}\n")
print(f"Public key:\ng={g}\nY={Y}\np={p}\n\nPrivate key\nx={x}")

# Generate random values k1 and k2 for encryption
k1 = random.randrange(3, p)
a1 = pow(g, k1, p)
b1 = (pow(Y, k1, p) * v1) % p

k2 = random.randrange(3, p)
a2 = pow(g, k2, p)
b2 = (pow(Y, k2, p) * v2) % p

# Perform homomorphic encryption for v1 and v2
a = a1 * a2
b = b1 * b2

# Print the encrypted values
print(f"\nEncrypted (v1)\na={a1}\nb={b1}")
print(f"\nEncrypted (v2)\na={a2}\nb={b2}")
print(f"\nAfter homomorphic encryption\na={a}\nb={b}")

# Calculate the result after decryption
v_r = (b * libnum.invmod(pow(a, x, p), p)) % p

# Print the result
print("\nResult: ", v_r)
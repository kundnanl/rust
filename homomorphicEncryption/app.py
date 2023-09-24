from flask import Flask, render_template, request
from Cryptodome.Util.number import *
from Cryptodome import Random
import Cryptodome
import random
import libnum
import sys
import hashlib
#hi there
app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        v1 = int(request.form["v1"])
        v2 = int(request.form["v2"])
        bits = int(request.form["bits"])

        # Generate a random prime number 'p' with 'bits' number of bits
        p = Cryptodome.Util.number.getPrime(bits, randfunc=Cryptodome.Random.get_random_bytes)

        # Find a generator 'g' for the prime number 'p'
        g = get_generator(p)

        # Generate a random private key 'x' within the range (3, p)
        x = random.randrange(3, p)

        # Calculate the public key 'Y' using the generator 'g' and private key 'x'
        Y = pow(g, x, p)

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

        # Calculate the result after decryption
        v_r = (b * libnum.invmod(pow(a, x, p), p)) % p

        return render_template("result.html", v_r=v_r)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
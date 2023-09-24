from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes

# Function to pad the input text with spaces at the end to make it a multiple of 16 bytes 
# AES blah...blah requires 16 bytes inpute data 
def pad(s):
    block_size = 16
    remainder = len(s) % block_size
    padding_needed = block_size - remainder
    return s + padding_needed * ' '


# Function to remove extra spaces at the end no loose ends remaining :)
def unpad(s):
    return s.rstrip()

# Function to encrypt plain text using AES 256 encryption 
def encrypt(plain_text, password):
    # Generate a random salt
    salt = get_random_bytes(AES.block_size)

    # Use the Scrypt KDF to derive a private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # Create a cipher configuration using AES in GCM (Galois/Counter Mode) mode
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # Encrypt the plain text and obtain the ciphertext and tag
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))

    # Return a dictionary with the encrypted text, salt, nonce, and tag
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

# Function to decrypt data using the provided encryption dictionary and password
def decrypt(enc_dict, password):
    # Decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    # Generate the private key from the password and salt using Scrypt KDF
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # Create the cipher configuration using AES in GCM mode and the provided nonce
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # Decrypt the cipher text and verify it using the provided tag
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted

# Main function
def main():
    # Prompt the user for a password
    password = input("Password: ")

    # Encrypt a sample message
    encrypted = encrypt("The secretest message here", password)
    print(encrypted)

    # Decrypt the encrypted message using the original password
    decrypted = decrypt(encrypted, password)
    print(bytes.decode(decrypted))

# Entry point of the program
if __name__ == "__main__":
    main()

    
import paramiko
import os

def xor_decrypt(file_path, xor_key):
    """
    Decrypts a file using XOR with a given key.
    
    :param file_path: Path to the encrypted file
    :param xor_key: Key for XOR operation
    :return: Decrypted content as a string
    """
    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    # XOR each byte with the key
    decrypted_data = bytearray(
        byte ^ xor_key[i % len(xor_key)]
        for i, byte in enumerate(encrypted_data)
    )
    
    return decrypted_data.decode()

def ssh_connect(host, port, username, key_data):
    """
    Connects to an SSH server using the provided key.
    
    :param host: Hostname or IP of the SSH server
    :param port: Port number for SSH
    :param username: SSH username
    :param key_data: SSH private key as string
    """
    # Load the key from the decrypted data
    private_key = paramiko.RSAKey(file_obj=key_data)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=host, port=port, username=username, pkey=private_key)
        print(f"Successfully connected to {host}:{port} as {username}")
        # You can execute commands or interact here
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Configuration
    encrypted_file_path = "akmsckm"  # Encrypted file path
    xor_key = b"randomeware"         # XOR key
    ssh_host = "example.com"         # SSH hostname or IP
    ssh_port = 2222                  # SSH port
    ssh_username = "your_username"   # SSH username
    
    # Step 1: XOR decrypt the file to get the SSH key
    try:
        decrypted_key_data = xor_decrypt(encrypted_file_path, xor_key)
        print("Decrypted SSH key successfully.")
    except Exception as e:
        print(f"Error during decryption: {e}")
        exit(1)

    # Step 2: Connect to SSH
    try:
        ssh_connect(ssh_host, ssh_port, ssh_username, decrypted_key_data)
    except Exception as e:
        print(f"SSH connection failed: {e}")

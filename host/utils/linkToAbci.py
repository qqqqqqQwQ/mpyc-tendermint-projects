from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def generate_key_pair(curve=ec.SECP256R1):
    # 生成密钥对
    private_key = ec.generate_private_key(curve(), default_backend())
    public_key = private_key.public_key()

    # 将私钥和公钥转换为 PEM 格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()


def sign_data(private_key_pem, data):
    # 将 PEM 格式的私钥加载回密钥对象
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,  # 如果有密码，请提供密码
        backend=default_backend()
    )

    # 对数据进行哈希
    hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hasher.update(data.encode())
    data_hash = hasher.finalize()

    print("Data Hash:", data_hash.hex())

    # 使用私钥对哈希值进行签名
    signature = private_key.sign(
        data_hash,
        ec.ECDSA(hashes.SHA256())
    )

    return signature.hex()


if __name__ == '__main__':
    # 调用函数生成密钥对
    private_key, public_key = generate_key_pair()
    print("私钥:", private_key)
    print("公钥:", public_key)
    # private_key="-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIKx3W4oCQwLjJaiPPULEvz6RdbUtj1JM6Leero4TUxpVoAoGCCqGSM49\nAwEHoUQDQgAEVhxXtOmaN7+qoPa9zu/9FKrpAzxNoSbiXew4gPu6GiQp2r8iIDcH\nw+kVMvwmEMc4k8o5ejEw1cvBQOsMjta8Jw==\n-----END EC PRIVATE KEY-----"
    # private_key=" -----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIAUeSJs2hC0sZdND6d68lhRsu6U5ZhdzNW7XPjljDY8EoAoGCCqGSM49\nAwEHoUQDQgAEC4gyobypz3/jhjVXiWfQR+Gk+RptrJM19uxN9f8qjA26psEjH2aM\nNOH2JSQojWRmi1kPEAkJ5Ahz7N4K49WlCQ==\n-----END EC PRIVATE KEY-----"
    data = "这就是我共享的数据"
    signature = sign_data(private_key, data)
    print("数据:", data)
    print("数字签名:", signature)

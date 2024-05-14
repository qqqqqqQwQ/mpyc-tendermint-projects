from ecdsa import VerifyingKey, BadSignatureError
import hashlib

def verify_signature(public_key_hex, data, signature_hex):
    # 将十六进制的公钥转换为 VerifyingKey 对象
    public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex))

    # 计算数据的哈希值
    data_hash = hashlib.sha256(data.encode()).digest()

    # 将十六进制的签名转换为字节串
    signature = bytes.fromhex(signature_hex)

    try:
        # 验证签名
        public_key.verify(signature, data_hash)
        return True
    except BadSignatureError:
        return False

if __name__ == '__main__':
    # 示例数据
    public_key_hex = "0383a4b26a901239c820523e622d83d479aca6c1d07a331f82690329a3f8fd946d"
    data = "这是要签名的数据"
    signature_hex = "304502202c3d171e0c7d2cb728fffc1e1eca2980389564889efa751d4a5c9c95198f3761022100c52805c724e6a6cc21f1ced24723e834c7338671dc140d713d85209ab61d929f"

    # 验证签名
    is_valid = verify_signature(public_key_hex, data, signature_hex)
    if is_valid:
        print("Signature is valid")
    else:
        print("Signature is invalid")

import base64

def decode_base64(encoded_string):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print("Error decoding Base64:", e)
        return None

if __name__ == "__main__":
    # 在这里替换你的Base64编码字符串
    encoded_string = "eyJwdWJsaWNfa2V5IjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRVZoeFh0T21hTjcrcW9QYTl6dS85RktycEF6eE5cbm9TYmlYZXc0Z1B1NkdpUXAycjhpSURjSHcra1ZNdndtRU1jNGs4bzVlakV3MWN2QlFPc01qdGE4Snc9PVxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tIiwiYW1vdW50IjoxMSwic2hhcmVsaXN0Ijoic2hhcmVSZWNvcmRzOjgyODU4MmRkLWU0ZDItNDMyYS1iMWMxLTA3ZGU5N2JlMDFkMTsifQ=="

    decoded_string = decode_base64(encoded_string)
    if decoded_string:
        print("Decoded string:", decoded_string)

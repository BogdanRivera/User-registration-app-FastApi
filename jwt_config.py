from jwt import encode, decode

def token_generate(data:dict) -> str:
    token: str = encode(payload=data,key='my_key',algorithm="HS256")
    return token

def token_validate(token:str) -> str: 
    data:dict = decode(token,key='my_key',algorithms=['HS256'])
    return data
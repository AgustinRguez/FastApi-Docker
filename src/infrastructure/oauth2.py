import json
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import date, datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from src.infrastructure.api.schemas import access_token_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def json_serial(obj):
    if isinstance(obj, (datetime, date, timedelta)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = json.dumps(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), default=json_serial)
    to_encode.update({"expiration": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded #chequear que no cumple el minuto de verificacion

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = access_token_model.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=
    "could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token=token, credentials_exception=credentials_exception)
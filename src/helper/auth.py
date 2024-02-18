
import os
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from jose import  jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

# 秘密鍵の内容を取得
def read_secret_key():
    with open(os.getenv('JWT_SECRET_KEY_PATH'), 'r') as f:
        return f.read()

SECRET_KEY = read_secret_key()
"""
SECRET_KRYはJWT（JSON Web Token）を生成するために使用されている。
これはJWTトークンを生成・検証する際に使用される秘密鍵です。
秘密鍵はトークンの署名に使用され、トークンが改ざんされていないことを保証します。
秘密鍵は安全に保管する必要があり、外部に漏れないようにする必要があります。
"""

ALGORITHM = "HS256"
"""
これはJWTの署名に使用される暗号化アルゴリズムを指定します。
HS256 はHMAC（Hash-based Message Authentication Code）を使用するSHA-256ハッシュアルゴリズムを意味します。
このアルゴリズムは、トークンの署名と検証に使われる安全な方法の一つです。
"""

ACCESS_TOKEN_EXPIRE_MINUTES = 30
"""
この値は、生成されるアクセストークンの有効期限を分単位で設定します。
この例では、トークンは生成されてから30分間有効で、その後は無効となります。
"""

# bcryptハッシュ化アルゴリズムを使用してパスワードをハッシュ化,検証するためのヘルパー関数
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/auth/token")
"""
OAuth2PasswordBearer は、FastAPIのセキュリティユーティリティの一つで、特にOAuth2のパスワードフロー（ユーザ名とパスワードを使用するフロー）に適用されます。
このクラスは、HTTPリクエストからBearerトークン（一般に「アクセストークン」と呼ばれる）を抽出するために使われます。

tokenUrl パラメータは、アクセストークンを取得するためにクライアントがリクエストを送るべきエンドポイントのURLを指定します。
この例では、トークンを取得するためのエンドポイントが /token であることを示しています。つまり、クライアントはこのURLにユーザ名とパスワードをPOSTリクエストとして送信し、応答としてアクセストークンを受け取ります。

使用方法
OAuth2PasswordBearer オブジェクトは、通常、FastAPIの依存性注入システムに組み込まれ、特定のエンドポイントがトークン(認証)を必要とする際に使用されます。
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # ここでトークンを使用した認証処理を行う
    ...
"""




def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    与えられたデータからJWT（JSON Web Token）アクセストークンを生成する関数です
    data: トークンを含むデータ
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # トークンを有効期限を設定する
    to_encode.update({"exp": expire})
    # jwtを使用して、トークンを生成
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


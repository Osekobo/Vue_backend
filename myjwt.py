from datetime import datetime, timedelta, timezone
import json
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Product, SessionLocal, User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["django_pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("access_token")

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user

# Create a helper to convert a Product object to the dictionary expected by ProductGetMap:


def product_to_response(product: Product) -> dict:
    features_list = json.loads(product.features) if product.features else []
    display_price = product.display_price or f"${product.selling_price:,.0f}"
    slug = product.slug or product.name.lower().replace(" ", "-")
    return {
        "id": product.id,
        "name": product.name,
        "buying_price": product.buying_price,
        "selling_price": product.selling_price,
        "model": product.model,
        "year": product.year,
        "condition": product.condition,
        "fuel": product.fuel,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "slug": slug,
        "subtitle": product.subtitle,
        "display_price": display_price,
        "badge": product.badge,
        "category": product.category,
        "image": product.image,
        "hero_image": product.hero_image,
        "engine": product.engine,
        "horsepower": product.horsepower,
        "top_speed": product.top_speed,
        "zero_to_sixty": product.zero_to_sixty,
        "transmission": product.transmission,
        "drivetrain": product.drivetrain,
        "description": product.description,
        "features": features_list
    }

from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional,List


class UserPostRegister(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str


class UserPostLogin(BaseModel):
    email: EmailStr
    password: str


class UserGetRegister(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr


class ProductPostMap(BaseModel):
    name: str
    buying_price: float
    selling_price: float
    model: str
    year: int
    condition: str
    fuel: str

    # ── New fields for frontend (all optional) ──
    # URL-friendly identifier (e.g., 'lamborghini-aventador')
    slug: Optional[str] = None

    # Display subtitle under car name (e.g., "V12 · 759 hp")
    subtitle: Optional[str] = None

    # Display price string (e.g., "$350,000"). If not provided, we format from selling_price.
    display_price: Optional[str] = None

    # Badge/status (e.g., "New", "Featured", "Hybrid", "Luxury")
    badge: Optional[str] = "Featured"

    # Category for filtering (e.g., "sports", "luxury", "electric", "hypercar")
    category: Optional[str] = "luxury"

    # Image URLs
    image: Optional[str] = None
    hero_image: Optional[str] = None

    # Specifications
    engine: Optional[str] = None
    horsepower: Optional[str] = None
    top_speed: Optional[str] = None
    zero_to_sixty: Optional[str] = None
    transmission: Optional[str] = None
    drivetrain: Optional[str] = None

    # Description
    description: Optional[str] = None

    # Features as a list of strings (e.g., ["Full Service History", "12-Month Warranty"])
    # Will be stored as JSON string in DB
    features: Optional[List[str]] = None
    # created_at: str


# class ProductGetMap(ProductPostMap):
    # id: int

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
import json

class ProductGetMap(BaseModel):
    id: int
    name: str
    buying_price: float
    selling_price: float
    model: str
    year: int
    condition: str
    fuel: str
    created_at: datetime
    updated_at: datetime

    slug: Optional[str] = None
    subtitle: Optional[str] = None
    display_price: Optional[str] = None
    badge: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    hero_image: Optional[str] = None
    engine: Optional[str] = None
    horsepower: Optional[str] = None
    top_speed: Optional[str] = None
    zero_to_sixty: Optional[str] = None
    transmission: Optional[str] = None
    drivetrain: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = []   # expects list, but DB gives JSON string

    @field_validator('features', mode='before')
    @classmethod
    def parse_features(cls, v):
        # If it's already a list (or None), return as is
        if v is None or isinstance(v, list):
            return v
        # If it's a JSON string, parse it
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                # Ensure it's a list of strings
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
        # Fallback: return empty list
        return []

    class Config:
        from_attributes = True  # Pydantic v2 (formerly orm_mode = True)

class RemainingPerProductMap(BaseModel):
    product_id: int
    product_name: str
    remaining_quantity: float


class SaleDetailsItem(BaseModel):
    product_id: int
    quantity: float


class SalePostMap(BaseModel):
    details: list[SaleDetailsItem]


class SaleGetMap(SalePostMap):
    id: int
    created_at: datetime
    updated_at: datetime


class SalePerProductMap(BaseModel):
    sale_id: int
    product_id: int
    quantity: float
    created_at: datetime


class PurchasePostMap(BaseModel):
    product_id: int
    quantity: float


class PurchaseGetMap(PurchasePostMap):
    id: int
    quantity: float
    product_id: int
    created_at: datetime
    updated_at: datetime

     # ── Product details (nested) ──
    product: Optional["ProductGetMap"] = None

    # ── Computed fields ──
    @property
    def total_buying_cost(self) -> float:
        if self.product:
            return self.quantity * self.product.buying_price
        return 0.0

    @property
    def total_selling_value(self) -> float:
        if self.product:
            return self.quantity * self.product.selling_price
        return 0.0

    class Config:
        from_attributes = True


class SalesPerProductOut(BaseModel):
    product_id: int
    product_name: str
    total_quantity_sold: int
    total_sales_amount: float


class RemainingPerProductOut(BaseModel):
    product_id: int
    product_name: str
    remaining_quantity: int


class ProfitPerProduct(BaseModel):
    product_id: int
    product_name: str
    total_quantity_sold: int
    total_revenue: float
    total_profit: float


class ProfitPerDay(BaseModel):
    date: date
    total_profit: float


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []


class PaymentResponse(BaseModel):
    id: int
    sale_id: str
    merchant_request_id: Optional[str] = None
    checkout_request_id: Optional[str] = None
    trans_code: str | None
    trans_amount: float | None
    phone_paid: str | None
    created_at: datetime

    class Config:
        from_attributes = True

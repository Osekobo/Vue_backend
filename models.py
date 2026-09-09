from sqlalchemy import Column, Integer, String, DateTime, Float, Text
# from database import Base
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Float, Integer, DateTime, create_engine
from typing import List
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# DATABASE_URL = "postgresql://postgres:12039@localhost:5432/vue"
# DATABASE_URL = "postgresql://postgres:12039@localhost:5432/vue"
# DATABASE_URL = "postgresql://postgres:12039@my_postgres:5432/vue"
DATABASE_URL = "postgresql://postgres:12039@postgres_database:5432/vue"
# DATABASE_URL = "sqlite:///./vue.db"

# engine = create_engine(DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)

    buying_price: Mapped[float] = mapped_column(Float, nullable=False)
    selling_price: Mapped[float] = mapped_column(Float, nullable=False)

    model: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    condition: Mapped[str] = mapped_column(String, nullable=False)
    fuel: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    purchases: Mapped[List["Purchase"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # ── NEW fields for frontend display (add these) ──
    # Used as URL-friendly identifier (e.g., 'lamborghini-aventador')
    slug: Mapped[str] = mapped_column(String(256), nullable=True, unique=True)

    # Subtitle shown under car name (e.g., "V12 · 759 hp")
    subtitle: Mapped[str] = mapped_column(String(256), nullable=True)

    # Display price on frontend (e.g., "$350,000")
    # You can derive this from selling_price, or keep as separate field
    display_price: Mapped[str] = mapped_column(String(50), nullable=True)

    # Badge/status (e.g., "New", "Featured", "Hybrid", "Luxury")
    badge: Mapped[str] = mapped_column(String(50), nullable=True)

    # Category for filtering (e.g., "sports", "luxury", "electric", "hypercar")
    category: Mapped[str] = mapped_column(String(50), nullable=True)

    # Image URLs
    # image: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(Text, nullable=True)
    hero_image: Mapped[str] = mapped_column(Text, nullable=True)
    # Specifications
    engine: Mapped[str] = mapped_column(String(100), nullable=True)
    horsepower: Mapped[str] = mapped_column(String(50), nullable=True)
    top_speed: Mapped[str] = mapped_column(String(50), nullable=True)
    zero_to_sixty: Mapped[str] = mapped_column(String(20), nullable=True)
    transmission: Mapped[str] = mapped_column(String(50), nullable=True)
    drivetrain: Mapped[str] = mapped_column(String(50), nullable=True)

    # Description
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Features as JSON array (e.g., ["Full Service History", "12-Month Warranty"])
    features: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string
    # features: Mapped[list] = mapped_column(JSON, nullable=True)


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    details: Mapped[List["SalesDetails"]] = relationship(
        back_populates="sale",
        cascade="all, delete-orphan"
    )


class SalesDetails(Base):
    __tablename__ = "sales_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    sale: Mapped["Sale"] = relationship(back_populates="details")


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # ── Relationship to Product ──
    product: Mapped["Product"] = relationship(back_populates="purchases")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    phone: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(
        String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    sale_id = Column(String)
    merchant_request_id = Column(String)
    checkout_request_id = Column(String)
    trans_code = Column(String, nullable=True)
    trans_amount = Column(Float, nullable=True)
    phone_paid = Column(String, nullable=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

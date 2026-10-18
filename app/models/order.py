from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    magnum_request_id = Column(String(128), nullable=True, index=True)
    request_type = Column(String(32), nullable=False)      # purchase | renew | action | convert
    product_code = Column(String(128), nullable=False)
    status = Column(String(64), default="queued", nullable=False, index=True)
    # reserved_pending_dispatch | queued | dispatching | succeeded | failed | failed_refunded | manual_review
    failure_reason = Column(String(128), nullable=True)
    error_id = Column(String(32), nullable=True)
    amount_deducted = Column(Float, nullable=False, default=0.0)
    related_proxy_id = Column(Integer, ForeignKey("proxies.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    proxy = relationship("Proxy", foreign_keys=[related_proxy_id])


class SystemSetting(Base):
    """Dynamic settings controlled from the admin dashboard."""
    __tablename__ = "system_settings"

    key = Column(String(128), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

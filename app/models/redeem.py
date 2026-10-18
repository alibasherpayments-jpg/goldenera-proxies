from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RedeemCode(Base):
    __tablename__ = "redeem_codes"

    id = Column(Integer, primary_key=True)
    code = Column(String(64), unique=True, nullable=False, index=True)
    code_type = Column(String(32), default="balance", nullable=False)  # "balance" | "deposit_bonus"
    reward_amount = Column(Float, nullable=False, default=0.0)         # e.g. 0.50 ($ or %)
    reward_type = Column(String(32), default="fixed", nullable=False)   # "fixed" | "percentage"
    min_deposit = Column(Float, default=0.0, nullable=False)           # Min deposit for deposit_bonus
    max_uses = Column(Integer, default=1, nullable=False)              # Max times this code can be redeemed
    used_count = Column(Integer, default=0, nullable=False)            # Times redeemed so far
    expires_at = Column(DateTime(timezone=True), nullable=True)        # Expiration datetime
    is_active = Column(Boolean, default=True, nullable=False)
    note = Column(String(256), nullable=True)                          # Description / note
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    usages = relationship("RedeemUsage", back_populates="code_obj", cascade="all, delete-orphan")


class RedeemUsage(Base):
    __tablename__ = "redeem_usages"

    id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey("redeem_codes.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reward_credited = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), default="completed", nullable=False)   # "completed" | "pending_deposit"
    used_at = Column(DateTime(timezone=True), server_default=func.now())

    code_obj = relationship("RedeemCode", back_populates="usages")
    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("code_id", "user_id", name="uq_code_user_redeem"),
    )

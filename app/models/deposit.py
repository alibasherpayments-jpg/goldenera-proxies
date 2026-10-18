from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class DepositMethod(str, enum.Enum):
    BINANCE = "binance"
    VODAFONE_CASH = "vodafone_cash"


class DepositStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"


class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    method = Column(String(32), nullable=False)            # binance | vodafone_cash
    status = Column(String(32), default="pending", nullable=False, index=True)
    txid = Column(String(256), nullable=False, unique=True, index=True)
    sender_phone = Column(String(32), nullable=True)       # Vodafone Cash: رقم المحوّل
    amount_usd = Column(Float, nullable=False)
    amount_local = Column(Float, nullable=True)            # المبلغ بالجنيه
    exchange_rate = Column(Float, nullable=True)           # سعر الصرف وقت الطلب
    admin_message_id = Column(BigInteger, nullable=True)   # رسالة الإشعار للأدمن
    admin_chat_id = Column(BigInteger, nullable=True)      # شات الأدمن الذي تلقى الإشعار
    reviewed_by = Column(BigInteger, nullable=True)        # Telegram ID of reviewing admin
    review_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="deposits")

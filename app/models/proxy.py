from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Proxy(Base):
    __tablename__ = "proxies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    request_id = Column(String(128), unique=True, nullable=False, index=True)  # Magnum request_id
    category = Column(String(32), nullable=False)          # prime | hyper | nexus | titan
    mode = Column(String(32), nullable=True)               # rotate | inject
    product_code = Column(String(128), nullable=False)
    server_id = Column(String(128), nullable=True)         # Magnum server_id
    country = Column(String(8), nullable=True)
    country_name = Column(String(128), nullable=True)
    state = Column(String(8), nullable=True)
    city = Column(String(128), nullable=True)
    provider = Column(String(256), nullable=True)
    rotation_label = Column(String(128), nullable=True)
    protocol = Column(String(16), nullable=True)           # SOCKS5 | HTTP
    host = Column(String(256), nullable=True)
    http_port = Column(Integer, nullable=True)
    socks5_port = Column(Integer, nullable=True)
    port = Column(Integer, nullable=True)
    username = Column(String(256), nullable=True)
    password = Column(String(256), nullable=True)
    allowed_ips = Column(JSON, nullable=True)              # list of IPs for inject mode
    proxy_url = Column(Text, nullable=True)
    isp = Column(String(256), nullable=True)               # TITAN ISP
    carrier = Column(String(256), nullable=True)           # NEXUS carrier
    price_paid = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, default=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    # Notifications tracking
    notified_24h = Column(Boolean, default=False)
    notified_2h = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="proxies")

    @property
    def display_location(self) -> str:
        parts = [self.country_name or self.country]
        if self.state:
            parts.append(self.state)
        if self.city:
            parts.append(self.city)
        return " — ".join(filter(None, parts))

    @property
    def flag(self) -> str:
        """Convert country code to flag emoji."""
        code = self.country or ""
        if code.upper() == "UK":
            code = "GB"
        if len(code) == 2:
            return "".join(chr(ord(c) + 127397) for c in code.upper())
        return "🌐"

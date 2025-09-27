"""
Stock model for SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Stock(Base):
    """
    株式情報を格納するテーブル
    """
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(Float)
    current_price = Column(Float)
    currency = Column(String(10), default='USD')
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Stock(symbol='{self.symbol}', company_name='{self.company_name}', price={self.current_price})>"
    
    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'sector': self.sector,
            'industry': self.industry,
            'market_cap': self.market_cap,
            'current_price': self.current_price,
            'currency': self.currency,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

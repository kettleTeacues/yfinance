"""
SQLAlchemy database client
"""
import os
from typing import Optional, Generator
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from dotenv import load_dotenv
load_dotenv()

from models import Base

class DatabaseClient:
    """SQLAlchemyデータベースクライアント"""
    
    def __init__(self, database_url: Optional[str] = None):
        """
        データベースクライアントの初期化
        
        Args:
            database_url: データベース接続URL。未指定の場合は環境変数またはデフォルト値を使用
        """
        self.database_url = os.getenv('PG_URL', '')
        self.engine = create_engine(
            self.database_url,
            echo=os.getenv('DB_ECHO', '').lower() == 'true'
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
        self.ScopedSession = scoped_session(self.SessionLocal)
        
    def _get_database_url(self) -> str:
        """データベースURLを取得"""
        # 環境変数から取得、なければSQLiteをデフォルトとして使用
        return os.getenv('DATABASE_URL', 'sqlite:///./stocks.db')
    
    def create_tables(self) -> None:
        """全てのテーブルを作成"""
        if self.engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self) -> None:
        """全てのテーブルを削除"""
        if self.engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """新しいセッションを取得"""
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self.SessionLocal()
    
    def get_scoped_session(self) -> Session:
        """スコープ付きセッションを取得（スレッドセーフ）"""
        if self.ScopedSession is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self.ScopedSession()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        セッションのコンテキストマネージャー
        自動的にcommit/rollbackを行う
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def close(self) -> None:
        """データベース接続を閉じる"""
        if self.ScopedSession:
            self.ScopedSession.remove()
        if self.engine:
            self.engine.dispose()


# グローバルインスタンス
db_client = DatabaseClient()


def get_db_client() -> DatabaseClient:
    """データベースクライアントのインスタンスを取得"""
    return db_client


def get_db_session() -> Generator[Session, None, None]:
    """
    データベースセッションを取得する依存性注入用関数
    FastAPIなどのフレームワークでの使用を想定
    """
    with db_client.session_scope() as session:
        yield session


# 便利な関数
def init_db(database_url: Optional[str] = None) -> DatabaseClient:
    """
    データベースを初期化してクライアントを返す
    
    Args:
        database_url: データベース接続URL
        
    Returns:
        初期化されたデータベースクライアント
    """
    global db_client
    if database_url:
        db_client = DatabaseClient(database_url)
    return db_client

if __name__ == '__main__':
    client = DatabaseClient()
    session = client.SessionLocal()
    table_info = session.execute(text('select * from information_schema.tables;'))
    pass

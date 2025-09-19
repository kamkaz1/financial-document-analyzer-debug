"""
Database initialization script for Financial Document Analyzer
"""

import asyncio
from .database import init_database, close_database, Base, engine

async def create_tables():
    """Create all database tables"""
    print("🔄 Initializing database...")
    
    try:
        # Initialize database connection
        await init_database()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        print("📊 Tables created:")
        print("   - users")
        print("   - analyses")
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise
    finally:
        # Close database connection
        await close_database()

if __name__ == "__main__":
    asyncio.run(create_tables())

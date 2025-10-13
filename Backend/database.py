import sqlite3
import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="playcheck.db"):
        """Initialize the database manager with the database file path."""
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # This allows us to access columns by name
            print(f"[OK] Connected to database: {self.db_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("[OK] Database connection closed")
    
    def create_tables(self):
        """Create all necessary tables for the PlayCheck AI database."""
        if not self.conn:
            print("[ERROR] No database connection. Call connect() first.")
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Create laws table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS laws (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number INTEGER UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    full_text TEXT,
                    keywords TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Check if full_text column exists in laws table (for existing databases)
            cursor.execute("PRAGMA table_info(laws)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'full_text' not in columns:
                print("[INFO] Adding full_text column to laws table...")
                cursor.execute("ALTER TABLE laws ADD COLUMN full_text TEXT")
                print("[OK] Added full_text column to laws table")
            
# Users table removed - no authentication needed
            
# Scenarios table removed - using simple frontend JavaScript instead
            
# User progress and stats tables removed - no authentication needed
            
            self.conn.commit()
            print("[OK] All tables created successfully!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error creating tables: {e}")
            return False
    
    def migrate_laws_from_json(self, json_file_path="fifa_laws.json"):
        """Migrate FIFA laws from JSON file to the database."""
        if not self.conn:
            print("[ERROR] No database connection. Call connect() first.")
            return False
        
        try:
            # Check if JSON file exists
            if not os.path.exists(json_file_path):
                print(f"[ERROR] JSON file not found: {json_file_path}")
                return False
            
            # Read JSON file
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cursor = self.conn.cursor()
            
            # Clear existing laws (in case we're re-migrating)
            cursor.execute("DELETE FROM laws")
            print("[INFO]  Cleared existing laws from database")
            
            # Insert laws from JSON
            laws = data.get('laws', [])
            for law in laws:
                cursor.execute('''
                    INSERT INTO laws (number, title, summary, full_text, keywords)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    law['number'],
                    law['title'],
                    law['summary'],
                    law.get('full_text', None),  # Will be None initially
                    json.dumps(law['keywords'])  # Store keywords as JSON string
                ))
            
            self.conn.commit()
            print(f"[OK] Successfully migrated {len(laws)} laws to database!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error migrating laws: {e}")
            return False
    
    def get_law_by_number(self, law_number):
        """Get a specific law by its number."""
        if not self.conn:
            return None
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM laws WHERE number = ?", (law_number,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            print(f"[ERROR] Error getting law: {e}")
            return None
    
    def get_all_laws(self):
        """Get all laws from the database."""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM laws ORDER BY number")
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"[ERROR] Error getting all laws: {e}")
            return []
    
    def update_law_full_text(self, law_number, full_text):
        """Update a law with its full text."""
        if not self.conn:
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE laws 
                SET full_text = ? 
                WHERE number = ?
            ''', (full_text, law_number))
            
            self.conn.commit()
            print(f"[OK] Updated Law {law_number} with full text")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error updating law {law_number}: {e}")
            return False
    
    def get_laws_without_full_text(self):
        """Get laws that don't have full text yet."""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM laws WHERE full_text IS NULL ORDER BY number")
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"[ERROR] Error getting laws without full text: {e}")
            return []
    
# Scenario functions removed - using simple frontend JavaScript instead
    
    
    def test_database(self):
        """Test the database by running some basic queries."""
        if not self.conn:
            print("[ERROR] No database connection. Call connect() first.")
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Test 1: Count laws
            cursor.execute("SELECT COUNT(*) as count FROM laws")
            law_count = cursor.fetchone()['count']
            print(f"[INFO] Total laws in database: {law_count}")
            
            # Test 2: Get first law
            cursor.execute("SELECT number, title FROM laws ORDER BY number LIMIT 1")
            first_law = cursor.fetchone()
            if first_law:
                print(f"[INFO] First law: {first_law['number']} - {first_law['title']}")
            
            # Test 3: Get law 12 (Fouls and Misconduct)
            law_12 = self.get_law_by_number(12)
            if law_12:
                print(f"[INFO] Law 12 found: {law_12['title']}")
                if law_12.get('full_text'):
                    print(f"[INFO] Law 12 has full text: {len(law_12['full_text'])} characters")
                else:
                    print(f"[INFO] Law 12 needs full text (currently summary only)")
            
            # Test 4: Check laws without full text
            laws_without_full_text = self.get_laws_without_full_text()
            print(f"[INFO] Laws needing full text: {len(laws_without_full_text)}")
            
            print("[OK] Database test completed successfully!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error testing database: {e}")
            return False

def main():
    """Main function to demonstrate database operations."""
    print("[START] Starting PlayCheck AI Database Setup...")
    
    # Create database manager
    db = DatabaseManager()
    
    # Connect to database
    if not db.connect():
        return
    
    try:
        # Create tables
        if not db.create_tables():
            return
        
        # Migrate laws from JSON
        if not db.migrate_laws_from_json():
            return
        
        # Test the database
        db.test_database()
        
        print("\n[SUCCESS] Database setup completed successfully!")
        print("[INFO] Database file created: playcheck.db")
        
    finally:
        # Always disconnect
        db.disconnect()

if __name__ == "__main__":
    main()

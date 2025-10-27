import sqlite3
import os

DATABASE_NAME = "client_tracker.db"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    
    # Create projects table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            project_name TEXT NOT NULL,
            start_date DATE NOT NULL,
            current_phase TEXT NOT NULL,
            description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create project phases table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS project_phases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            phase_name TEXT NOT NULL,
            phase_order INTEGER NOT NULL,
            completion_percentage INTEGER DEFAULT 0,
            start_date DATE,
            end_date DATE,
            notes TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    """)
    
    # Create issues table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Open',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_date TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes for better performance
    conn.execute("CREATE INDEX IF NOT EXISTS idx_project_phases_project_id ON project_phases(project_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_issues_project_id ON issues(project_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status)")
    
    conn.commit()
    conn.close()

def reset_database():
    """Reset database - useful for testing"""
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    init_database()
from database import get_db_connection
from datetime import datetime

class Project:
    def __init__(self):
        pass
    
    def create(self, client_name, project_name, start_date, current_phase, description=""):
        """Create a new project"""
        conn = get_db_connection()
        cursor = conn.execute("""
            INSERT INTO projects (client_name, project_name, start_date, current_phase, description)
            VALUES (?, ?, ?, ?, ?)
        """, (client_name, project_name, start_date, current_phase, description))
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    def get_all(self):
        """Get all projects"""
        conn = get_db_connection()
        projects = conn.execute("SELECT * FROM projects ORDER BY created_date DESC").fetchall()
        conn.close()
        return [dict(project) for project in projects]
    
    def get_by_id(self, project_id):
        """Get project by ID"""
        conn = get_db_connection()
        project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        conn.close()
        return dict(project) if project else None
    
    def update(self, project_id, client_name, project_name, start_date, current_phase, description=""):
        """Update project"""
        conn = get_db_connection()
        conn.execute("""
            UPDATE projects 
            SET client_name = ?, project_name = ?, start_date = ?, 
                current_phase = ?, description = ?, updated_date = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (client_name, project_name, start_date, current_phase, description, project_id))
        conn.commit()
        conn.close()
    
    def delete(self, project_id):
        """Delete project and related data"""
        conn = get_db_connection()
        # Delete related phases and issues (CASCADE should handle this, but being explicit)
        conn.execute("DELETE FROM project_phases WHERE project_id = ?", (project_id,))
        conn.execute("DELETE FROM issues WHERE project_id = ?", (project_id,))
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()

class ProjectPhase:
    def __init__(self):
        pass
    
    def create(self, project_id, phase_name, phase_order, completion_percentage=0):
        """Create a new project phase"""
        conn = get_db_connection()
        cursor = conn.execute("""
            INSERT INTO project_phases (project_id, phase_name, phase_order, completion_percentage)
            VALUES (?, ?, ?, ?)
        """, (project_id, phase_name, phase_order, completion_percentage))
        phase_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return phase_id
    
    def get_by_project(self, project_id):
        """Get all phases for a project"""
        conn = get_db_connection()
        phases = conn.execute("""
            SELECT * FROM project_phases 
            WHERE project_id = ? 
            ORDER BY phase_order
        """, (project_id,)).fetchall()
        conn.close()
        return [dict(phase) for phase in phases]
    
    def update_progress(self, phase_id, completion_percentage):
        """Update phase completion percentage"""
        conn = get_db_connection()
        conn.execute("""
            UPDATE project_phases 
            SET completion_percentage = ? 
            WHERE id = ?
        """, (completion_percentage, phase_id))
        conn.commit()
        conn.close()
    
    def update_dates(self, phase_id, start_date=None, end_date=None):
        """Update phase dates"""
        conn = get_db_connection()
        if start_date and end_date:
            conn.execute("""
                UPDATE project_phases 
                SET start_date = ?, end_date = ? 
                WHERE id = ?
            """, (start_date, end_date, phase_id))
        elif start_date:
            conn.execute("""
                UPDATE project_phases 
                SET start_date = ? 
                WHERE id = ?
            """, (start_date, phase_id))
        elif end_date:
            conn.execute("""
                UPDATE project_phases 
                SET end_date = ? 
                WHERE id = ?
            """, (end_date, phase_id))
        conn.commit()
        conn.close()

class Issue:
    def __init__(self):
        pass
    
    def create(self, project_id, title, description="", priority="Medium", status="Open"):
        """Create a new issue"""
        conn = get_db_connection()
        cursor = conn.execute("""
            INSERT INTO issues (project_id, title, description, priority, status)
            VALUES (?, ?, ?, ?, ?)
        """, (project_id, title, description, priority, status))
        issue_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return issue_id
    
    def get_all(self):
        """Get all issues"""
        conn = get_db_connection()
        issues = conn.execute("""
            SELECT i.*, p.client_name, p.project_name
            FROM issues i
            JOIN projects p ON i.project_id = p.id
            ORDER BY i.created_date DESC
        """).fetchall()
        conn.close()
        return [dict(issue) for issue in issues]
    
    def get_by_project(self, project_id):
        """Get all issues for a project"""
        conn = get_db_connection()
        issues = conn.execute("""
            SELECT * FROM issues 
            WHERE project_id = ? 
            ORDER BY created_date DESC
        """, (project_id,)).fetchall()
        conn.close()
        return [dict(issue) for issue in issues]
    
    def update_status(self, issue_id, status):
        """Update issue status"""
        conn = get_db_connection()
        resolved_date = datetime.now() if status == "Resolved" else None
        conn.execute("""
            UPDATE issues 
            SET status = ?, resolved_date = ?, updated_date = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, resolved_date, issue_id))
        conn.commit()
        conn.close()
    
    def update(self, issue_id, title, description, priority, status):
        """Update issue details"""
        conn = get_db_connection()
        resolved_date = datetime.now() if status == "Resolved" else None
        conn.execute("""
            UPDATE issues 
            SET title = ?, description = ?, priority = ?, status = ?, 
                resolved_date = ?, updated_date = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (title, description, priority, status, resolved_date, issue_id))
        conn.commit()
        conn.close()
    
    def delete(self, issue_id):
        """Delete issue"""
        conn = get_db_connection()
        conn.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
        conn.commit()
        conn.close()
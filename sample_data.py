from database import init_database, reset_database
from models import Project, ProjectPhase, Issue
from datetime import datetime, date, timedelta
import random

def create_sample_data():
    """Create sample data for testing the application"""
    
    # Reset database to start fresh
    reset_database()
    
    # Sample projects data
    sample_projects = [
        {
            "client_name": "TechCorp Solutions",
            "project_name": "ERP Implementation",
            "start_date": date.today() - timedelta(days=90),
            "current_phase": "Testing",
            "description": "Complete ERP system implementation with custom modules for inventory and HR management."
        },
        {
            "client_name": "Global Retail Inc",
            "project_name": "E-commerce Platform",
            "start_date": date.today() - timedelta(days=45),
            "current_phase": "Configuration",
            "description": "Multi-channel e-commerce platform with mobile app integration and payment gateway setup."
        },
        {
            "client_name": "Healthcare Partners",
            "project_name": "Patient Management System",
            "start_date": date.today() - timedelta(days=120),
            "current_phase": "Training",
            "description": "Comprehensive patient management system with appointment scheduling and billing integration."
        },
        {
            "client_name": "Manufacturing Co",
            "project_name": "Supply Chain Optimization",
            "start_date": date.today() - timedelta(days=30),
            "current_phase": "Requirement Gathering",
            "description": "Supply chain management system with real-time tracking and vendor management."
        },
        {
            "client_name": "Financial Services Ltd",
            "project_name": "Risk Management Platform",
            "start_date": date.today() - timedelta(days=150),
            "current_phase": "Deployment",
            "description": "Advanced risk assessment and management platform with regulatory compliance features."
        }
    ]
    
    # Create projects and phases
    project_ids = []
    for project_data in sample_projects:
        project = Project()
        project_id = project.create(
            project_data["client_name"],
            project_data["project_name"],
            project_data["start_date"],
            project_data["current_phase"],
            project_data["description"]
        )
        project_ids.append(project_id)
        
        # Create phases with realistic progress
        phases = [
            ("Requirement Gathering", 1),
            ("Configuration", 2),
            ("Testing", 3),
            ("Training", 4),
            ("Deployment", 5)
        ]
        
        phase_obj = ProjectPhase()
        current_phase_index = ["Requirement Gathering", "Configuration", "Testing", "Training", "Deployment"].index(project_data["current_phase"])
        
        for i, (phase_name, order) in enumerate(phases):
            if i < current_phase_index:
                # Completed phases
                completion = 100
            elif i == current_phase_index:
                # Current phase - random progress
                completion = random.randint(20, 80)
            else:
                # Future phases
                completion = 0
            
            phase_obj.create(project_id, phase_name, order, completion)
    
    # Create sample issues
    sample_issues = [
        {
            "project_id": project_ids[0],
            "title": "Database connection timeout",
            "description": "Users experiencing timeout issues when accessing large datasets",
            "priority": "High",
            "status": "In Progress"
        },
        {
            "project_id": project_ids[0],
            "title": "UI responsiveness on mobile",
            "description": "Mobile interface needs optimization for better user experience",
            "priority": "Medium",
            "status": "Open"
        },
        {
            "project_id": project_ids[1],
            "title": "Payment gateway integration",
            "description": "SSL certificate configuration needed for payment processing",
            "priority": "Critical",
            "status": "Resolved"
        },
        {
            "project_id": project_ids[1],
            "title": "Inventory sync issues",
            "description": "Product inventory not syncing properly between channels",
            "priority": "High",
            "status": "Open"
        },
        {
            "project_id": project_ids[2],
            "title": "Report generation slow",
            "description": "Monthly reports taking too long to generate",
            "priority": "Medium",
            "status": "In Progress"
        },
        {
            "project_id": project_ids[3],
            "title": "Vendor API documentation",
            "description": "Need updated API documentation from vendor",
            "priority": "Low",
            "status": "Open"
        },
        {
            "project_id": project_ids[4],
            "title": "Compliance audit requirements",
            "description": "Additional compliance features needed for audit",
            "priority": "High",
            "status": "Resolved"
        }
    ]
    
    issue_obj = Issue()
    for issue_data in sample_issues:
        issue_obj.create(
            issue_data["project_id"],
            issue_data["title"],
            issue_data["description"],
            issue_data["priority"],
            issue_data["status"]
        )
    
    print("Sample data created successfully!")
    print(f"Created {len(sample_projects)} projects with phases and {len(sample_issues)} issues.")

if __name__ == "__main__":
    create_sample_data()
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os

# Page configuration
st.set_page_config(
    page_title="Client Implementation Tracker",
    page_icon="📊",
    layout="wide"
)

# Database setup
from database import init_database, get_db_connection
from models import Project, Issue

# Initialize database
init_database()

def main():
    st.title("📊 Client Implementation Tracker")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Projects", "Issues", "Analytics"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Projects":
        show_projects()
    elif page == "Issues":
        show_issues()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    st.header("Project Dashboard")
    
    # Get all projects
    conn = get_db_connection()
    projects_df = pd.read_sql_query("""
        SELECT p.*, 
               AVG(pp.completion_percentage) as overall_progress
        FROM projects p
        LEFT JOIN project_phases pp ON p.id = pp.project_id
        GROUP BY p.id
    """, conn)
    conn.close()
    
    if projects_df.empty:
        st.info("No projects found. Add some projects in the Projects section!")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", len(projects_df))
    
    with col2:
        active_projects = len(projects_df[projects_df['overall_progress'] < 100])
        st.metric("Active Projects", active_projects)
    
    with col3:
        completed_projects = len(projects_df[projects_df['overall_progress'] >= 100])
        st.metric("Completed Projects", completed_projects)
    
    with col4:
        avg_progress = projects_df['overall_progress'].mean() if not projects_df.empty else 0
        st.metric("Average Progress", f"{avg_progress:.1f}%")
    
    # Project progress overview
    st.subheader("Project Progress Overview")
    
    for _, project in projects_df.iterrows():
        with st.expander(f"{project['client_name']} - {project['project_name']}"):
            progress = project['overall_progress'] if project['overall_progress'] else 0
            st.progress(progress / 100)
            st.write(f"Progress: {progress:.1f}%")
            st.write(f"Start Date: {project['start_date']}")
            st.write(f"Current Phase: {project['current_phase']}")

def show_projects():
    st.header("Project Management")
    
    tab1, tab2 = st.tabs(["View Projects", "Add/Edit Project"])
    
    with tab1:
        display_projects()
    
    with tab2:
        manage_project()

def display_projects():
    conn = get_db_connection()
    projects_df = pd.read_sql_query("""
        SELECT p.*, 
               AVG(pp.completion_percentage) as overall_progress
        FROM projects p
        LEFT JOIN project_phases pp ON p.id = pp.project_id
        GROUP BY p.id
    """, conn)
    conn.close()
    
    if projects_df.empty:
        st.info("No projects found.")
        return
    
    for _, project in projects_df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.subheader(f"{project['client_name']} - {project['project_name']}")
                progress = project['overall_progress'] if project['overall_progress'] else 0
                st.progress(progress / 100)
                st.write(f"Start Date: {project['start_date']}")
                st.write(f"Current Phase: {project['current_phase']}")
            
            with col2:
                if st.button(f"Edit", key=f"edit_{project['id']}"):
                    st.session_state.edit_project_id = project['id']
            
            with col3:
                if st.button(f"Delete", key=f"delete_{project['id']}"):
                    delete_project(project['id'])
                    st.rerun()
            
            # Show phase details
            show_project_phases(project['id'])
            st.divider()

def show_project_phases(project_id):
    conn = get_db_connection()
    phases_df = pd.read_sql_query("""
        SELECT * FROM project_phases 
        WHERE project_id = ? 
        ORDER BY phase_order
    """, conn, params=(project_id,))
    conn.close()
    
    if not phases_df.empty:
        st.write("**Phase Progress:**")
        for _, phase in phases_df.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{phase['phase_name']}")
                st.progress(phase['completion_percentage'] / 100)
            with col2:
                new_progress = st.slider(
                    "Progress",
                    0, 100,
                    int(phase['completion_percentage']),
                    key=f"phase_{phase['id']}",
                    label_visibility="collapsed"
                )
                if new_progress != phase['completion_percentage']:
                    update_phase_progress(phase['id'], new_progress)

def manage_project():
    # Check if editing existing project
    edit_project_id = st.session_state.get('edit_project_id', None)
    
    if edit_project_id:
        st.subheader("Edit Project")
        project_data = get_project_by_id(edit_project_id)
        if not project_data:
            st.error("Project not found!")
            return
    else:
        st.subheader("Add New Project")
        project_data = None
    
    with st.form("project_form"):
        client_name = st.text_input(
            "Client Name",
            value=project_data['client_name'] if project_data else ""
        )
        project_name = st.text_input(
            "Project Name",
            value=project_data['project_name'] if project_data else ""
        )
        start_date = st.date_input(
            "Start Date",
            value=datetime.strptime(project_data['start_date'], '%Y-%m-%d').date() if project_data else date.today()
        )
        current_phase = st.selectbox(
            "Current Phase",
            ["Requirement Gathering", "Configuration", "Testing", "Training", "Deployment"],
            index=["Requirement Gathering", "Configuration", "Testing", "Training", "Deployment"].index(project_data['current_phase']) if project_data else 0
        )
        description = st.text_area(
            "Description",
            value=project_data['description'] if project_data else ""
        )
        
        submitted = st.form_submit_button("Save Project")
        
        if submitted and client_name and project_name:
            if edit_project_id:
                update_project(edit_project_id, client_name, project_name, start_date, current_phase, description)
                st.success("Project updated successfully!")
                del st.session_state.edit_project_id
            else:
                create_project(client_name, project_name, start_date, current_phase, description)
                st.success("Project created successfully!")
            st.rerun()

def show_issues():
    st.header("Issue Management")
    
    tab1, tab2 = st.tabs(["View Issues", "Add Issue"])
    
    with tab1:
        display_issues()
    
    with tab2:
        add_issue()

def display_issues():
    conn = get_db_connection()
    issues_df = pd.read_sql_query("""
        SELECT i.*, p.client_name, p.project_name
        FROM issues i
        JOIN projects p ON i.project_id = p.id
        ORDER BY i.created_date DESC
    """, conn)
    conn.close()
    
    if issues_df.empty:
        st.info("No issues found.")
        return
    
    for _, issue in issues_df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                status_color = "🔴" if issue['status'] == "Open" else "🟡" if issue['status'] == "In Progress" else "🟢"
                st.write(f"{status_color} **{issue['title']}**")
                st.write(f"Project: {issue['client_name']} - {issue['project_name']}")
                st.write(f"Priority: {issue['priority']} | Status: {issue['status']}")
                st.write(f"Created: {issue['created_date']}")
                if issue['description']:
                    st.write(f"Description: {issue['description']}")
            
            with col2:
                new_status = st.selectbox(
                    "Status",
                    ["Open", "In Progress", "Resolved"],
                    index=["Open", "In Progress", "Resolved"].index(issue['status']),
                    key=f"status_{issue['id']}"
                )
                if new_status != issue['status']:
                    update_issue_status(issue['id'], new_status)
                    st.rerun()
            
            st.divider()

def add_issue():
    # Get projects for dropdown
    conn = get_db_connection()
    projects_df = pd.read_sql_query("SELECT id, client_name, project_name FROM projects", conn)
    conn.close()
    
    if projects_df.empty:
        st.warning("No projects available. Please add a project first.")
        return
    
    with st.form("issue_form"):
        project_options = [f"{row['client_name']} - {row['project_name']}" for _, row in projects_df.iterrows()]
        selected_project = st.selectbox("Project", project_options)
        
        title = st.text_input("Issue Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        
        submitted = st.form_submit_button("Add Issue")
        
        if submitted and title and selected_project:
            project_id = projects_df.iloc[project_options.index(selected_project)]['id']
            create_issue(project_id, title, description, priority)
            st.success("Issue added successfully!")
            st.rerun()

def show_analytics():
    st.header("Analytics & Reports")
    
    conn = get_db_connection()
    
    # Project completion chart
    projects_df = pd.read_sql_query("""
        SELECT p.client_name, p.project_name,
               AVG(pp.completion_percentage) as overall_progress
        FROM projects p
        LEFT JOIN project_phases pp ON p.id = pp.project_id
        GROUP BY p.id
    """, conn)
    
    if not projects_df.empty:
        st.subheader("Project Completion Status")
        fig = px.bar(
            projects_df,
            x='overall_progress',
            y='project_name',
            orientation='h',
            title="Project Progress Overview",
            labels={'overall_progress': 'Completion %', 'project_name': 'Project'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Phase distribution
        phases_df = pd.read_sql_query("""
            SELECT phase_name, AVG(completion_percentage) as avg_completion
            FROM project_phases
            GROUP BY phase_name
        """, conn)
        
        if not phases_df.empty:
            st.subheader("Average Phase Completion")
            fig2 = px.bar(
                phases_df,
                x='phase_name',
                y='avg_completion',
                title="Average Completion by Phase"
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    # Issues analytics
    issues_df = pd.read_sql_query("""
        SELECT status, COUNT(*) as count
        FROM issues
        GROUP BY status
    """, conn)
    
    if not issues_df.empty:
        st.subheader("Issues Status Distribution")
        fig3 = px.pie(
            issues_df,
            values='count',
            names='status',
            title="Issues by Status"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    conn.close()

# Helper functions
def create_project(client_name, project_name, start_date, current_phase, description):
    project = Project()
    project_id = project.create(client_name, project_name, start_date, current_phase, description)
    
    # Create default phases
    phases = [
        ("Requirement Gathering", 1),
        ("Configuration", 2),
        ("Testing", 3),
        ("Training", 4),
        ("Deployment", 5)
    ]
    
    conn = get_db_connection()
    for phase_name, order in phases:
        conn.execute("""
            INSERT INTO project_phases (project_id, phase_name, phase_order, completion_percentage)
            VALUES (?, ?, ?, 0)
        """, (project_id, phase_name, order))
    conn.commit()
    conn.close()

def update_project(project_id, client_name, project_name, start_date, current_phase, description):
    project = Project()
    project.update(project_id, client_name, project_name, start_date, current_phase, description)

def delete_project(project_id):
    project = Project()
    project.delete(project_id)

def get_project_by_id(project_id):
    project = Project()
    return project.get_by_id(project_id)

def update_phase_progress(phase_id, progress):
    conn = get_db_connection()
    conn.execute("""
        UPDATE project_phases 
        SET completion_percentage = ? 
        WHERE id = ?
    """, (progress, phase_id))
    conn.commit()
    conn.close()

def create_issue(project_id, title, description, priority):
    issue = Issue()
    issue.create(project_id, title, description, priority)

def update_issue_status(issue_id, status):
    issue = Issue()
    issue.update_status(issue_id, status)

if __name__ == "__main__":
    main()
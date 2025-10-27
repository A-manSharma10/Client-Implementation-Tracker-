# Client Implementation Tracker

A comprehensive Streamlit-based web application for tracking client project implementations with progress monitoring, issue management, and analytics.

## Features

### 🎯 Core Functionality
- **Project Management**: Add, edit, and delete client projects with detailed information
- **Phase Tracking**: Monitor 5 predefined implementation phases with completion percentages
- **Issue Management**: Log and track project issues with resolution status
- **Dashboard**: Real-time overview of all projects with key metrics
- **Analytics**: Visual charts and reports using Plotly

### 📊 Implementation Phases
1. **Requirement Gathering** - Initial project scoping and requirements collection
2. **Configuration** - System setup and configuration
3. **Testing** - Quality assurance and testing procedures
4. **Training** - User training and documentation
5. **Deployment** - Go-live and production deployment

### 🔧 Technical Features
- SQLite database for data persistence
- Interactive progress bars and sliders
- Real-time data visualization with Plotly
- Responsive web interface
- CRUD operations for all entities
- Data export capabilities

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone or download the project files**
   ```bash
   # If you have git
   git clone <repository-url>
   cd client-implementation-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create sample data (optional)**
   ```bash
   python sample_data.py
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - The app will automatically open in your default browser

## Usage Guide

### 🏠 Dashboard
- View key metrics: total projects, active projects, completed projects, average progress
- Quick overview of all projects with progress bars
- Real-time status updates

### 📋 Projects Section
- **View Projects**: See all projects with their current status and phase progress
- **Add New Project**: Create new client projects with all required details
- **Edit Projects**: Modify existing project information
- **Delete Projects**: Remove projects (this will also delete related phases and issues)
- **Update Phase Progress**: Use sliders to update completion percentage for each phase

### 🐛 Issues Section
- **View Issues**: See all logged issues across projects
- **Add Issues**: Create new issues with priority levels (Low, Medium, High, Critical)
- **Update Status**: Change issue status (Open, In Progress, Resolved)
- **Filter by Project**: Issues are linked to specific projects

### 📈 Analytics Section
- **Project Progress Chart**: Horizontal bar chart showing completion status
- **Phase Analysis**: Average completion by implementation phase
- **Issue Distribution**: Pie chart showing issues by status
- **Trend Analysis**: Visual insights into project performance

## Database Schema

### Projects Table
- `id`: Primary key
- `client_name`: Client organization name
- `project_name`: Project title
- `start_date`: Project start date
- `current_phase`: Current implementation phase
- `description`: Project description
- `created_date`, `updated_date`: Timestamps

### Project Phases Table
- `id`: Primary key
- `project_id`: Foreign key to projects
- `phase_name`: Name of the phase
- `phase_order`: Order of execution (1-5)
- `completion_percentage`: Progress (0-100%)
- `start_date`, `end_date`: Phase dates
- `notes`: Additional notes

### Issues Table
- `id`: Primary key
- `project_id`: Foreign key to projects
- `title`: Issue title
- `description`: Detailed description
- `priority`: Priority level (Low, Medium, High, Critical)
- `status`: Current status (Open, In Progress, Resolved)
- `created_date`, `updated_date`, `resolved_date`: Timestamps

## Sample Data

The application includes a sample data generator (`sample_data.py`) that creates:
- 5 sample projects with different clients and phases
- Realistic progress data for each phase
- 7 sample issues with various priorities and statuses

To load sample data:
```bash
python sample_data.py
```

## Chart Interpretations

### Project Progress Overview
- **Green bars (80-100%)**: Projects nearing completion
- **Yellow bars (40-79%)**: Projects in active development
- **Red bars (0-39%)**: Projects in early stages or facing delays

### Phase Completion Analysis
- Shows which phases typically take longer
- Helps identify bottlenecks in the implementation process
- Useful for resource planning and timeline estimation

### Issue Status Distribution
- **Open**: New issues requiring attention
- **In Progress**: Issues currently being worked on
- **Resolved**: Completed issues

## File Structure

```
client-implementation-tracker/
├── app.py              # Main Streamlit application
├── database.py         # Database connection and initialization
├── models.py           # Data models (Project, ProjectPhase, Issue)
├── sample_data.py      # Sample data generator
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── client_tracker.db  # SQLite database (created automatically)
```

## Customization

### Adding New Phases
To modify the implementation phases, update the phase list in:
- `app.py` in the `create_project()` function
- `sample_data.py` in the phases definition

### Changing Priority Levels
Update priority options in:
- `app.py` in the issue forms
- `models.py` in the Issue class

### Database Modifications
- Modify table schemas in `database.py`
- Update corresponding model classes in `models.py`
- Run the application to auto-create new tables

## Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database locked errors**
   - Close all instances of the app
   - Delete `client_tracker.db` and restart

3. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

4. **Charts not displaying**
   - Ensure Plotly is installed: `pip install plotly`
   - Check browser console for JavaScript errors

### Performance Tips
- For large datasets, consider adding pagination
- Use database indexes for better query performance
- Regular database maintenance for optimal performance

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Happy tracking!** 🚀
# YoDayCare

**A digital daycare management and reporting platform.**

## Overview

In many daycare institutions in Ghana, daily reports about children's activities, feeding, wellbeing, and general progress are traditionally recorded and communicated to parents using paper-based methods. While this approach serves its purpose, it can make retrieving previously issued reports inconvenient and limit parents' ability to access information about their children whenever they need it.

YoDayCare seeks to address this challenge by providing a centralised digital platform for recording, managing, and accessing daycare information. Instead of relying solely on physical reports, parents can conveniently access their children's reports, including records from previous days, while daycare staff can record and make relevant information available digitally.

The platform also provides tools for managing children, parents, staff, and other essential daycare records, bringing important daycare operations into one accessible system.

## Features

YoDayCare provides the following features:

### User and Access Management
- Role-based access for administrators, staff, and parents.
- Administrator-controlled user account creation and management.
- Access restrictions based on user roles and permissions.

### Child Management
- Register and manage children's profiles.
- Associate children with their respective parents.
- Assign children to classrooms.
- View individual child profiles and relevant information.

### Allergy Management
- Record and manage children's allergies.
- Document allergic reactions and severity levels.
- Store immediate treatment instructions for reference.

### Daily Reporting
- Create and manage daily reports for children.
- Allow parents to access their children's reports.
- Retrieve previously recorded reports for reference.

### Classroom Management
- Create and manage classrooms.
- Organise children according to their assigned classrooms.
- Associate staff members with classrooms.


## User Roles and Permissions

YoDayCare supports three main user roles, each with access to functionality relevant to their responsibilities.

** ROLES AND DESCRIPTIONS**
| **Administrators** | Have access to the entire system, including user management, child records, classroom management, and other administrative operations. |
| **Staff** | Access relevant child and classroom information and perform activities associated with their assigned responsibilities. |
| **Parents** | Access information and daily reports belonging to their registered children. |

The application implements role-based access control to protect sensitive information and prevent users from accessing records outside their permitted scope.


## Technologies Used

YoDayCare is built using the following technologies:

**TECHNOLOGIES USED**|
| **Python** | Primary programming language. |
| **Django** | Backend web framework used for application logic, routing, authentication, and database operations. |
| **SQLite** | Database used during development. |
| **HTML5** | Structures the application's web pages. |
| **CSS3** | Handles the presentation and styling of the interface. |
| **JavaScript** | Provides client-side interactivity. |
| **Bootstrap** | Supports responsive interface components and layout. |
| **Git & GitHub** | Version control and source code management. |


## Installation and Setup

Follow these steps to set up YoDayCare locally.

### Prerequisites

Ensure you have the following installed:

- Python 3.11 or later
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ykonlan/yodaycare.git
cd yodaycare
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

http://127.0.0.1:8000/

## Environment Configuration

YoDayCare uses environment-specific configuration to manage sensitive settings and application behaviour.

For local development, create a `.env` file in the project's root directory and configure the required environment variables.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

Ensure that your `.env` file is included in `.gitignore` and never commit sensitive credentials or production secrets to version control.

For production deployments, use a secure secret key and disable debug mode.

## Future Improvements

The following improvements are being considered for future versions of YoDayCare:

- **Enhanced Reporting:** Introduce more comprehensive reporting capabilities, including improved report filtering, searching, and historical report retrieval.
- **Notifications:** Implement notifications to inform parents when new daily reports are available.
- **Interactive Data Tables:** Introduce dynamic searching, sorting, and pagination to improve the experience of navigating large datasets.
- **Attendance Management:** Introduce attendance tracking and management for children.
- **Report Exporting:** Allow relevant reports and records to be exported in downloadable formats such as PDF.
- **Improved User Experience:** Continue improving the application's interface, accessibility, and responsiveness.
- **Deployment and Scalability:** Prepare the application for production deployment and explore database options beyond SQLite as the system grows.
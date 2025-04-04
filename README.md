# Project Car Manager

A Django-based web application for car enthusiasts to track, document, and manage all relevant information and expenditures related to their project cars.

## Features

- **User Authentication**: Secure registration and login system with profile management
- **Vehicle Management**: Track multiple vehicles with detailed information and images
- **Expense Tracking**: Log and categorize expenses with receipt storage
- **Maintenance Records**: Keep detailed service records
- **Maintenance Scheduling**: Set up maintenance reminders based on date or mileage
- **Dashboard**: Overview of vehicles and upcoming maintenance

## Technology Stack

- Python 3.x
- Django 5.x
- Bootstrap 5
- SQLite (default, can be configured for other databases)
- Pillow for image processing
- Crispy Forms for enhanced form rendering

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/project-car-manager.git
cd project-car-manager
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```
venv\Scripts\activate
```
- macOS/Linux:
```
source venv/bin/activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Apply migrations:
```
python manage.py migrate
```

6. Create a superuser:
```
python manage.py createsuperuser
```

7. Run the development server:
```
python manage.py runserver
```

8. Visit http://127.0.0.1:8000/ in your browser

## Usage

1. Register an account or log in
2. Add your project vehicles with details and images
3. Log expenses and maintenance records 
4. Set up maintenance schedules for routine services
5. Use the dashboard to get an overview of your vehicles

## Project Structure

- **users**: User authentication and profile management
- **vehicles**: Vehicle information and image management
- **expenses**: Expense tracking and receipt management
- **maintenance**: Service records and maintenance scheduling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django
- Bootstrap
- Font Awesome
- All contributors to the project 
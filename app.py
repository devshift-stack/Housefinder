#!/usr/bin/env python
"""
Web interface for Housefinder
Provides a simple dashboard for monitoring and controlling the system
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import sys
from datetime import datetime
import json
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import HousefinderApp
from src.utils import setup_logger

app = Flask(__name__)
logger = setup_logger(__name__)

# Global app instance
housefinder_app = None


def get_app():
    """Get or create HousefinderApp instance"""
    global housefinder_app
    if housefinder_app is None:
        try:
            housefinder_app = HousefinderApp()
        except Exception as e:
            logger.error(f"Failed to initialize HousefinderApp: {e}")
            housefinder_app = None
    return housefinder_app


@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Get system status"""
    try:
        app_instance = get_app()
        if app_instance is None:
            return jsonify({
                'status': 'error',
                'message': 'Application not initialized. Check configuration.',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        return jsonify({
            'status': 'running',
            'message': 'Housefinder is operational',
            'timestamp': datetime.now().isoformat(),
            'scrapers': len(app_instance.scrapers)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/employees')
def get_employees():
    """Get list of employees"""
    try:
        app_instance = get_app()
        if app_instance is None:
            return jsonify({'error': 'Application not initialized'}), 500
        
        employees = app_instance.sheet_reader.get_employees()
        return jsonify({
            'count': len(employees),
            'employees': [
                {
                    'name': emp.name,
                    'start_date': emp.start_date,
                    'location': emp.location,
                    'city': emp.city,
                    'urgent': emp.urgent,
                    'budget': emp.budget,
                    'num_persons': emp.num_persons
                }
                for emp in employees
            ]
        })
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/run', methods=['POST'])
def run_process():
    """Manually trigger the processing"""
    try:
        app_instance = get_app()
        if app_instance is None:
            return jsonify({'error': 'Application not initialized'}), 500
        
        # Run processing in background (simplified for demo)
        app_instance.process_all_employees()
        
        return jsonify({
            'status': 'success',
            'message': 'Processing started',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error running process: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/setup-sheets', methods=['POST'])
def setup_sheets():
    """Setup Google Sheets"""
    try:
        app_instance = get_app()
        if app_instance is None:
            return jsonify({'error': 'Application not initialized'}), 500
        
        app_instance.setup_sheets()
        return jsonify({
            'status': 'success',
            'message': 'Google Sheets setup complete'
        })
    except Exception as e:
        logger.error(f"Error setting up sheets: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Run the web server"""
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🏠 HOUSEFINDER - Web Interface                         ║
    ║                                                           ║
    ║   Version 4.0                                            ║
    ║   Step2Job GmbH                                          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Starting web server on http://{host}:{port}
    
    Access the dashboard at: http://localhost:{port}/
    
    Press Ctrl+C to stop the server
    """)
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()

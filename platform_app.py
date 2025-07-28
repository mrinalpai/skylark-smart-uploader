"""
SkylarkCloud.com Platform - Main Application
AI-Powered Business Tools Platform
"""

import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'skylarkcloud-platform-secret-key-2025')

# Platform configuration
PLATFORM_CONFIG = {
    'name': 'SkylarkCloud',
    'version': '1.0.0',
    'description': 'AI-Powered Business Tools Platform',
    'tools': [
        {
            'id': 'smart-uploader',
            'name': 'Smart Uploader',
            'description': 'AI-powered file organization for Marketing Hub',
            'icon': '📤',
            'status': 'active',
            'url': 'https://skylark-smart-uploader.el.r.appspot.com/upload',
            'category': 'Marketing'
        },
        {
            'id': 'smart-search',
            'name': 'Smart Search',
            'description': 'Intelligent file search with natural language queries',
            'icon': '🔍',
            'status': 'coming-soon',
            'url': '/tools/smart-search',
            'category': 'Marketing'
        }
    ]
}

@app.route('/')
def dashboard():
    """Platform dashboard - main landing page"""
    return render_template('dashboard.html', 
                         config=PLATFORM_CONFIG,
                         user_session=session)

@app.route('/tools')
def tools_overview():
    """Tools overview page"""
    return render_template('tools.html', 
                         config=PLATFORM_CONFIG,
                         tools=PLATFORM_CONFIG['tools'])

@app.route('/tools/smart-uploader')
def smart_uploader():
    """Smart Uploader tool - redirect to tool interface"""
    # For now, redirect to the existing uploader
    # Later we'll integrate it directly into the platform
    return render_template('smart_uploader.html', 
                         config=PLATFORM_CONFIG)

@app.route('/tools/smart-search')
def smart_search():
    """Smart Search tool - coming soon page"""
    return render_template('coming_soon.html', 
                         config=PLATFORM_CONFIG,
                         tool_name='Smart Search',
                         tool_description='Intelligent file search with natural language queries')

@app.route('/api/health')
def health_check():
    """Platform health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'skylarkcloud',
        'version': PLATFORM_CONFIG['version'],
        'timestamp': datetime.utcnow().isoformat(),
        'tools': {
            'smart_uploader': 'active',
            'smart_search': 'coming_soon'
        }
    })

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', config=PLATFORM_CONFIG)

if __name__ == '__main__':
    # Production server
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)


"""
SkylarkCloud.com - Integrated Platform
Path-based routing: / = Dashboard, /uploader = Smart Uploader v1
"""

import os
import secrets
import requests
from urllib.parse import urlencode
import base64
import json
from datetime import datetime
from flask import Flask, render_template_string, session, redirect, url_for, request, jsonify, flash
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'skylarkcloud-platform-secret-key-2025')

# Configuration from environment variables
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', "466918583342-44dugo1ikr921dr2ogkt9i6mcvh2ae0m.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', "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")
MARKETING_HUB_FOLDER_ID = os.environ.get('MARKETING_HUB_FOLDER_ID', "1FM66Jay8G6gpXsP-pLGwW64-FmqJszLa")
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
NAMING_CONVENTION_DOC_ID = os.environ.get('NAMING_CONVENTION_DOC_ID', "1IqpsMdfAjGx3H2l6SyRWcRH3red40c6AosMORn0oQes")

# Platform Dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - SkylarkCloud</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="bg-white bg-opacity-95 backdrop-blur-sm shadow-lg">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <h1 class="text-2xl font-bold text-blue-600">🚀 SkylarkCloud</h1>
                    </div>
                </div>
                <div class="flex items-center space-x-8">
                    <a href="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Dashboard</a>
                    <a href="/uploader" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Smart Uploader</a>
                    <a href="#" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">About</a>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Welcome Section -->
        <div class="bg-white bg-opacity-95 backdrop-blur-sm rounded-lg shadow-lg p-8 mb-8">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <div class="w-12 h-12 bg-red-500 rounded-lg flex items-center justify-center">
                        <span class="text-white text-xl">🎯</span>
                    </div>
                </div>
                <div class="ml-4">
                    <h2 class="text-2xl font-bold text-gray-900">Welcome to</h2>
                    <h3 class="text-3xl font-bold text-blue-600">SkylarkCloud Platform</h3>
                </div>
            </div>
            <p class="mt-4 text-lg text-gray-600">AI-Powered Business Tools Platform</p>
            <p class="text-gray-500">Transform your workflows with AI-powered tools designed for modern teams.</p>
        </div>

        <!-- Available Tools -->
        <div class="bg-white bg-opacity-95 backdrop-blur-sm rounded-lg shadow-lg p-8 mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Available Tools</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Smart Uploader -->
                <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div class="flex items-center mb-4">
                        <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-3">
                            <span class="text-white text-lg">📤</span>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-900">Smart Uploader</h3>
                            <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">Marketing</span>
                        </div>
                    </div>
                    <p class="text-gray-600 mb-4">AI-powered file organization for Marketing Hub</p>
                    
                    <div class="mt-6">
                        <a href="/uploader" 
                           class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            Launch Tool
                            <svg class="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                            </svg>
                        </a>
                    </div>
                </div>

                <!-- Smart Search -->
                <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow opacity-75">
                    <div class="flex items-center mb-4">
                        <div class="w-10 h-10 bg-gray-400 rounded-lg flex items-center justify-center mr-3">
                            <span class="text-white text-lg">🔍</span>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-900">Smart Search</h3>
                            <span class="inline-block bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full">Coming Soon</span>
                        </div>
                    </div>
                    <p class="text-gray-600 mb-4">Intelligent file search with natural language queries</p>
                    
                    <div class="mt-6">
                        <button disabled 
                                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-500 bg-gray-100 cursor-not-allowed">
                            Coming Soon
                            <svg class="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Platform Stats -->
        <div class="bg-white bg-opacity-95 backdrop-blur-sm rounded-lg shadow-lg p-8 mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Platform Overview</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="text-center">
                    <div class="text-4xl font-bold text-blue-600">1</div>
                    <div class="text-gray-600">Active Tools</div>
                </div>
                <div class="text-center">
                    <div class="text-4xl font-bold text-orange-500">1</div>
                    <div class="text-gray-600">Coming Soon</div>
                </div>
                <div class="text-center">
                    <div class="text-4xl font-bold text-green-600">2</div>
                    <div class="text-gray-600">Total Tools</div>
                </div>
            </div>
        </div>

        <!-- Call to Action -->
        <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg p-8 text-center text-white">
            <h2 class="text-2xl font-bold mb-4">Ready to get started?</h2>
            <p class="text-lg mb-6">Launch the Smart Uploader to begin organizing your files with AI.</p>
            <a href="/uploader" 
               class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Get Started
                <svg class="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                </svg>
            </a>
        </div>
    </main>

    <script>
        // Simple analytics tracking
        function trackToolClick(toolId) {
            console.log('Tool clicked:', toolId);
        }
    </script>
</body>
</html>
"""

# Smart Uploader HTML (simplified version)
UPLOADER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skylark Smart Uploader - Marketing Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="bg-white bg-opacity-95 backdrop-blur-sm shadow-lg">
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <h1 class="text-2xl font-bold text-orange-600">🚀 Skylark Smart Uploader</h1>
                    </div>
                </div>
                <div class="flex items-center space-x-8">
                    <a href="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">← Back to Dashboard</a>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="bg-white bg-opacity-95 backdrop-blur-sm rounded-lg shadow-lg p-8">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Skylark Smart Uploader</h2>
                <p class="text-lg text-gray-600">AI-Powered Marketing Hub Organization</p>
            </div>

            <!-- Features -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="flex items-center p-4 bg-orange-50 rounded-lg">
                    <div class="w-10 h-10 bg-orange-500 rounded-lg flex items-center justify-center mr-3">
                        <span class="text-white text-lg">🧠</span>
                    </div>
                    <div>
                        <h3 class="font-semibold text-gray-900">AI Analysis</h3>
                        <p class="text-sm text-gray-600">Intelligent content analysis and automatic categorization using Google's advanced AI</p>
                    </div>
                </div>

                <div class="flex items-center p-4 bg-blue-50 rounded-lg">
                    <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-3">
                        <span class="text-white text-lg">📁</span>
                    </div>
                    <div>
                        <h3 class="font-semibold text-gray-900">Smart Organization</h3>
                        <p class="text-sm text-gray-600">Automatic folder placement and filename generation following Skylark conventions</p>
                    </div>
                </div>

                <div class="flex items-center p-4 bg-green-50 rounded-lg">
                    <div class="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center mr-3">
                        <span class="text-white text-lg">📝</span>
                    </div>
                    <div>
                        <h3 class="font-semibold text-gray-900">Naming Convention</h3>
                        <p class="text-sm text-gray-600">Dynamic rule application from Google Doc</p>
                    </div>
                </div>

                <div class="flex items-center p-4 bg-purple-50 rounded-lg">
                    <div class="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center mr-3">
                        <span class="text-white text-lg">⚡</span>
                    </div>
                    <div>
                        <h3 class="font-semibold text-gray-900">Performance</h3>
                        <p class="text-sm text-gray-600">Version-based caching and optimized processing</p>
                    </div>
                </div>
            </div>

            <!-- Google Sign In -->
            <div class="text-center">
                {% if 'credentials' in session %}
                    <div class="mb-6">
                        <p class="text-green-600 mb-4">✅ Signed in as {{ session.get('user_email', 'User') }}</p>
                        <a href="/uploader/logout" class="text-blue-600 hover:text-blue-800">Sign out</a>
                    </div>
                    
                    <!-- File Upload Area -->
                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-6">
                        <div class="text-center">
                            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                            </svg>
                            <div class="mt-4">
                                <label for="file-upload" class="cursor-pointer">
                                    <span class="mt-2 block text-sm font-medium text-gray-900">
                                        Drop files here or click to upload
                                    </span>
                                    <input id="file-upload" name="file-upload" type="file" class="sr-only" multiple>
                                </label>
                                <p class="mt-1 text-xs text-gray-500">
                                    PNG, JPG, PDF, DOC, DOCX up to 10MB each
                                </p>
                            </div>
                        </div>
                    </div>

                    <button id="upload-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg disabled:opacity-50" disabled>
                        Upload and Organize Files
                    </button>
                {% else %}
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-blue-900 mb-4">Continue with Google</h3>
                        <p class="text-blue-700 mb-6">Sign in with your Google account to access the Smart Uploader and organize files in your Marketing Hub.</p>
                        <a href="/uploader/auth" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
                                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                            </svg>
                            Continue with Google
                        </a>
                    </div>
                {% endif %}
            </div>
        </div>
    </main>

    <script>
        // File upload handling
        const fileInput = document.getElementById('file-upload');
        const uploadBtn = document.getElementById('upload-btn');
        
        if (fileInput) {
            fileInput.addEventListener('change', function(e) {
                uploadBtn.disabled = e.target.files.length === 0;
            });
        }
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def dashboard():
    """Platform dashboard - main landing page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/uploader')
def smart_uploader():
    """Smart Uploader tool page"""
    return render_template_string(UPLOADER_HTML)

@app.route('/uploader/auth')
def auth():
    """Google OAuth authentication"""
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode({
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': request.url_root + 'uploader/callback',
        'scope': 'openid email profile https://www.googleapis.com/auth/drive',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    })}"
    return redirect(auth_url)

@app.route('/uploader/callback')
def callback():
    """OAuth callback handler"""
    code = request.args.get('code')
    if not code:
        flash('Authentication failed', 'error')
        return redirect('/uploader')
    
    # Exchange code for tokens
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': request.url_root + 'uploader/callback'
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        tokens = response.json()
        
        if 'access_token' in tokens:
            session['credentials'] = tokens
            
            # Get user info
            user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={tokens['access_token']}"
            user_response = requests.get(user_info_url)
            user_data = user_response.json()
            session['user_email'] = user_data.get('email')
            
            flash('Successfully signed in!', 'success')
        else:
            flash('Authentication failed', 'error')
    except Exception as e:
        flash(f'Authentication error: {str(e)}', 'error')
    
    return redirect('/uploader')

@app.route('/uploader/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('Successfully signed out', 'info')
    return redirect('/uploader')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'platform': 'skylarkcloud',
        'status': 'healthy',
        'version': '1.0.0',
        'architecture': 'path-based-routing',
        'tools': {
            'dashboard': 'active',
            'smart_uploader': 'active',
            'smart_search': 'coming_soon'
        }
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)


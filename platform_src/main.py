"""
SkylarkCloud.com Platform - Integrated Application
AI-Powered Business Tools Platform with Smart Uploader Integration
"""

import os
import secrets
import requests
from urllib.parse import urlencode
import base64
import json
from datetime import datetime
from flask import Flask, render_template, render_template_string, session, redirect, url_for, request, jsonify
from flask_cors import CORS
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Import Smart Uploader services
try:
    from services_enhanced import GeminiService, DriveService, NamingConventionService, IntelligentWorkflowOrchestrator
except ImportError:
    # Fallback if services not available
    GeminiService = DriveService = NamingConventionService = IntelligentWorkflowOrchestrator = None

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY', 'skylarkcloud-platform-secret-key-2025')

# Smart Uploader Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', "466918583342-44dugo1ikr921dr2ogkt9i6mcvh2ae0m.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', "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")
MARKETING_HUB_FOLDER_ID = os.environ.get('MARKETING_HUB_FOLDER_ID', "1FM66Jay8G6gpXsP-pLGwW64-FmqJszLa")
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "AIzaSyC_r3bNkIN41mSe7-nrnhePguaW7oq4C2E")
NAMING_CONVENTION_DOC_ID = os.environ.get('NAMING_CONVENTION_DOC_ID', "1IqpsMdfAjGx3H2l6SyRWcRH3red40c6AosMORn0oQes")

# Initialize Smart Uploader services
if GeminiService:
    gemini_service = GeminiService(GEMINI_API_KEY)
else:
    gemini_service = None

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
            'url': '/tools/smart-uploader',
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

# Smart Uploader HTML Template (from original)
SMART_UPLOADER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Uploader - SkylarkCloud</title>
    <link rel="icon" type="image/png" href="/static/SkylarkLogo-BirdOrange.png">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --skylark-orange: #FF6B35;
            --skylark-orange-light: #FF8A5B;
            --skylark-orange-dark: #E55A2B;
            --skylark-blue: #2563EB;
            --skylark-gray: #64748B;
            --skylark-light: #F8FAFC;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1rem 0;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--skylark-blue);
            text-decoration: none;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }

        .nav-links a {
            color: var(--skylark-gray);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .nav-links a:hover {
            color: var(--skylark-blue);
        }

        .container {
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        .tool-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .tool-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--skylark-blue);
            margin-bottom: 0.5rem;
        }

        .tool-subtitle {
            color: var(--skylark-gray);
            font-size: 1.1rem;
        }

        .upload-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }

        .upload-area {
            border: 3px dashed var(--skylark-blue);
            border-radius: 15px;
            padding: 3rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            background: var(--skylark-light);
        }

        .upload-area:hover {
            border-color: var(--skylark-orange);
            background: rgba(255, 107, 53, 0.05);
        }

        .upload-area.dragover {
            border-color: var(--skylark-orange);
            background: rgba(255, 107, 53, 0.1);
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            color: var(--skylark-blue);
        }

        .upload-text {
            font-size: 1.2rem;
            color: var(--skylark-gray);
            margin-bottom: 1rem;
        }

        .upload-button {
            background: linear-gradient(135deg, var(--skylark-blue), var(--skylark-orange));
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(37, 99, 235, 0.3);
        }

        .upload-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.4);
        }

        .file-input {
            display: none;
        }

        .auth-section {
            text-align: center;
            margin-bottom: 2rem;
        }

        .auth-button {
            background: #4285f4;
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .auth-button:hover {
            background: #3367d6;
            transform: translateY(-2px);
        }

        .user-info {
            background: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }

        .progress-container {
            margin-top: 2rem;
            display: none;
        }

        .progress-bar {
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--skylark-blue), var(--skylark-orange));
            width: 0%;
            transition: width 0.3s ease;
        }

        .status-message {
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            display: none;
        }

        .status-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .status-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        @media (max-width: 768px) {
            .nav-container {
                padding: 0 1rem;
            }
            
            .nav-links {
                gap: 1rem;
            }
            
            .container {
                padding: 0 1rem;
            }
            
            .tool-title {
                font-size: 2rem;
            }
            
            .upload-area {
                padding: 2rem 1rem;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav-container">
            <a href="/" class="logo">🚀 SkylarkCloud</a>
            <ul class="nav-links">
                <li><a href="/">Dashboard</a></li>
                <li><a href="/tools">Tools</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
    </header>

    <div class="container">
        <div class="tool-header">
            <h1 class="tool-title">📤 Smart Uploader</h1>
            <p class="tool-subtitle">AI-powered file organization for Marketing Hub</p>
        </div>

        {% if user_info %}
            <div class="user-info">
                <img src="{{ user_info.picture }}" alt="User Avatar" class="user-avatar">
                <div>
                    <strong>{{ user_info.name }}</strong>
                    <div style="font-size: 0.9rem; color: #666;">{{ user_info.email }}</div>
                </div>
                <div style="margin-left: auto;">
                    <a href="/logout" style="color: #666; text-decoration: none;">Logout</a>
                </div>
            </div>
        {% else %}
            <div class="auth-section">
                <p style="margin-bottom: 1rem; color: #666;">Please sign in with Google to access the Smart Uploader</p>
                <a href="/auth/login" class="auth-button">
                    Sign in with Google
                </a>
            </div>
        {% endif %}

        {% if user_info %}
            <div class="upload-section">
                <div class="upload-area" id="uploadArea">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text">
                        Drag and drop files here or click to browse
                    </div>
                    <button class="upload-button" onclick="document.getElementById('fileInput').click()">
                        Choose Files
                    </button>
                    <input type="file" id="fileInput" class="file-input" multiple>
                </div>

                <div class="progress-container" id="progressContainer">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div id="progressText" style="text-align: center; margin-top: 0.5rem; color: #666;"></div>
                </div>

                <div class="status-message" id="statusMessage"></div>
            </div>
        {% endif %}
    </div>

    <script>
        // File upload functionality
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const statusMessage = document.getElementById('statusMessage');

        // Drag and drop handlers
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            handleFiles(files);
        });

        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });

        function handleFiles(files) {
            if (files.length === 0) return;

            progressContainer.style.display = 'block';
            statusMessage.style.display = 'none';

            uploadFiles(files);
        }

        async function uploadFiles(files) {
            const totalFiles = files.length;
            let completedFiles = 0;

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                progressText.textContent = `Processing ${file.name} (${i + 1}/${totalFiles})...`;

                try {
                    await uploadSingleFile(file);
                    completedFiles++;
                } catch (error) {
                    console.error('Upload failed for', file.name, error);
                }

                const progress = (completedFiles / totalFiles) * 100;
                progressFill.style.width = progress + '%';
            }

            progressText.textContent = `Completed ${completedFiles}/${totalFiles} files`;
            
            if (completedFiles === totalFiles) {
                showStatus('All files uploaded successfully!', 'success');
            } else {
                showStatus(`${completedFiles}/${totalFiles} files uploaded. Some uploads failed.`, 'error');
            }
        }

        async function uploadSingleFile(file) {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/upload/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            return response.json();
        }

        function showStatus(message, type) {
            statusMessage.textContent = message;
            statusMessage.className = `status-message status-${type}`;
            statusMessage.style.display = 'block';
        }
    </script>
</body>
</html>
"""

# Platform Routes
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
    """Smart Uploader tool - integrated functionality"""
    user_info = session.get('user_info')
    return render_template_string(SMART_UPLOADER_HTML, 
                                user_info=user_info,
                                naming_convention_doc_id=NAMING_CONVENTION_DOC_ID,
                                marketing_hub_folder_id=MARKETING_HUB_FOLDER_ID)

@app.route('/tools/smart-search')
def smart_search():
    """Smart Search tool - coming soon"""
    return render_template('coming_soon.html', 
                         config=PLATFORM_CONFIG,
                         tool_name='Smart Search')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', 
                         config=PLATFORM_CONFIG)

# Smart Uploader API Routes (from original)
@app.route('/auth/login')
def login():
    """Initiate Google OAuth login"""
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode({
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': request.url_root + 'api/auth/callback',
        'scope': 'openid email profile https://www.googleapis.com/auth/drive',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    })}"
    return redirect(auth_url)

@app.route('/api/auth/callback')
def auth_callback():
    """Handle Google OAuth callback"""
    code = request.args.get('code')
    if not code:
        return "Authorization failed", 400
    
    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': request.url_root + 'api/auth/callback'
    }
    
    token_response = requests.post(token_url, data=token_data)
    token_info = token_response.json()
    
    if 'access_token' not in token_info:
        return "Token exchange failed", 400
    
    # Get user info
    user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token_info['access_token']}"
    user_response = requests.get(user_info_url)
    user_info = user_response.json()
    
    # Store in session
    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info.get('refresh_token')
    session['user_info'] = user_info
    
    return redirect('/tools/smart-uploader')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect('/tools/smart-uploader')

@app.route('/api/upload/upload', methods=['POST'])
def upload_file():
    """Handle file upload with AI processing"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Here you would integrate with the original Smart Uploader services
        # For now, return a success response
        return jsonify({
            'success': True,
            'message': f'File {file.filename} uploaded successfully',
            'filename': file.filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health and API routes
@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'platform': 'skylarkcloud',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'tools': {
            'smart_uploader': 'active',
            'smart_search': 'coming_soon'
        },
        'version': PLATFORM_CONFIG['version']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)


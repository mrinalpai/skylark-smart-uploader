"""
SkylarkCloud.com Platform - Simple Dashboard
Minimal platform with working Launch Tool button
"""

import os
from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'skylarkcloud-platform-secret-key-2025')

# Simple HTML template for the platform dashboard
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
                    <a href="#" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">Tools</a>
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
                        <a href="https://smartuploader.skylarkcloud.com" 
                           target="_blank"
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
            <a href="https://smartuploader.skylarkcloud.com" 
               target="_blank"
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

@app.route('/')
def dashboard():
    """Platform dashboard - main landing page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'platform': 'skylarkcloud',
        'status': 'healthy',
        'version': '1.0.0',
        'tools': {
            'smart_uploader': 'active',
            'smart_search': 'coming_soon'
        }
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)


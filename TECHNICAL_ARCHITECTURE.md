# Technical Architecture - Skylark Smart Uploader Platform

## 🏗️ **System Architecture Overview**

### **Current State: Smart Uploader v1.0**
```
┌─────────────────────────────────────────────────────────┐
│                Smart Uploader v1.0                     │
├─────────────────────────────────────────────────────────┤
│  Web Interface (Flask)                                 │
│  ├── File Upload UI                                    │
│  ├── Progress Tracking                                 │
│  ├── Authentication (Google OAuth)                     │
│  └── Results Display                                   │
├─────────────────────────────────────────────────────────┤
│  Backend Services                                      │
│  ├── GeminiService (AI Analysis)                       │
│  ├── DriveService (Google Drive Integration)           │
│  ├── NamingConventionService (Dynamic Rules)           │
│  └── IntelligentWorkflowService (Orchestration)        │
├─────────────────────────────────────────────────────────┤
│  External APIs                                         │
│  ├── Google Gemini 2.5 Pro (Content Analysis)         │
│  ├── Google Drive API (File Operations)                │
│  ├── Google Docs API (Naming Convention)               │
│  └── Google OAuth 2.0 (Authentication)                 │
└─────────────────────────────────────────────────────────┘
```

### **Future State: skylarkcloud.com Platform**
```
┌─────────────────────────────────────────────────────────┐
│                SkylarkCloud Platform                    │
├─────────────────────────────────────────────────────────┤
│  Platform Dashboard                                    │
│  ├── Unified Navigation                                │
│  ├── User Management                                   │
│  ├── Analytics Overview                                │
│  └── Tool Launcher                                     │
├─────────────────────────────────────────────────────────┤
│  Marketing Tools                                       │
│  ├── Smart Uploader (/marketing/uploader)              │
│  └── Smart Search (/marketing/search)                  │
├─────────────────────────────────────────────────────────┤
│  Shared Platform Services                              │
│  ├── Authentication Service                            │
│  ├── File Index Service                                │
│  ├── AI Service (Gemini Integration)                   │
│  ├── Analytics Service                                 │
│  └── Notification Service                              │
├─────────────────────────────────────────────────────────┤
│  Data Layer                                            │
│  ├── File Index Database                               │
│  ├── User Activity Database                            │
│  ├── Configuration Storage                             │
│  └── Cache Layer                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 **Component Details**

### **1. Smart Uploader Service**

#### **Core Components**
```python
# Main Flask Application
class SmartUploaderApp:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.drive_service = DriveService()
        self.naming_service = NamingConventionService()
        self.workflow_service = IntelligentWorkflowService()

# AI Analysis Service
class GeminiService:
    def analyze_file_content(self, file_content, file_type):
        """Analyze file content using Gemini 2.5 Pro"""
        
    def extract_metadata(self, analysis_result):
        """Extract structured metadata from AI analysis"""
        
    def recommend_folder(self, metadata, folder_structure):
        """Recommend optimal folder placement"""

# Google Drive Integration
class DriveService:
    def upload_file(self, file_data, target_folder, filename):
        """Upload file to Google Drive"""
        
    def get_folder_structure(self, root_folder_id):
        """Retrieve Marketing Hub folder structure"""
        
    def find_folder_by_path(self, folder_path):
        """Find folder by hierarchical path"""

# Dynamic Naming Convention
class NamingConventionService:
    def __init__(self):
        self._cached_rules = None
        self._cache_timestamp = None
        
    def get_naming_rules(self):
        """Get naming rules with version-based caching"""
        
    def apply_naming_convention(self, filename, metadata):
        """Apply naming rules to generate proper filename"""
```

#### **Data Flow**
```
1. File Upload
   ├── User selects file
   ├── File validation (size, type)
   ├── Upload to temporary storage
   └── Trigger analysis workflow

2. AI Analysis
   ├── Extract file content (PDF, DOCX, PPTX)
   ├── Send to Gemini API for analysis
   ├── Parse AI response for metadata
   └── Generate folder recommendation

3. Organization
   ├── Apply naming convention rules
   ├── Find target folder in Drive
   ├── Upload file to final location
   └── Return success confirmation

4. User Feedback
   ├── Display analysis results
   ├── Show final file location
   ├── Provide download/preview links
   └── Suggest related actions
```

### **2. Smart Search Service (Planned)**

#### **Architecture Components**
```python
# Search Interface
class SmartSearchApp:
    def __init__(self):
        self.search_service = SearchService()
        self.ai_service = AIService()
        self.index_service = FileIndexService()

# File Indexing System
class FileIndexService:
    def scan_marketing_hub(self):
        """Scan all files and build searchable index"""
        
    def extract_content_summary(self, file):
        """Generate AI summary of file content"""
        
    def build_search_vectors(self, content):
        """Create semantic search embeddings"""
        
    def update_index(self, file_metadata):
        """Update index when new files are uploaded"""

# Search Intelligence
class SearchService:
    def understand_query(self, user_query):
        """Use AI to parse search intent"""
        
    def search_files(self, parsed_query):
        """Execute semantic and keyword search"""
        
    def rank_results(self, results, query_context):
        """AI-powered result ranking"""
        
    def generate_suggestions(self, query, results):
        """Provide related search suggestions"""

# Chat Interface Handler
class ChatInterface:
    def process_message(self, user_message):
        """Handle natural language search queries"""
        
    def format_results(self, search_results):
        """Format results for chat-like display"""
        
    def handle_follow_up(self, previous_context, new_query):
        """Manage conversation context"""
```

#### **Search Data Flow**
```
1. Query Processing
   ├── User enters natural language query
   ├── AI parses intent and parameters
   ├── Extract search criteria (type, topic, date)
   └── Generate search strategy

2. File Matching
   ├── Semantic search using embeddings
   ├── Keyword matching in metadata
   ├── Folder path filtering
   └── Content similarity scoring

3. Result Ranking
   ├── Relevance scoring (AI-powered)
   ├── Recency weighting
   ├── User activity patterns
   └── File popularity metrics

4. Response Generation
   ├── Format results with previews
   ├── Generate explanations
   ├── Suggest related searches
   └── Provide action buttons
```

---

## 🗄️ **Database Design**

### **File Index Schema**
```sql
-- Main file index for search
CREATE TABLE file_index (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id VARCHAR(255) UNIQUE NOT NULL,     -- Google Drive file ID
    filename VARCHAR(500) NOT NULL,
    original_filename VARCHAR(500),
    content_summary TEXT,                     -- AI-generated summary
    content_type VARCHAR(100),                -- document, presentation, etc.
    folder_path VARCHAR(1000),                -- Full folder hierarchy
    folder_id VARCHAR(255),                   -- Google Drive folder ID
    file_type VARCHAR(50),                    -- pdf, docx, pptx, etc.
    file_size BIGINT,                         -- File size in bytes
    created_by VARCHAR(255),                  -- User email
    created_date TIMESTAMP DEFAULT NOW(),
    modified_date TIMESTAMP DEFAULT NOW(),
    upload_source VARCHAR(100),               -- 'smart_uploader', 'manual'
    tags JSONB,                              -- Extracted tags and metadata
    search_vector VECTOR(1536),              -- Semantic search embeddings
    confidence_score FLOAT,                  -- AI analysis confidence
    
    -- Indexes for performance
    INDEX idx_file_id (file_id),
    INDEX idx_filename (filename),
    INDEX idx_folder_path (folder_path),
    INDEX idx_created_by (created_by),
    INDEX idx_created_date (created_date),
    INDEX idx_content_type (content_type),
    INDEX idx_search_vector USING ivfflat (search_vector)
);

-- User activity tracking
CREATE TABLE user_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email VARCHAR(255) NOT NULL,
    tool_name VARCHAR(100) NOT NULL,          -- 'uploader', 'search', 'dashboard'
    action VARCHAR(100) NOT NULL,             -- 'upload', 'search', 'download', 'view'
    target_file_id VARCHAR(255),              -- Related file if applicable
    query_text TEXT,                          -- Search query if applicable
    result_count INTEGER,                     -- Number of results returned
    session_id VARCHAR(255),                  -- User session identifier
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB,                          -- Additional context data
    
    -- Indexes
    INDEX idx_user_email (user_email),
    INDEX idx_tool_name (tool_name),
    INDEX idx_timestamp (timestamp),
    INDEX idx_session_id (session_id)
);

-- Platform configuration
CREATE TABLE platform_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT NOW(),
    modified_date TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_config_key (config_key)
);

-- Search analytics
CREATE TABLE search_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text TEXT NOT NULL,
    user_email VARCHAR(255),
    result_count INTEGER,
    click_through_rate FLOAT,
    avg_result_position FLOAT,
    search_date TIMESTAMP DEFAULT NOW(),
    response_time_ms INTEGER,
    
    INDEX idx_query_text (query_text),
    INDEX idx_search_date (search_date),
    INDEX idx_user_email (user_email)
);
```

### **Caching Strategy**
```python
# Redis cache configuration
CACHE_CONFIG = {
    'naming_convention_rules': {
        'ttl': 3600,  # 1 hour
        'key_pattern': 'naming_rules:{doc_version}'
    },
    'folder_structure': {
        'ttl': 1800,  # 30 minutes
        'key_pattern': 'folders:{folder_id}'
    },
    'search_results': {
        'ttl': 300,   # 5 minutes
        'key_pattern': 'search:{query_hash}'
    },
    'user_sessions': {
        'ttl': 86400, # 24 hours
        'key_pattern': 'session:{user_email}'
    }
}
```

---

## 🔐 **Security Architecture**

### **Authentication Flow**
```
1. User Access
   ├── User visits skylarkcloud.com
   ├── Check for existing session
   ├── Redirect to Google OAuth if needed
   └── Validate permissions

2. OAuth Process
   ├── Google OAuth 2.0 authorization
   ├── Receive authorization code
   ├── Exchange for access/refresh tokens
   └── Store tokens securely

3. Token Management
   ├── Automatic token refresh
   ├── Session persistence
   ├── Secure token storage
   └── Graceful expiration handling

4. Authorization
   ├── Check user permissions
   ├── Validate folder access
   ├── Enforce rate limits
   └── Audit access attempts
```

### **Security Measures**
```python
# Security configuration
SECURITY_CONFIG = {
    'session_timeout': 86400,        # 24 hours
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'allowed_file_types': ['.pdf', '.docx', '.pptx', '.xlsx', '.jpg', '.png'],
    'rate_limits': {
        'uploads': '10/hour',
        'searches': '100/hour',
        'api_calls': '1000/hour'
    },
    'cors_origins': ['skylarkcloud.com', '*.skylarkcloud.com'],
    'csrf_protection': True,
    'secure_headers': True
}

# Input validation
class SecurityValidator:
    def validate_file_upload(self, file):
        """Validate file type, size, and content"""
        
    def sanitize_search_query(self, query):
        """Sanitize user search input"""
        
    def validate_folder_access(self, user, folder_id):
        """Check user permissions for folder access"""
```

---

## 📊 **Performance Architecture**

### **Optimization Strategies**
```python
# Performance configuration
PERFORMANCE_CONFIG = {
    'file_processing': {
        'max_concurrent_uploads': 5,
        'chunk_size': 1024 * 1024,  # 1MB chunks
        'timeout': 300,             # 5 minutes
    },
    'ai_processing': {
        'batch_size': 10,
        'max_tokens': 50000,
        'timeout': 120,             # 2 minutes
    },
    'search_performance': {
        'max_results': 50,
        'cache_duration': 300,      # 5 minutes
        'index_refresh': 3600,      # 1 hour
    }
}

# Async processing
class AsyncProcessor:
    def process_file_upload(self, file_data):
        """Process file upload asynchronously"""
        
    def update_search_index(self, file_metadata):
        """Update search index in background"""
        
    def generate_analytics(self, time_period):
        """Generate usage analytics asynchronously"""
```

### **Monitoring & Alerting**
```python
# Monitoring configuration
MONITORING_CONFIG = {
    'health_checks': {
        'interval': 60,             # 1 minute
        'timeout': 10,              # 10 seconds
        'endpoints': ['/health', '/api/status']
    },
    'performance_metrics': {
        'response_time_threshold': 2000,  # 2 seconds
        'error_rate_threshold': 0.01,     # 1%
        'uptime_target': 0.999            # 99.9%
    },
    'alerts': {
        'email_recipients': ['admin@skylarkdrones.com'],
        'slack_webhook': 'https://hooks.slack.com/...',
        'escalation_delay': 300           # 5 minutes
    }
}
```

---

## 🚀 **Deployment Architecture**

### **Google Cloud Platform Setup**
```yaml
# App Engine configuration (app.yaml)
runtime: python311
service: default

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

env_variables:
  GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
  GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}
  GEMINI_API_KEY: ${GEMINI_API_KEY}
  MARKETING_HUB_FOLDER_ID: ${MARKETING_HUB_FOLDER_ID}
  NAMING_CONVENTION_DOC_ID: ${NAMING_CONVENTION_DOC_ID}
  DATABASE_URL: ${DATABASE_URL}
  REDIS_URL: ${REDIS_URL}

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto
```

### **Infrastructure Components**
```
Google Cloud Platform:
├── App Engine (Web Application)
├── Cloud SQL (PostgreSQL Database)
├── Cloud Storage (File Processing)
├── Cloud Memorystore (Redis Cache)
├── Cloud Monitoring (Observability)
├── Cloud Logging (Log Management)
└── Cloud IAM (Access Control)

External Services:
├── Google Drive API (File Storage)
├── Google Docs API (Configuration)
├── Google Gemini API (AI Processing)
└── Google OAuth 2.0 (Authentication)
```

### **CI/CD Pipeline**
```yaml
# GitHub Actions workflow
name: Deploy to Google App Engine

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/
    - name: Deploy to App Engine
      uses: google-github-actions/deploy-appengine@v0
      with:
        credentials: ${{ secrets.GCP_SA_KEY }}
```

---

## 🔧 **API Design**

### **RESTful API Endpoints**
```python
# Platform APIs
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Initiate OAuth login flow"""

@app.route('/api/auth/callback', methods=['GET'])
def auth_callback():
    """Handle OAuth callback"""

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user and clear session"""

# Upload APIs
@app.route('/api/upload/analyze', methods=['POST'])
def analyze_file():
    """Analyze uploaded file content"""

@app.route('/api/upload/organize', methods=['POST'])
def organize_file():
    """Organize file in Marketing Hub"""

# Search APIs
@app.route('/api/search/query', methods=['POST'])
def search_files():
    """Execute natural language search"""

@app.route('/api/search/suggestions', methods=['GET'])
def get_suggestions():
    """Get search suggestions"""

# Analytics APIs
@app.route('/api/analytics/usage', methods=['GET'])
def get_usage_analytics():
    """Get platform usage statistics"""

@app.route('/api/analytics/files', methods=['GET'])
def get_file_analytics():
    """Get file organization statistics"""

# Health & Monitoring
@app.route('/health', methods=['GET'])
def health_check():
    """System health check"""

@app.route('/api/status', methods=['GET'])
def system_status():
    """Detailed system status"""
```

### **WebSocket Integration**
```python
# Real-time updates
@socketio.on('upload_progress')
def handle_upload_progress(data):
    """Send real-time upload progress"""

@socketio.on('search_typing')
def handle_search_typing(data):
    """Handle search-as-you-type"""

@socketio.on('file_preview')
def handle_file_preview(data):
    """Stream file preview data"""
```

---

This technical architecture provides a solid foundation for both the current Smart Uploader and the future skylarkcloud.com platform, ensuring scalability, maintainability, and excellent user experience.


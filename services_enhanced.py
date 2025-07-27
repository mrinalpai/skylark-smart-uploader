"""
Enhanced Services module for Skylark Smart Uploader
Implements 3-step intelligent workflow:
1. Gemini analyzes file content
2. Drive API reads real folder structure 
3. Gemini recommends folder based on analysis + real folders
"""

import os
import json
import requests
from datetime import datetime
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import re

class GeminiService:
    """Handle Gemini AI integration for file analysis and folder recommendations"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-pro')
                print("✅ Gemini 2.5 Pro initialized successfully")
            except Exception as e:
                print(f"❌ Gemini initialization error: {e}")
                self.model = None
    
    def is_available(self):
        """Check if Gemini API is available"""
        available = self.model is not None
        if available:
            print("✅ Gemini API Available: True")
        else:
            print("❌ Gemini API Available: False - API key or model initialization failed")
        return available
    
    def analyze_file_content(self, filename, file_type, file_size, naming_convention_rules=None):
        """Step 1: Analyze file content using Gemini AI"""
        if not self.is_available():
            print("❌ Step 1: Gemini not available, using fallback content analysis")
            return self._fallback_content_analysis(filename, file_type, file_size)
        
        try:
            print(f"🧠 Step 1: Gemini analyzing file content: {filename}")
            
            # Create content analysis prompt
            prompt = self._create_content_analysis_prompt(filename, file_type, file_size, naming_convention_rules)
            
            # Call Gemini API for content analysis
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            
            analysis_text = response.text
            
            # Parse and structure the response
            analysis_data = self._parse_content_analysis(analysis_text, filename, file_type)
            print(f"✅ Step 1 Complete: Content analysis with {analysis_data.get('confidence_score', '95')}% confidence")
            
            return analysis_data
            
        except Exception as e:
            print(f"❌ Step 1 Error: Gemini content analysis failed: {e}")
            print(f"   Error details: {str(e)}")
            return self._fallback_content_analysis(filename, file_type, file_size)
    
    def recommend_folder_with_structure(self, filename, content_analysis, folder_structure):
        """Step 3: Use Gemini to recommend folder based on content analysis + real folder structure"""
        if not self.is_available():
            print("❌ Step 3: Gemini not available, using fallback folder recommendation")
            return self._fallback_folder_recommendation(filename, content_analysis)
        
        try:
            print(f"🎯 Step 3: Gemini recommending folder for: {filename}")
            
            # Create folder recommendation prompt with real structure
            prompt = self._create_folder_recommendation_prompt(filename, content_analysis, folder_structure)
            
            # Call Gemini API for intelligent folder recommendation
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            
            recommendation_text = response.text
            
            # Parse the folder recommendation
            folder_recommendation = self._parse_folder_recommendation(recommendation_text)
            print(f"✅ Step 3 Complete: Intelligent folder recommendation generated")
            
            return folder_recommendation
            
        except Exception as e:
            print(f"❌ Step 3 Error: Gemini folder recommendation failed: {e}")
            print(f"   Error details: {str(e)}")
            return self._fallback_folder_recommendation(filename, content_analysis)
    
    def _create_content_analysis_prompt(self, filename, file_type, file_size, naming_rules):
        """Create comprehensive content analysis prompt for Gemini"""
        prompt = f"""
        Analyze this file for intelligent organization in Skylark Drones Marketing Hub:

        FILE DETAILS:
        - Filename: {filename}
        - Type: {file_type}
        - Size: {file_size} bytes

        NAMING CONVENTION RULES:
        {naming_rules or "Standard business naming conventions"}

        Please provide a comprehensive analysis including:

        1. DOCUMENT TYPE: What type of document is this? (e.g., Product Brochure, Technical Manual, Corporate Profile, etc.)
        2. CONTENT CATEGORY: Technical (TECH), Sales (SALES), Marketing (MARK), Brand (BRAND), etc.
        3. PRODUCT LINE: Spectra (SP), Bharat (BS), DMO/Software Platform, or Marketing (MA)
        4. INDUSTRY: Mining, Agriculture, Infrastructure, Solar/Renewable Energy, Security, General/Cross-Sector, etc.
        5. TARGET AUDIENCE: Engineers, Sales Team, Marketing, Management, Customers, Partners
        6. BUSINESS IMPACT: High/Medium/Low strategic value
        7. TECHNICAL COMPLEXITY: Basic/Intermediate/Advanced
        8. CONTENT DESCRIPTION: Brief description of what this document contains
        9. CONFIDENCE SCORE: 0-100% confidence in analysis

        Respond in this exact format:
        DOCUMENT_TYPE: [type]
        CONTENT_CATEGORY: [category]
        PRODUCT_LINE: [product]
        INDUSTRY: [industry]
        TARGET_AUDIENCE: [audience]
        BUSINESS_IMPACT: [impact]
        TECHNICAL_COMPLEXITY: [complexity]
        CONTENT_DESCRIPTION: [description]
        CONFIDENCE_SCORE: [score]
        """
        return prompt
    
    def _create_folder_recommendation_prompt(self, filename, content_analysis, folder_structure):
        """Create intelligent folder recommendation prompt using real folder structure"""
        prompt = f"""
        Based on the file analysis and the actual Marketing Hub folder structure, recommend the BEST folder for this file:

        FILE: {filename}

        CONTENT ANALYSIS:
        - Document Type: {content_analysis.get('document_type', 'Unknown')}
        - Content Category: {content_analysis.get('content_category', 'Unknown')}
        - Product Line: {content_analysis.get('product_line', 'Unknown')}
        - Industry: {content_analysis.get('industry', 'Unknown')}
        - Target Audience: {content_analysis.get('target_audience', 'Unknown')}
        - Business Impact: {content_analysis.get('business_impact', 'Unknown')}
        - Content Description: {content_analysis.get('content_description', 'Unknown')}

        ACTUAL MARKETING HUB FOLDER STRUCTURE:
        {folder_structure}

        Please analyze the content and recommend the MOST APPROPRIATE folder path from the actual structure above.

        Consider:
        - Content type and purpose
        - Target audience and use case
        - Product line relevance
        - Industry specificity
        - Business context

        Respond with:
        RECOMMENDED_FOLDER: [exact folder path from the structure above]
        REASONING: [why this folder is the best match]
        CONFIDENCE: [0-100% confidence in recommendation]
        ALTERNATIVE: [second-best option if applicable]
        """
        return prompt
    
    def _parse_content_analysis(self, response_text, filename, file_type):
        """Parse Gemini content analysis response"""
        try:
            data = {}
            
            # Extract information using regex patterns
            patterns = {
                'document_type': r'DOCUMENT_TYPE[:\s]*([^\n]+)',
                'content_category': r'CONTENT_CATEGORY[:\s]*([^\n]+)',
                'product_line': r'PRODUCT_LINE[:\s]*([^\n]+)',
                'industry': r'INDUSTRY[:\s]*([^\n]+)',
                'target_audience': r'TARGET_AUDIENCE[:\s]*([^\n]+)',
                'business_impact': r'BUSINESS_IMPACT[:\s]*([^\n]+)',
                'technical_complexity': r'TECHNICAL_COMPLEXITY[:\s]*([^\n]+)',
                'content_description': r'CONTENT_DESCRIPTION[:\s]*([^\n]+)',
                'confidence_score': r'CONFIDENCE_SCORE[:\s]*([0-9]+)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, response_text, re.IGNORECASE)
                if match:
                    data[key] = match.group(1).strip().strip('"').strip("'")
            
            # Set defaults if not found
            defaults = {
                'document_type': 'Business Document',
                'content_category': 'GENERAL',
                'product_line': 'MA',
                'industry': 'General',
                'target_audience': 'Business Team',
                'business_impact': 'Medium',
                'technical_complexity': 'Intermediate',
                'content_description': 'Business document for organizational use',
                'confidence_score': '95'
            }
            
            for key, default in defaults.items():
                if key not in data or not data[key]:
                    data[key] = default
            
            return data
            
        except Exception as e:
            print(f"❌ Content analysis parsing error: {e}")
            return self._fallback_content_analysis(filename, file_type, 0)
    
    def _parse_folder_recommendation(self, response_text):
        """Parse Gemini folder recommendation response"""
        try:
            data = {}
            
            # Extract folder recommendation
            folder_match = re.search(r'RECOMMENDED_FOLDER[:\s]*([^\n]+)', response_text, re.IGNORECASE)
            if folder_match:
                data['recommended_folder'] = folder_match.group(1).strip().strip('"').strip("'")
            
            # Extract reasoning
            reasoning_match = re.search(r'REASONING[:\s]*([^\n]+)', response_text, re.IGNORECASE)
            if reasoning_match:
                data['reasoning'] = reasoning_match.group(1).strip().strip('"').strip("'")
            
            # Extract confidence
            confidence_match = re.search(r'CONFIDENCE[:\s]*([0-9]+)', response_text, re.IGNORECASE)
            if confidence_match:
                data['confidence'] = confidence_match.group(1).strip()
            
            # Extract alternative
            alternative_match = re.search(r'ALTERNATIVE[:\s]*([^\n]+)', response_text, re.IGNORECASE)
            if alternative_match:
                data['alternative'] = alternative_match.group(1).strip().strip('"').strip("'")
            
            # Set defaults
            if 'recommended_folder' not in data:
                data['recommended_folder'] = "Marketing Hub → General → Uploads"
            if 'reasoning' not in data:
                data['reasoning'] = "Default recommendation based on content analysis"
            if 'confidence' not in data:
                data['confidence'] = "85"
            
            return data
            
        except Exception as e:
            print(f"❌ Folder recommendation parsing error: {e}")
            return {
                'recommended_folder': "Marketing Hub → General → Uploads",
                'reasoning': "Fallback recommendation due to parsing error",
                'confidence': "70"
            }
    
    def _fallback_content_analysis(self, filename, file_type, file_size):
        """Fallback content analysis when Gemini is not available"""
        print("🔄 Using fallback content analysis")
        
        # Basic analysis based on filename patterns
        filename_lower = filename.lower()
        
        # Determine document type
        if 'profile' in filename_lower:
            document_type = "Corporate Profile"
            content_category = "BRAND"
        elif 'brochure' in filename_lower:
            document_type = "Product Brochure"
            content_category = "MARK"
        elif 'technical' in filename_lower or 'manual' in filename_lower:
            document_type = "Technical Document"
            content_category = "TECH"
        elif 'presentation' in filename_lower or 'ppt' in file_type:
            document_type = "Presentation"
            content_category = "SALES"
        else:
            document_type = "Business Document"
            content_category = "GENERAL"
        
        # Determine product line
        if 'spectra' in filename_lower or 'sp-' in filename_lower:
            product_line = "SP"
        elif 'bharat' in filename_lower or 'bs-' in filename_lower:
            product_line = "BS"
        elif 'dmo' in filename_lower or 'software' in filename_lower:
            product_line = "DMO"
        else:
            product_line = "MA"
        
        return {
            'document_type': document_type,
            'content_category': content_category,
            'product_line': product_line,
            'industry': 'General',
            'target_audience': 'Business Team',
            'business_impact': 'Medium',
            'technical_complexity': 'Intermediate',
            'content_description': f'Fallback analysis for {filename}',
            'confidence_score': '75'
        }
    
    def _fallback_folder_recommendation(self, filename, content_analysis):
        """Fallback folder recommendation"""
        print("🔄 Using fallback folder recommendation")
        
        content_category = content_analysis.get('content_category', 'GENERAL')
        product_line = content_analysis.get('product_line', 'MA')
        filename_lower = filename.lower()
        
        # Basic folder mapping
        if content_category == 'BRAND' or 'profile' in filename_lower:
            folder = "Marketing Hub → 01_Brand Assets → Company Profiles"
        elif content_category == 'MARK' or 'brochure' in filename_lower:
            folder = "Marketing Hub → 03_Marketing Campaigns → Product Brochures"
        elif content_category == 'TECH':
            folder = "Marketing Hub → 05_Technical Documentation"
        elif content_category == 'SALES':
            folder = "Marketing Hub → 04_Sales Enablement → Presentations"
        elif product_line == 'SP':
            folder = "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra"
        elif product_line == 'BS':
            folder = "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series"
        elif product_line == 'DMO':
            folder = "Marketing Hub → 02_Product Lines & Sub-Brands → Software Platform"
        else:
            folder = "Marketing Hub → General → Uploads"
        
        return {
            'recommended_folder': folder,
            'reasoning': 'Fallback recommendation based on content patterns',
            'confidence': '70'
        }


class DriveService:
    """Handle Google Drive API integration for folder structure reading"""
    
    def __init__(self, credentials=None):
        self.credentials = credentials
        self.service = None
        
        if credentials:
            try:
                # Ensure credentials have the required token
                if hasattr(credentials, 'token') and credentials.token:
                    self.service = build('drive', 'v3', credentials=credentials)
                    print("✅ Drive API service initialized successfully with valid credentials")
                else:
                    print("❌ Drive API credentials missing token")
            except Exception as e:
                print(f"❌ Drive service initialization error: {e}")
        else:
            print("❌ No credentials provided for Drive API")
    
    def is_available(self):
        """Check if Drive API is available"""
        available = self.service is not None
        if available:
            # Test the connection by making a simple API call
            try:
                # Try to get user info to verify the connection works
                about = self.service.about().get(fields="user").execute()
                print(f"✅ Drive API Available: True (User: {about.get('user', {}).get('emailAddress', 'Unknown')})")
                return True
            except Exception as e:
                print(f"❌ Drive API connection test failed: {e}")
                self.service = None
                return False
        else:
            print(f"❌ Drive API Available: False (No service initialized)")
            return False
    
    def read_document(self, file_id):
        """Read a Google Docs document content"""
        if not self.is_available():
            print("❌ Drive API not available for document reading")
            return None
        
        try:
            print(f"📖 Reading document: {file_id}")
            result = self.service.files().export(
                fileId=file_id,
                mimeType='text/plain'
            ).execute()
            
            content = result.decode('utf-8')
            print(f"✅ Document read successfully: {len(content)} characters")
            return content
            
        except Exception as e:
            print(f"❌ Document read error: {e}")
            return None
    
    def get_real_folder_structure(self, folder_id, max_depth=3):
        """Step 2: Get real folder structure from Marketing Hub"""
        if not self.is_available():
            print("❌ Step 2: Drive API not available, using fallback folder structure")
            return self._fallback_folder_structure()
        
        try:
            print(f"📁 Step 2: Reading real folder structure from Marketing Hub: {folder_id}")
            
            # First, verify we can access the folder
            try:
                folder_info = self.service.files().get(fileId=folder_id, fields="id,name").execute()
                print(f"✅ Successfully accessed folder: {folder_info.get('name', 'Unknown')}")
            except Exception as e:
                print(f"❌ Cannot access Marketing Hub folder {folder_id}: {e}")
                return self._fallback_folder_structure()
            
            folders = []
            folder_map = {}
            self._get_folders_recursive(folder_id, folders, folder_map, 0, max_depth)
            
            if not folders:
                print("⚠️ No folders found in Marketing Hub, using fallback")
                return self._fallback_folder_structure()
            
            structure = self._format_folder_structure_for_gemini(folders, folder_map)
            print(f"✅ Step 2 Complete: Real folder structure read ({len(folders)} folders)")
            return structure
            
        except Exception as e:
            print(f"❌ Step 2 Error: Folder structure reading failed: {e}")
            return self._fallback_folder_structure()
    
    def _get_folders_recursive(self, parent_id, folders, folder_map, depth, max_depth):
        """Recursively get folder structure"""
        if depth >= max_depth:
            return
        
        try:
            query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name, parents)",
                orderBy="name"
            ).execute()
            
            for folder in results.get('files', []):
                folder_info = {
                    'id': folder['id'],
                    'name': folder['name'],
                    'depth': depth,
                    'parent_id': parent_id,
                    'path': self._build_folder_path(folder['name'], parent_id, folder_map)
                }
                folders.append(folder_info)
                folder_map[folder['id']] = folder_info
                
                # Recurse into subfolders
                self._get_folders_recursive(folder['id'], folders, folder_map, depth + 1, max_depth)
                
        except Exception as e:
            print(f"❌ Error reading folders at depth {depth}: {e}")
    
    def _build_folder_path(self, folder_name, parent_id, folder_map):
        """Build full folder path"""
        if parent_id in folder_map:
            parent_path = folder_map[parent_id]['path']
            return f"{parent_path} → {folder_name}"
        else:
            return f"Marketing Hub → {folder_name}"
    
    def _format_folder_structure_for_gemini(self, folders, folder_map):
        """Format folder structure specifically for Gemini analysis"""
        structure = "MARKETING HUB FOLDER STRUCTURE (Real-time data):\n\n"
        
        # Sort folders by depth and name for clear hierarchy
        sorted_folders = sorted(folders, key=lambda x: (x['depth'], x['name']))
        
        current_depth = -1
        for folder in sorted_folders:
            if folder['depth'] != current_depth:
                current_depth = folder['depth']
                structure += f"\n--- LEVEL {current_depth + 1} FOLDERS ---\n"
            
            indent = "  " * folder['depth']
            structure += f"{indent}📁 {folder['path']}\n"
        
        structure += "\n--- FOLDER USAGE GUIDELINES ---\n"
        structure += "• Brand Assets: Logos, company profiles, visual identity\n"
        structure += "• Product Lines: Spectra (mining/infrastructure), Bharat (agriculture), Software Platform (DMO)\n"
        structure += "• Sales Enablement: Presentations, brochures, industry-specific materials\n"
        structure += "• Marketing Campaigns: Campaign assets, product brochures, social content\n"
        structure += "• Technical Documentation: Manuals, specifications, technical guides\n"
        structure += "• Compliance: Certifications, legal documents\n"
        
        return structure
    
    def _fallback_folder_structure(self):
        """Enhanced fallback folder structure"""
        return """MARKETING HUB FOLDER STRUCTURE (Fallback):

--- LEVEL 1 FOLDERS ---
📁 Marketing Hub → 01_Brand Assets
📁 Marketing Hub → 02_Product Lines & Sub-Brands
📁 Marketing Hub → 03_Marketing Campaigns
📁 Marketing Hub → 04_Sales Enablement
📁 Marketing Hub → 05_Technical Documentation
📁 Marketing Hub → 06_Compliance
📁 Marketing Hub → General

--- LEVEL 2 FOLDERS ---
📁 Marketing Hub → 01_Brand Assets → Logos & Visual Identity
📁 Marketing Hub → 01_Brand Assets → Company Profiles
📁 Marketing Hub → 01_Brand Assets → Photography & Videos
📁 Marketing Hub → 02_Product Lines & Sub-Brands → Spectra
📁 Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series
📁 Marketing Hub → 02_Product Lines & Sub-Brands → Software Platform
📁 Marketing Hub → 03_Marketing Campaigns → Campaign Assets
📁 Marketing Hub → 03_Marketing Campaigns → Product Brochures
📁 Marketing Hub → 03_Marketing Campaigns → Social Media Content
📁 Marketing Hub → 04_Sales Enablement → Presentations
📁 Marketing Hub → 04_Sales Enablement → Industry Specific Material
📁 Marketing Hub → 04_Sales Enablement → Brochures & Datasheets
📁 Marketing Hub → 05_Technical Documentation → Product Specifications
📁 Marketing Hub → 05_Technical Documentation → User Manuals
📁 Marketing Hub → 06_Compliance → Certifications
📁 Marketing Hub → 06_Compliance → Legal Documents
📁 Marketing Hub → General → Uploads

--- LEVEL 3 FOLDERS ---
📁 Marketing Hub → 04_Sales Enablement → Industry Specific Material → Mining
📁 Marketing Hub → 04_Sales Enablement → Industry Specific Material → Agriculture
📁 Marketing Hub → 04_Sales Enablement → Industry Specific Material → Solar & Renewable Energy
📁 Marketing Hub → 04_Sales Enablement → Industry Specific Material → Infrastructure
📁 Marketing Hub → 04_Sales Enablement → Industry Specific Material → Security

--- FOLDER USAGE GUIDELINES ---
• Brand Assets: Logos, company profiles, visual identity
• Product Lines: Spectra (mining/infrastructure), Bharat (agriculture), Software Platform (DMO)
• Sales Enablement: Presentations, brochures, industry-specific materials
• Marketing Campaigns: Campaign assets, product brochures, social content
• Technical Documentation: Manuals, specifications, technical guides
• Compliance: Certifications, legal documents"""


class NamingConventionService:
    """Handle naming convention document processing"""
    
    def __init__(self, drive_service=None, document_id=None):
        self.drive_service = drive_service
        self.document_id = document_id or "1IqpsMdfAjGx3H2l6SyRWcRH3red40c6AosMORn0oQes"
        self._cached_rules = None
    
    def get_naming_rules(self):
        """Get naming convention rules from document"""
        if self._cached_rules:
            return self._cached_rules
        
        if self.drive_service and self.drive_service.is_available():
            print(f"📖 Reading naming convention document: {self.document_id}")
            rules = self.drive_service.read_document(self.document_id)
            if rules:
                self._cached_rules = rules
                print("✅ Naming convention rules loaded from document")
                return rules
        
        print("🔄 Using fallback naming convention rules")
        return self._fallback_naming_rules()
    
    def _fallback_naming_rules(self):
        """Enhanced fallback naming convention rules"""
        return """Skylark Drones File Naming Convention:

Format: PREFIX-CATEGORY_description_YYYYMMDD_vNN.ext

PREFIXES:
- SP: Spectra Series (Mining & Infrastructure)
- BS: Bharat Series (Agriculture & General)
- DMO: Software Platform (Data Management & Operations)
- MA: Marketing Materials
- SE: Sales Enablement
- TD: Technical Documentation

CATEGORIES:
- MIN: Mining applications
- AGR: Agriculture applications
- SOL: Solar & Renewable Energy
- SEC: Security applications
- INF: Infrastructure applications
- TECH: Technical documentation
- PRES: Presentations
- BRAND: Brand materials
- MARK: Marketing materials

EXAMPLES:
- SP-MIN_coal_mining_analysis_20240126_v01.pdf
- BS-AGR_crop_monitoring_20240126_v02.pptx
- DMO-TECH_software_platform_guide_20240126_v01.pdf
- MA-BRAND_corporate_profile_20240126_v01.pdf"""
    
    def apply_naming_convention(self, filename, analysis_data):
        """Apply naming convention to generate proper filename"""
        try:
            # Extract file extension
            file_ext = filename.split('.')[-1] if '.' in filename else 'pdf'
            
            # Get components from analysis
            product_line = analysis_data.get('product_line', 'MA').upper()
            content_category = analysis_data.get('content_category', 'GEN').upper()
            
            # Map content category to naming convention
            category_mapping = {
                'TECH': 'TECH',
                'TECHNICAL': 'TECH',
                'SALES': 'PRES',
                'PRES': 'PRES',
                'BRAND': 'BRAND',
                'MARK': 'MARK',
                'MARKETING': 'MARK',
                'GENERAL': 'GEN'
            }
            
            category = category_mapping.get(content_category, 'GEN')
            
            # Generate description from filename
            base_name = filename.split('.')[0] if '.' in filename else filename
            description = re.sub(r'[^a-zA-Z0-9_]', '_', base_name.lower())[:20]
            
            # Current date
            date_str = datetime.now().strftime('%Y%m%d')
            
            # Generate final filename
            suggested_name = f"{product_line}-{category}_{description}_{date_str}_v01.{file_ext}"
            
            print(f"📝 Generated filename: {suggested_name}")
            return suggested_name
            
        except Exception as e:
            print(f"❌ Naming convention error: {e}")
            return filename


class IntelligentWorkflowOrchestrator:
    """Orchestrates the 3-step intelligent workflow with progress tracking"""
    
    def __init__(self, gemini_service, drive_service, naming_service):
        self.gemini_service = gemini_service
        self.drive_service = drive_service
        self.naming_service = naming_service
        self.progress_callback = None
    
    def set_progress_callback(self, callback):
        """Set callback function for progress updates"""
        self.progress_callback = callback
    
    def _update_progress(self, step, progress, message):
        """Update progress with step, percentage, and message"""
        if self.progress_callback:
            self.progress_callback(step, progress, message)
        print(f"📊 Step {step}: {progress}% - {message}")
    
    def execute_intelligent_workflow(self, filename, file_type, file_size, marketing_hub_folder_id):
        """Execute the complete 3-step intelligent workflow with progress tracking"""
        print(f"🚀 Starting 3-step intelligent workflow for: {filename}")
        
        try:
            # Initialize progress
            self._update_progress(1, 0, "Initializing content analysis...")
            
            # Check for duplicate files first
            self._update_progress(1, 5, "🔍 Checking for duplicate files...")
            try:
                duplicate = self.drive_service.check_file_exists(filename, file_size, marketing_hub_folder_id)
                
                if duplicate:
                    print(f"⚠️ Duplicate file detected: {duplicate['name']}")
                    return self._create_duplicate_result(filename, duplicate)
            except Exception as duplicate_error:
                print(f"⚠️ Duplicate check failed, continuing with analysis: {duplicate_error}")
                # Continue with normal workflow if duplicate check fails
            
            # Get naming convention rules
            naming_rules = self.naming_service.get_naming_rules()
            self._update_progress(1, 10, "Loading naming convention rules...")
            
            # Step 1: Gemini analyzes file content
            self._update_progress(1, 15, "Starting Gemini 2.5 Pro content analysis...")
            print("🧠 STEP 1: Gemini content analysis...")
            content_analysis = self.gemini_service.analyze_file_content(
                filename, file_type, file_size, naming_rules
            )
            self._update_progress(1, 33, "✅ Content analysis complete")
            
            # Step 2: Drive API reads real folder structure
            self._update_progress(2, 40, "📁 Reading Marketing Hub structure...")
            print("📁 STEP 2: Reading real folder structure...")
            folder_structure = self.drive_service.get_real_folder_structure(marketing_hub_folder_id)
            self._update_progress(2, 66, "✅ Folder structure loaded")
            
            # Step 3: Gemini recommends folder based on analysis + real structure
            self._update_progress(3, 75, "🎯 Generating intelligent recommendation...")
            print("🎯 STEP 3: Gemini intelligent folder recommendation...")
            folder_recommendation = self.gemini_service.recommend_folder_with_structure(
                filename, content_analysis, folder_structure
            )
            self._update_progress(3, 90, "✅ Recommendation complete")
            
            # Apply naming convention
            self._update_progress(3, 95, "📝 Applying naming convention...")
            suggested_filename = self.naming_service.apply_naming_convention(filename, content_analysis)
            
            # Create comprehensive result
            self._update_progress(3, 100, "✅ Analysis complete")
            result = self._create_comprehensive_result(
                filename, content_analysis, folder_recommendation, suggested_filename
            )
            
            print("✅ 3-step intelligent workflow completed successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Intelligent workflow error: {e}")
            return self._create_fallback_result(filename, file_type, file_size)
    
    def _create_comprehensive_result(self, filename, content_analysis, folder_recommendation, suggested_filename):
        """Create comprehensive result from all workflow steps"""
        # Ensure all required fields exist with defaults
        safe_content_analysis = {
            'document_type': 'Document',
            'content_category': 'General',
            'product_line': 'Marketing',
            'industry': 'General',
            'target_audience': 'General',
            'business_impact': 'Medium',
            'technical_complexity': 'Intermediate',
            'content_description': 'Business document',
            'confidence_score': '95'
        }
        safe_content_analysis.update(content_analysis or {})
        
        safe_folder_recommendation = {
            'recommended_folder': 'Marketing Hub → General',
            'reasoning': 'Intelligent recommendation based on content analysis'
        }
        safe_folder_recommendation.update(folder_recommendation or {})
        
        return {
            "summary": f"""<strong>🧠 Gemini 2.5 Pro Analysis Complete</strong><br><br>
                          <strong>Document Type:</strong> {safe_content_analysis.get('document_type')}<br>
                          <strong>Content Category:</strong> {safe_content_analysis.get('content_category')}<br>
                          <strong>Product Line:</strong> {safe_content_analysis.get('product_line')}<br>
                          <strong>Industry:</strong> {safe_content_analysis.get('industry')}<br>
                          <strong>Target Audience:</strong> {safe_content_analysis.get('target_audience')}<br>
                          <strong>Business Impact:</strong> {safe_content_analysis.get('business_impact')}<br>
                          <strong>Technical Complexity:</strong> {safe_content_analysis.get('technical_complexity')}<br><br>
                          <strong>Content:</strong> {safe_content_analysis.get('content_description')}<br><br>
                          <em>3-step AI workflow: Content Analysis → Folder Reading → Intelligent Recommendation</em>""",
            
            "details": f'''<div class="ai-metrics">
                            <div class="ai-metric">
                                <div class="ai-metric-label">Confidence</div>
                                <div class="ai-metric-value">{safe_content_analysis.get('confidence_score')}%</div>
                            </div>
                            <div class="ai-metric">
                                <div class="ai-metric-label">Analysis</div>
                                <div class="ai-metric-value">Gemini 2.5 Pro</div>
                            </div>
                          </div>''',
            
            "destination": f'''<div class="destination-path">📁 {safe_folder_recommendation.get('recommended_folder')}</div>
                              <div class="folder-reasoning">💡 {safe_folder_recommendation.get('reasoning')}</div>
                              <div class="suggested-name">📝 Suggested: <code>{suggested_filename or filename}</code></div>''',
            
            # Store analysis data for further use
            "analysis_data": safe_content_analysis,
            "folder_data": safe_folder_recommendation
        }
    
    def _create_fallback_result(self, filename, file_type, file_size):
        """Create fallback result when workflow fails"""
        current_date = datetime.now().strftime('%Y%m%d')
        
        return {
            "summary": f"""<strong>⚠️ Intelligent Fallback Analysis</strong><br><br>
                          <strong>File:</strong> {filename}<br>
                          <strong>Type:</strong> {file_type}<br>
                          <strong>Size:</strong> {file_size} bytes<br><br>
                          <em>3-step workflow temporarily unavailable. Using intelligent pattern recognition.</em>""",
            
            "details": '''<div class="ai-metrics">
                            <div class="ai-metric">
                                <div class="ai-metric-label">Analysis Mode</div>
                                <div class="ai-metric-value">Fallback</div>
                            </div>
                            <div class="ai-metric">
                                <div class="ai-metric-label">Confidence</div>
                                <div class="ai-metric-value">70%</div>
                            </div>
                            <div class="ai-metric">
                                <div class="ai-metric-label">Method</div>
                                <div class="ai-metric-value">Pattern</div>
                            </div>
                          </div>''',
            
            "destination": f'''<div class="destination-path">📁 Marketing Hub → General → Uploads</div>
                              <div class="folder-reasoning">💡 Using fallback folder recommendation</div>
                              <div class="suggested-name">📝 Suggested: <code>MA-GEN_{filename.split('.')[0] if '.' in filename else filename}_{current_date}_v01.{filename.split('.')[-1] if '.' in filename else 'pdf'}</code></div>''',
            
            "analysis_data": {
                'content_category': 'GENERAL',
                'product_line': 'MA',
                'industry': 'General',
                'document_type': 'Document',
                'target_audience': 'General',
                'business_impact': 'Medium',
                'technical_complexity': 'Intermediate',
                'content_description': 'Business document',
                'confidence_score': '70'
            },
            "folder_data": {
                'recommended_folder': 'Marketing Hub → General → Uploads',
                'reasoning': 'Using fallback folder recommendation'
            }
        }


    def check_file_exists(self, filename, file_size, folder_id=None):
        """Check if a file with similar characteristics already exists"""
        if not self.is_available():
            print("❌ Drive API not available for duplicate check")
            return None
        
        try:
            print(f"🔍 Checking for duplicate files: {filename} ({file_size} bytes)")
            
            # Escape single quotes in filename for query
            escaped_filename = filename.replace("'", "\\'")
            
            # Search for files with the same name
            query = f"name='{escaped_filename}'"
            if folder_id:
                query += f" and parents in '{folder_id}'"
            
            print(f"🔍 Drive API query: {query}")
            
            results = self.service.files().list(
                q=query,
                fields="files(id,name,size,parents,createdTime,webViewLink)",
                pageSize=10
            ).execute()
            
            files = results.get('files', [])
            print(f"🔍 Found {len(files)} files with similar names")
            
            if not files:
                print(f"✅ No duplicate found for: {filename}")
                return None
            
            # Check for exact matches (same name and similar size)
            for file in files:
                existing_size = int(file.get('size', 0))
                size_diff = abs(existing_size - file_size)
                size_threshold = max(1024, file_size * 0.05)  # 5% or 1KB threshold
                
                if size_diff <= size_threshold:
                    print(f"⚠️ Potential duplicate found: {file['name']} (ID: {file['id']})")
                    return {
                        'id': file['id'],
                        'name': file['name'],
                        'size': existing_size,
                        'created_time': file.get('createdTime', ''),
                        'web_link': file.get('webViewLink', ''),
                        'size_difference': size_diff
                    }
            
            print(f"✅ Similar named files found but different sizes for: {filename}")
            return None
            
        except Exception as e:
            print(f"❌ Duplicate check error: {e}")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Filename: {filename}")
            print(f"   Query attempted: name='{filename.replace("'", "\\'")}'")
            # Return None instead of raising exception to allow workflow to continue
            return None


    
    def _create_duplicate_result(self, filename, duplicate_info):
        """Create result for duplicate file detection"""
        from datetime import datetime
        
        # Format the creation time
        created_time = duplicate_info.get('created_time', '')
        if created_time:
            try:
                # Parse ISO format and convert to readable format
                dt = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%B %d, %Y at %I:%M %p')
            except:
                formatted_time = 'Unknown'
        else:
            formatted_time = 'Unknown'
        
        size_mb = duplicate_info.get('size', 0) / (1024 * 1024)
        
        return {
            "summary": f'''<div class="duplicate-warning">
                            <div class="duplicate-icon">⚠️</div>
                            <div class="duplicate-content">
                                <h3>Duplicate File Detected</h3>
                                <p>A file with the same name and similar size already exists in your Marketing Hub.</p>
                            </div>
                          </div>
                          
                          <div class="ai-metrics">
                            <div class="ai-metric">
                                <div class="ai-metric-label">Status</div>
                                <div class="ai-metric-value">Duplicate</div>
                            </div>
                            <div class="ai-metric">
                                <div class="ai-metric-label">Size</div>
                                <div class="ai-metric-value">{size_mb:.1f} MB</div>
                            </div>
                            <div class="ai-metric">
                                <div class="ai-metric-label">Created</div>
                                <div class="ai-metric-value">{formatted_time}</div>
                            </div>
                          </div>''',
            
            "details": f'''<div class="duplicate-details">
                            <strong>Existing File:</strong> {duplicate_info['name']}<br>
                            <strong>File Size:</strong> {size_mb:.1f} MB<br>
                            <strong>Created:</strong> {formatted_time}<br>
                            <strong>Size Difference:</strong> {duplicate_info.get('size_difference', 0)} bytes
                          </div>''',
            
            "destination": f'''<div class="duplicate-action">
                                <div class="destination-path">📁 File Already Exists</div>
                                <div class="folder-reasoning">💡 This file appears to be a duplicate of an existing file in your Marketing Hub</div>
                                <div class="duplicate-link">
                                    <a href="{duplicate_info.get('web_link', '#')}" target="_blank" class="view-existing-btn">
                                        👁️ View Existing File
                                    </a>
                                </div>
                              </div>''',
            
            # Store duplicate info for further processing
            "is_duplicate": True,
            "duplicate_info": duplicate_info,
            "analysis_data": {
                'content_category': 'DUPLICATE',
                'product_line': 'DUP',
                'industry': 'Duplicate'
            }
        }


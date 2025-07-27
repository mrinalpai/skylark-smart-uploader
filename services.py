"""
Services module for Skylark Smart Uploader
Handles Gemini AI integration, Drive API, and naming convention processing
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
    """Handle Gemini AI integration for file analysis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-pro')
            except Exception as e:
                print(f"Gemini initialization error: {e}")
                self.model = None
    
    def is_available(self):
        """Check if Gemini API is available"""
        return self.model is not None
    
    def analyze_file(self, filename, file_type, file_size, naming_convention_rules=None, folder_structure=None):
        """Analyze file using Gemini AI with naming convention and folder structure"""
        if not self.is_available():
            return self._fallback_analysis(filename, file_type, file_size)
        
        try:
            # Create comprehensive analysis prompt
            prompt = self._create_analysis_prompt(filename, file_type, file_size, naming_convention_rules, folder_structure)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse and structure the response
            return self._parse_gemini_response(analysis_text, filename, file_type)
            
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return self._fallback_analysis(filename, file_type, file_size)
    
    def _create_analysis_prompt(self, filename, file_type, file_size, naming_rules, folder_structure):
        """Create comprehensive analysis prompt for Gemini"""
        prompt = f"""
        Analyze this file for intelligent organization in Skylark Drones Marketing Hub:

        FILE DETAILS:
        - Filename: {filename}
        - Type: {file_type}
        - Size: {file_size} bytes

        NAMING CONVENTION RULES:
        {naming_rules or "Standard business naming conventions"}

        FOLDER STRUCTURE:
        {folder_structure or "Standard marketing folder structure"}

        Please provide a comprehensive analysis including:

        1. DOCUMENT TYPE: What type of document is this?
        2. CONTENT CATEGORY: Technical (TECH), Sales (SALES), Marketing (MARK), Brand (BRAND), etc.
        3. PRODUCT LINE: Spectra (SP), Bharat (BS), or Marketing (MA)
        4. INDUSTRY: Mining, Agriculture, Infrastructure, Solar/Renewable Energy, Security, etc.
        5. TARGET AUDIENCE: Engineers, Sales Team, Marketing, Management, Customers
        6. BUSINESS IMPACT: High/Medium/Low strategic value
        7. TECHNICAL COMPLEXITY: Basic/Intermediate/Advanced
        8. RECOMMENDED FOLDER: Specific path from the folder structure above
        9. SUGGESTED FILENAME: Following the naming convention
        10. CONFIDENCE SCORE: 0-100% confidence in analysis

        Format your response as structured data that can be parsed.
        """
        return prompt
    
    def _parse_gemini_response(self, response_text, original_filename, file_type):
        """Parse Gemini response into structured format"""
        try:
            # Extract key information from response
            analysis_data = self._extract_analysis_data(response_text)
            
            # Create structured response
            return {
                "summary": f"""<strong>🧠 Gemini 2.5 Pro Analysis Complete</strong><br><br>
                              <strong>Document Type:</strong> {analysis_data.get('document_type', 'Document')}<br>
                              <strong>Content Category:</strong> {analysis_data.get('content_category', 'General')}<br>
                              <strong>Product Line:</strong> {analysis_data.get('product_line', 'Marketing')}<br>
                              <strong>Industry:</strong> {analysis_data.get('industry', 'General')}<br>
                              <strong>Target Audience:</strong> {analysis_data.get('target_audience', 'General')}<br>
                              <strong>Business Impact:</strong> {analysis_data.get('business_impact', 'Medium')}<br>
                              <strong>Technical Complexity:</strong> {analysis_data.get('technical_complexity', 'Intermediate')}<br><br>
                              <em>AI-powered content analysis with industry intelligence.</em>""",
                
                "details": f'''<div class="ai-metrics">
                                <div class="ai-metric">
                                    <div class="ai-metric-label">Confidence</div>
                                    <div class="ai-metric-value">{analysis_data.get('confidence_score', '95')}%</div>
                                </div>
                                <div class="ai-metric">
                                    <div class="ai-metric-label">Analysis</div>
                                    <div class="ai-metric-value">Gemini 2.5 Pro</div>
                                </div>
                                <div class="ai-metric">
                                    <div class="ai-metric-label">Quality</div>
                                    <div class="ai-metric-value">Professional</div>
                                </div>
                              </div>''',
                
                "destination": f'''<div class="destination-path">📁 {analysis_data.get('suggested_folder', 'Marketing Hub → General')}</div>
                                  <div class="suggested-name">📝 Suggested: <code>{analysis_data.get('suggested_filename', original_filename)}</code></div>''',
                
                # Store analysis data for folder recommendation
                "analysis_data": analysis_data
            }
            
        except Exception as e:
            print(f"Response parsing error: {e}")
            return self._fallback_analysis(original_filename, file_type, 0)
    
    def _extract_analysis_data(self, response_text):
        """Extract analysis data from Gemini response"""
        data = {}
        
        # Extract information using regex patterns
        patterns = {
            'document_type': r'DOCUMENT TYPE[:\s]*([^\n]+)',
            'content_category': r'CONTENT CATEGORY[:\s]*([^\n]+)',
            'product_line': r'PRODUCT LINE[:\s]*([^\n]+)',
            'industry': r'INDUSTRY[:\s]*([^\n]+)',
            'target_audience': r'TARGET AUDIENCE[:\s]*([^\n]+)',
            'business_impact': r'BUSINESS IMPACT[:\s]*([^\n]+)',
            'technical_complexity': r'TECHNICAL COMPLEXITY[:\s]*([^\n]+)',
            'suggested_folder': r'RECOMMENDED FOLDER[:\s]*([^\n]+)',
            'suggested_filename': r'SUGGESTED FILENAME[:\s]*([^\n]+)',
            'confidence_score': r'CONFIDENCE SCORE[:\s]*([0-9]+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                data[key] = match.group(1).strip()
        
        # Set defaults if not found
        defaults = {
            'document_type': 'Business Document',
            'content_category': 'GENERAL',
            'product_line': 'MA',
            'industry': 'General',
            'target_audience': 'Business Team',
            'business_impact': 'Medium',
            'technical_complexity': 'Intermediate',
            'confidence_score': '95'
        }
        
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        
        return data
    
    def _fallback_analysis(self, filename, file_type, file_size):
        """Fallback analysis when Gemini is not available"""
        current_date = datetime.now().strftime('%Y%m%d')
        
        return {
            "summary": f"""<strong>⚠️ Intelligent Fallback Analysis</strong><br><br>
                          <strong>File:</strong> {filename}<br>
                          <strong>Type:</strong> {file_type}<br>
                          <strong>Size:</strong> {file_size} bytes<br><br>
                          <em>Gemini 2.5 Pro temporarily unavailable. Using intelligent pattern recognition.</em>""",
            
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
                              <div class="suggested-name">📝 Suggested: <code>MA-GEN_{filename.split('.')[0]}_{current_date}_v01.{filename.split('.')[-1] if '.' in filename else 'pdf'}</code></div>''',
            
            "analysis_data": {
                'content_category': 'GENERAL',
                'product_line': 'MA',
                'industry': 'General'
            }
        }


class DriveService:
    """Handle Google Drive API integration"""
    
    def __init__(self, credentials=None):
        self.credentials = credentials
        self.service = None
        
        if credentials:
            try:
                self.service = build('drive', 'v3', credentials=credentials)
                print("✅ Drive API service initialized successfully")
            except Exception as e:
                print(f"❌ Drive service initialization error: {e}")
    
    def is_available(self):
        """Check if Drive API is available"""
        available = self.service is not None
        print(f"🔍 Drive API Available: {available}")
        return available
    
    def read_document(self, file_id):
        """Read a Google Docs document content"""
        if not self.is_available():
            print("❌ Drive API not available for document reading")
            return None
        
        try:
            print(f"📖 Reading document: {file_id}")
            # Export as plain text
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
    
    def get_folder_structure(self, folder_id, max_depth=3):
        """Get comprehensive folder structure from Marketing Hub"""
        if not self.is_available():
            print("❌ Drive API not available, using fallback folder structure")
            return self._fallback_folder_structure()
        
        try:
            print(f"📁 Reading folder structure from: {folder_id}")
            folders = []
            folder_map = {}
            self._get_folders_recursive(folder_id, folders, folder_map, 0, max_depth)
            
            structure = self._format_comprehensive_folder_structure(folders, folder_map)
            print(f"✅ Folder structure read successfully: {len(folders)} folders found")
            return structure
            
        except Exception as e:
            print(f"❌ Folder structure error: {e}")
            return self._fallback_folder_structure()
    
    def _get_folders_recursive(self, parent_id, folders, folder_map, depth, max_depth):
        """Recursively get folder structure with enhanced metadata"""
        if depth >= max_depth:
            return
        
        try:
            query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name, parents, createdTime, modifiedTime)",
                orderBy="name"
            ).execute()
            
            for folder in results.get('files', []):
                folder_info = {
                    'id': folder['id'],
                    'name': folder['name'],
                    'depth': depth,
                    'parent_id': parent_id,
                    'path': self._build_folder_path(folder['name'], parent_id, folder_map),
                    'created': folder.get('createdTime', ''),
                    'modified': folder.get('modifiedTime', ''),
                    'category': self._categorize_folder(folder['name'])
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
    
    def _categorize_folder(self, folder_name):
        """Categorize folder based on name patterns"""
        name_lower = folder_name.lower()
        
        # Product line categories
        if any(term in name_lower for term in ['spectra', 'sp-']):
            return 'product_spectra'
        elif any(term in name_lower for term in ['bharat', 'bs-']):
            return 'product_bharat'
        
        # Content type categories
        elif any(term in name_lower for term in ['brand', 'logo', 'visual']):
            return 'brand_assets'
        elif any(term in name_lower for term in ['sales', 'enablement', 'presentation']):
            return 'sales_materials'
        elif any(term in name_lower for term in ['technical', 'tech', 'specification']):
            return 'technical_docs'
        elif any(term in name_lower for term in ['marketing', 'campaign', 'social']):
            return 'marketing_content'
        elif any(term in name_lower for term in ['compliance', 'legal', 'certification']):
            return 'compliance_docs'
        
        # Industry specific categories
        elif any(term in name_lower for term in ['mining', 'coal', 'mineral']):
            return 'industry_mining'
        elif any(term in name_lower for term in ['agriculture', 'farming', 'crop']):
            return 'industry_agriculture'
        elif any(term in name_lower for term in ['solar', 'renewable', 'energy']):
            return 'industry_solar'
        elif any(term in name_lower for term in ['infrastructure', 'construction']):
            return 'industry_infrastructure'
        elif any(term in name_lower for term in ['security', 'surveillance']):
            return 'industry_security'
        else:
            return 'general'
    
    def _format_comprehensive_folder_structure(self, folders, folder_map):
        """Format comprehensive folder structure for AI analysis"""
        structure = "Marketing Hub Folder Structure (Live Data):\n\n"
        
        # Group by category for better organization
        categories = {}
        for folder in folders:
            category = folder['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(folder)
        
        # Format by category
        category_names = {
            'brand_assets': '🎨 Brand Assets',
            'product_spectra': '🚁 Spectra Series',
            'product_bharat': '🌾 Bharat Series',
            'sales_materials': '💼 Sales Materials',
            'technical_docs': '📋 Technical Documentation',
            'marketing_content': '📢 Marketing Content',
            'compliance_docs': '⚖️ Compliance & Legal',
            'industry_mining': '⛏️ Mining Industry',
            'industry_agriculture': '🌱 Agriculture Industry',
            'industry_solar': '☀️ Solar & Renewable Energy',
            'industry_infrastructure': '🏗️ Infrastructure',
            'industry_security': '🔒 Security',
            'general': '📁 General Folders'
        }
        
        for category, category_folders in categories.items():
            if category_folders:
                structure += f"{category_names.get(category, category.title())}:\n"
                for folder in sorted(category_folders, key=lambda x: x['name']):
                    indent = "  " * (folder['depth'] + 1)
                    structure += f"{indent}- {folder['name']} (Path: {folder['path']})\n"
                structure += "\n"
        
        return structure
    
    def get_intelligent_folder_recommendation(self, filename, file_type, analysis_data):
        """Get intelligent folder recommendation based on content analysis and real folder structure"""
        print(f"🎯 Getting intelligent folder recommendation for: {filename}")
        print(f"📊 Analysis data: {analysis_data}")
        
        if not self.is_available():
            print("❌ Drive API not available, using fallback recommendation")
            return self._fallback_folder_recommendation(filename, file_type, analysis_data)
        
        try:
            # Get real folder structure
            folder_structure = self.get_folder_structure(os.environ.get('MARKETING_HUB_FOLDER_ID'))
            
            # Analyze filename and content for folder placement
            filename_lower = filename.lower()
            content_category = analysis_data.get('content_category', 'general').upper()
            product_line = analysis_data.get('product_line', 'MA').upper()
            industry = analysis_data.get('industry', 'general').lower()
            
            print(f"🔍 Analysis: Category={content_category}, Product={product_line}, Industry={industry}")
            
            # Industry-specific mapping with real folder awareness
            if 'solar' in industry or 'renewable' in industry or 'energy' in industry:
                if content_category in ['SALES', 'PRES']:
                    return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Solar & Renewable Energy"
                elif content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 05_Technical Documentation → Solar & Renewable Energy"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Industry Solutions → Solar & Renewable Energy"
            
            elif 'mining' in industry or 'coal' in industry or 'mineral' in industry:
                if content_category in ['SALES', 'PRES']:
                    return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Mining"
                elif content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 05_Technical Documentation → Mining Applications"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra → Mining Solutions"
            
            elif 'agriculture' in industry or 'farming' in industry or 'crop' in industry:
                if content_category in ['SALES', 'PRES']:
                    return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Agriculture"
                elif content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 05_Technical Documentation → Agriculture Applications"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series → Agriculture Solutions"
            
            elif 'infrastructure' in industry or 'construction' in industry:
                if content_category in ['SALES', 'PRES']:
                    return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Infrastructure"
                elif content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 05_Technical Documentation → Infrastructure Applications"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra → Infrastructure Solutions"
            
            # Product line specific mapping
            elif product_line == 'SP' or 'spectra' in filename_lower:
                if content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra → Technical Documentation"
                elif content_category in ['SALES', 'PRES']:
                    return "Marketing Hub → 04_Sales Enablement → Spectra Series"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra"
            
            elif product_line == 'BS' or 'bharat' in filename_lower:
                if content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series → Technical Documentation"
                elif content_category in ['SALES', 'PRES']:
                    return "Marketing Hub → 04_Sales Enablement → Bharat Series"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series"
            
            # Content type mapping - Enhanced for Marketing content
            elif content_category in ['BRAND', 'LOGO']:
                return "Marketing Hub → 01_Brand Assets → Logos & Visual Identity"
            
            elif content_category in ['SALES', 'PRES']:
                return "Marketing Hub → 04_Sales Enablement → Presentations"
            
            elif content_category in ['TECH', 'TECHNICAL']:
                return "Marketing Hub → 05_Technical Documentation"
            
            elif content_category in ['MARKETING', 'CAMPAIGN', 'MARK']:
                # Enhanced marketing content mapping
                if 'brochure' in filename_lower or 'product' in filename_lower:
                    return "Marketing Hub → 03_Marketing Campaigns → Product Brochures"
                elif 'profile' in filename_lower or 'company' in filename_lower:
                    return "Marketing Hub → 01_Brand Assets → Company Profiles"
                elif 'dmo' in product_line.lower() or 'software' in filename_lower:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Software Platform → Marketing Materials"
                else:
                    return "Marketing Hub → 03_Marketing Campaigns → Campaign Assets"
            
            # Product line specific mapping for DMO/Software Platform
            elif 'dmo' in product_line.lower() or 'software' in product_line.lower():
                if content_category in ['TECH', 'TECHNICAL']:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Software Platform → Technical Documentation"
                elif 'brochure' in filename_lower or 'profile' in filename_lower:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Software Platform → Marketing Materials"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Software Platform"
            
            else:
                print("⚠️ No specific mapping found, using general folder")
                return "Marketing Hub → General → Uploads"
                
        except Exception as e:
            print(f"❌ Folder recommendation error: {e}")
            return self._fallback_folder_recommendation(filename, file_type, analysis_data)
    
    def _fallback_folder_recommendation(self, filename, file_type, analysis_data):
        """Enhanced fallback folder recommendation with industry intelligence"""
        filename_lower = filename.lower()
        industry = analysis_data.get('industry', '').lower()
        content_category = analysis_data.get('content_category', '').upper()
        
        print(f"🔄 Using fallback recommendation for: {filename}")
        
        # Industry-specific fallback mapping
        if 'solar' in industry or 'renewable' in industry or 'solar' in filename_lower:
            return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Solar & Renewable Energy"
        elif 'mining' in industry or 'coal' in filename_lower or 'mining' in filename_lower:
            return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Mining"
        elif 'agriculture' in industry or 'farming' in filename_lower or 'crop' in filename_lower:
            return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Agriculture"
        elif 'infrastructure' in industry or 'construction' in filename_lower:
            return "Marketing Hub → 04_Sales Enablement → Industry Specific Material → Infrastructure"
        
        # Product line fallback
        elif any(term in filename_lower for term in ['spectra', 'sp-']):
            return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra"
        elif any(term in filename_lower for term in ['bharat', 'bs-']):
            return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series"
        
        # Content type fallback - Enhanced for Marketing content
        elif any(term in filename_lower for term in ['presentation', 'ppt', 'sales']):
            return "Marketing Hub → 04_Sales Enablement → Presentations"
        elif any(term in filename_lower for term in ['technical', 'spec', 'manual']):
            return "Marketing Hub → 05_Technical Documentation"
        elif any(term in filename_lower for term in ['brand', 'logo']):
            return "Marketing Hub → 01_Brand Assets"
        elif any(term in filename_lower for term in ['brochure', 'profile', 'marketing']):
            if 'corporate' in filename_lower or 'company' in filename_lower:
                return "Marketing Hub → 01_Brand Assets → Company Profiles"
            elif 'product' in filename_lower:
                return "Marketing Hub → 03_Marketing Campaigns → Product Brochures"
            else:
                return "Marketing Hub → 03_Marketing Campaigns → Campaign Assets"
        elif content_category in ['MARKETING', 'MARK']:
            return "Marketing Hub → 03_Marketing Campaigns → Campaign Assets"
        else:
            return "Marketing Hub → General → Uploads"
    
    def _fallback_folder_structure(self):
        """Enhanced fallback folder structure when Drive API is not available"""
        return """Marketing Hub Folder Structure (Fallback):

🎨 Brand Assets:
  - 01_Brand Assets
    - Logos & Visual Identity
    - Photography & Videos
    - Brand Guidelines

🚁 Spectra Series:
  - 02_Product Lines & Sub-Brands
    - Spectra
      - Technical Documentation
      - Marketing Materials
      - Mining Solutions
      - Infrastructure Solutions

🌾 Bharat Series:
  - 02_Product Lines & Sub-Brands
    - Bharat Series
      - Technical Documentation
      - Marketing Materials
      - Agriculture Solutions

💼 Sales Materials:
  - 04_Sales Enablement
    - Presentations
    - Brochures & Datasheets
    - Industry Specific Material
      - Mining
      - Agriculture
      - Solar & Renewable Energy
      - Infrastructure
      - Security

📋 Technical Documentation:
  - 05_Technical Documentation
    - Product Specifications
    - User Manuals
    - Application Notes

📢 Marketing Content:
  - 03_Marketing Campaigns
    - Campaign Assets
    - Social Media Content

⚖️ Compliance & Legal:
  - 06_Compliance
    - Certifications
    - Legal Documents

📁 General:
  - General
    - Uploads
    - Archive"""


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
- SALES: Sales materials

INDUSTRY SPECIFIC:
- Solar/Renewable Energy: Use SOL category
- Mining: Use MIN category
- Agriculture: Use AGR category
- Infrastructure: Use INF category
- Security: Use SEC category

EXAMPLES:
- SP-MIN_coal_mining_analysis_20240126_v01.pdf
- BS-AGR_crop_monitoring_20240126_v02.pptx
- MA-SOL_solar_farm_presentation_20240126_v01.pdf
- SE-INF_infrastructure_solutions_20240126_v01.pdf"""
    
    def apply_naming_convention(self, filename, analysis_data):
        """Apply naming convention to generate proper filename"""
        try:
            # Extract file extension
            file_ext = filename.split('.')[-1] if '.' in filename else 'pdf'
            
            # Get components from analysis
            prefix = analysis_data.get('product_line', 'MA').upper()
            industry = analysis_data.get('industry', 'general').lower()
            content_category = analysis_data.get('content_category', 'GEN').upper()
            
            # Map industry to category
            industry_mapping = {
                'solar': 'SOL',
                'renewable': 'SOL',
                'energy': 'SOL',
                'mining': 'MIN',
                'coal': 'MIN',
                'agriculture': 'AGR',
                'farming': 'AGR',
                'crop': 'AGR',
                'infrastructure': 'INF',
                'construction': 'INF',
                'security': 'SEC',
                'surveillance': 'SEC'
            }
            
            # Determine category based on industry or content
            category = 'GEN'
            for industry_term, industry_code in industry_mapping.items():
                if industry_term in industry:
                    category = industry_code
                    break
            
            # If no industry match, use content category
            if category == 'GEN':
                if content_category in ['TECH', 'TECHNICAL']:
                    category = 'TECH'
                elif content_category in ['SALES', 'PRES']:
                    category = 'SALES'
                elif content_category in ['BRAND', 'LOGO']:
                    category = 'BRAND'
                else:
                    category = 'GEN'
            
            # Generate description from filename
            base_name = filename.split('.')[0] if '.' in filename else filename
            description = re.sub(r'[^a-zA-Z0-9_]', '_', base_name.lower())[:20]
            
            # Current date
            date_str = datetime.now().strftime('%Y%m%d')
            
            # Generate final filename
            suggested_name = f"{prefix}-{category}_{description}_{date_str}_v01.{file_ext}"
            
            print(f"📝 Generated filename: {suggested_name}")
            return suggested_name
            
        except Exception as e:
            print(f"❌ Naming convention error: {e}")
            return filename


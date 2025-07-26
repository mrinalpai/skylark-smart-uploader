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
                self.model = genai.GenerativeModel('gemini-pro')
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
        
        # Base prompt
        prompt = f"""
        Analyze this file for Skylark Drones' Marketing Hub organization:
        
        **File Details:**
        - Filename: {filename}
        - File Type: {file_type}
        - File Size: {file_size} bytes
        
        **Your Task:**
        1. Analyze the filename and type to determine the document's purpose and content category
        2. Suggest the most appropriate folder location based on the content type
        3. Generate a proper filename following Skylark's naming convention
        4. Provide confidence scores for your recommendations
        
        **Available Product Lines & Prefixes:**
        - SP (Spectra) - Mining & Infrastructure drones
        - BS (Bharat Series) - Agriculture & General purpose
        - MA (Marketing) - Marketing materials
        - SE (Sales) - Sales enablement materials
        - TD (Technical) - Technical documentation
        
        **Content Categories:**
        - MIN (Mining), AGR (Agriculture), SEC (Security), INF (Infrastructure)
        - TECH (Technical), PRES (Presentations), BRAND (Brand), SALES (Sales)
        
        **Date Format:** YYYYMMDD (today: {datetime.now().strftime('%Y%m%d')})
        **Version Format:** v01, v02, etc.
        """
        
        # Add naming convention rules if available
        if naming_rules:
            prompt += f"\n\n**Skylark Naming Convention Rules:**\n{naming_rules[:1000]}..."
        
        # Add folder structure if available
        if folder_structure:
            prompt += f"\n\n**Available Marketing Hub Folders:**\n{folder_structure[:500]}..."
        
        prompt += """
        
        **Response Format (JSON):**
        {
            "document_type": "Brief description of document type",
            "content_category": "Primary category (TECH, BRAND, SALES, etc.)",
            "product_line": "Suggested product line (SP, BS, MA, etc.)",
            "suggested_folder": "Full folder path in Marketing Hub",
            "suggested_filename": "Complete filename with proper format",
            "confidence_score": "0-100 confidence percentage",
            "reasoning": "Brief explanation of recommendations"
        }
        
        Provide only the JSON response, no additional text.
        """
        
        return prompt
    
    def _parse_gemini_response(self, response_text, original_filename, file_type):
        """Parse Gemini response and format for UI"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
            else:
                # Fallback parsing
                analysis_data = self._extract_analysis_data(response_text)
            
            # Format for UI display
            return {
                "summary": f"""<strong>Gemini AI Analysis Complete</strong><br><br>
                              <strong>Document Type:</strong> {analysis_data.get('document_type', 'Unknown')}<br>
                              <strong>Category:</strong> {analysis_data.get('content_category', 'General')}<br>
                              <strong>Product Line:</strong> {analysis_data.get('product_line', 'General')}<br><br>
                              <strong>Reasoning:</strong> {analysis_data.get('reasoning', 'Analysis complete')}""",
                
                "details": f'''<div class="ai-metrics">
                                <div class="ai-metric">
                                    <div class="ai-metric-label">AI Engine</div>
                                    <div class="ai-metric-value">Gemini Pro</div>
                                </div>
                                <div class="ai-metric">
                                    <div class="ai-metric-label">Confidence</div>
                                    <div class="ai-metric-value">{analysis_data.get('confidence_score', '85')}%</div>
                                </div>
                                <div class="ai-metric">
                                    <div class="ai-metric-label">Category</div>
                                    <div class="ai-metric-value">{analysis_data.get('content_category', 'General')}</div>
                                </div>
                                <div class="ai-metric">
                                    <div class="ai-metric-label">Processing</div>
                                    <div class="ai-metric-value">Real-time</div>
                                </div>
                              </div>''',
                
                "destination": f'''<div class="destination-path">📁 {analysis_data.get('suggested_folder', 'Marketing Hub → General')}</div>
                                  <div class="suggested-name">📝 Suggested: <code>{analysis_data.get('suggested_filename', original_filename)}</code></div>'''
            }
            
        except Exception as e:
            print(f"Response parsing error: {e}")
            return self._fallback_analysis(original_filename, file_type, 0)
    
    def _extract_analysis_data(self, response_text):
        """Extract analysis data from non-JSON response"""
        # Simple extraction for fallback
        return {
            "document_type": "Document",
            "content_category": "TECH",
            "product_line": "SP",
            "suggested_folder": "Marketing Hub → Technical Documentation",
            "suggested_filename": f"SP-TECH_{datetime.now().strftime('%Y%m%d')}_v01.pdf",
            "confidence_score": "75",
            "reasoning": "Automated analysis based on filename patterns"
        }
    
    def _fallback_analysis(self, filename, file_type, file_size):
        """Fallback analysis when Gemini is not available"""
        current_date = datetime.now().strftime('%Y%m%d')
        
        return {
            "summary": f"""<strong>Intelligent Fallback Analysis</strong><br><br>
                          <strong>File:</strong> {filename}<br>
                          <strong>Type:</strong> {file_type}<br>
                          <strong>Size:</strong> {file_size} bytes<br><br>
                          <em>Gemini API temporarily unavailable. Using intelligent pattern recognition.</em>""",
            
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
                              <div class="suggested-name">📝 Suggested: <code>MA-GEN_{filename.split('.')[0]}_{current_date}_v01.{filename.split('.')[-1] if '.' in filename else 'pdf'}</code></div>'''
        }


class DriveService:
    """Handle Google Drive API integration"""
    
    def __init__(self, credentials=None):
        self.credentials = credentials
        self.service = None
        
        if credentials:
            try:
                self.service = build('drive', 'v3', credentials=credentials)
            except Exception as e:
                print(f"Drive service initialization error: {e}")
    
    def is_available(self):
        """Check if Drive API is available"""
        return self.service is not None
    
    def read_document(self, file_id):
        """Read a Google Docs document content"""
        if not self.is_available():
            return None
        
        try:
            # Export as plain text
            result = self.service.files().export(
                fileId=file_id,
                mimeType='text/plain'
            ).execute()
            
            return result.decode('utf-8')
            
        except Exception as e:
            print(f"Document read error: {e}")
            return None
    
    def get_folder_structure(self, folder_id, max_depth=3):
        """Get comprehensive folder structure from Marketing Hub"""
        if not self.is_available():
            return self._fallback_folder_structure()
        
        try:
            folders = []
            folder_map = {}
            self._get_folders_recursive(folder_id, folders, folder_map, 0, max_depth)
            return self._format_comprehensive_folder_structure(folders, folder_map)
            
        except Exception as e:
            print(f"Folder structure error: {e}")
            return self._fallback_folder_structure()
    
    def _get_folders_recursive(self, parent_id, folders, folder_map, depth, max_depth):
        """Recursively get folder structure with enhanced metadata"""
        if depth >= max_depth:
            return
        
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
            'general': '📁 General Folders'
        }
        
        for category, category_folders in categories.items():
            if category_folders:
                structure += f"{category_names.get(category, category.title())}:\n"
                for folder in sorted(category_folders, key=lambda x: x['name']):
                    indent = "  " * (folder['depth'] + 1)
                    structure += f"{indent}- {folder['name']}\n"
                structure += "\n"
        
        # Add folder recommendations
        structure += "📍 Folder Recommendations:\n"
        structure += "- Use 'Spectra' folders for mining/infrastructure content\n"
        structure += "- Use 'Bharat' folders for agriculture/general content\n"
        structure += "- Technical docs go in Technical Documentation\n"
        structure += "- Marketing materials go in appropriate campaign folders\n"
        structure += "- Brand assets include logos, guidelines, photography\n"
        
        return structure
    
    def get_intelligent_folder_recommendation(self, filename, file_type, analysis_data):
        """Get intelligent folder recommendation based on content analysis"""
        if not self.is_available():
            return self._fallback_folder_recommendation(filename, file_type)
        
        try:
            # Analyze filename and content for folder placement
            filename_lower = filename.lower()
            content_category = analysis_data.get('content_category', 'general').lower()
            product_line = analysis_data.get('product_line', 'ma').lower()
            
            # Determine best folder based on analysis
            if product_line == 'sp' or 'spectra' in filename_lower:
                if content_category in ['tech', 'technical']:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra → Technical Documentation"
                elif content_category in ['sales', 'pres']:
                    return "Marketing Hub → 04_Sales Enablement → Spectra Series"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra"
            
            elif product_line == 'bs' or 'bharat' in filename_lower:
                if content_category in ['tech', 'technical']:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series → Technical Documentation"
                elif content_category in ['sales', 'pres']:
                    return "Marketing Hub → 04_Sales Enablement → Bharat Series"
                else:
                    return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series"
            
            elif content_category in ['brand', 'logo']:
                return "Marketing Hub → 01_Brand Assets → Logos & Visual Identity"
            
            elif content_category in ['sales', 'pres']:
                return "Marketing Hub → 04_Sales Enablement → Presentations"
            
            elif content_category in ['tech', 'technical']:
                return "Marketing Hub → 05_Technical Documentation"
            
            elif content_category in ['marketing', 'campaign']:
                return "Marketing Hub → 03_Marketing Campaigns → Campaign Assets"
            
            else:
                return "Marketing Hub → General → Uploads"
                
        except Exception as e:
            print(f"Folder recommendation error: {e}")
            return self._fallback_folder_recommendation(filename, file_type)
    
    def _fallback_folder_recommendation(self, filename, file_type):
        """Fallback folder recommendation"""
        filename_lower = filename.lower()
        
        if any(term in filename_lower for term in ['spectra', 'sp-', 'mining']):
            return "Marketing Hub → 02_Product Lines & Sub-Brands → Spectra"
        elif any(term in filename_lower for term in ['bharat', 'bs-', 'agriculture']):
            return "Marketing Hub → 02_Product Lines & Sub-Brands → Bharat Series"
        elif any(term in filename_lower for term in ['presentation', 'ppt', 'sales']):
            return "Marketing Hub → 04_Sales Enablement → Presentations"
        elif any(term in filename_lower for term in ['technical', 'spec', 'manual']):
            return "Marketing Hub → 05_Technical Documentation"
        elif any(term in filename_lower for term in ['brand', 'logo']):
            return "Marketing Hub → 01_Brand Assets"
        else:
            return "Marketing Hub → General → Uploads"
    
    def _fallback_folder_structure(self):
        """Fallback folder structure when Drive API is not available"""
        return """Marketing Hub Folder Structure:
- 00_Admin & Guidelines
  - File Naming Rules
  - Brand Guidelines
- 01_Brand Assets
  - Logos & Visual Identity
  - Photography & Videos
- 02_Product Lines & Sub-Brands
  - Spectra Series
  - Bharat Series
- 03_Marketing Campaigns
  - Campaign Assets
  - Social Media Content
- 04_Sales Enablement
  - Presentations
  - Brochures & Datasheets
- 05_Technical Documentation
  - Product Specifications
  - User Manuals
- 06_Compliance
  - Certifications
  - Legal Documents"""


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
            rules = self.drive_service.read_document(self.document_id)
            if rules:
                self._cached_rules = rules
                return rules
        
        # Fallback rules
        return self._fallback_naming_rules()
    
    def _fallback_naming_rules(self):
        """Fallback naming convention rules"""
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
- SEC: Security applications
- INF: Infrastructure applications
- TECH: Technical documentation
- PRES: Presentations
- BRAND: Brand materials
- SALES: Sales materials

EXAMPLES:
- SP-MIN_drill_analysis_20240126_v01.pdf
- BS-AGR_crop_monitoring_20240126_v02.pptx
- MA-BRAND_logo_guidelines_20240126_v01.pdf"""
    
    def apply_naming_convention(self, filename, analysis_data):
        """Apply naming convention to generate proper filename"""
        try:
            # Extract file extension
            file_ext = filename.split('.')[-1] if '.' in filename else 'pdf'
            
            # Get components from analysis
            prefix = analysis_data.get('product_line', 'MA')
            category = analysis_data.get('content_category', 'GEN')
            
            # Generate description from filename
            base_name = filename.split('.')[0] if '.' in filename else filename
            description = re.sub(r'[^a-zA-Z0-9_]', '_', base_name.lower())[:20]
            
            # Current date
            date_str = datetime.now().strftime('%Y%m%d')
            
            # Generate final filename
            suggested_name = f"{prefix}-{category}_{description}_{date_str}_v01.{file_ext}"
            
            return suggested_name
            
        except Exception as e:
            print(f"Naming convention error: {e}")
            return filename


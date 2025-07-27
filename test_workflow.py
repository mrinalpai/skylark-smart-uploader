#!/usr/bin/env python3
"""
Test script for the 3-step intelligent workflow
"""

import os
import sys
sys.path.append('/home/ubuntu/skylark-smart-uploader')

from services_enhanced import GeminiService, DriveService, NamingConventionService, IntelligentWorkflowOrchestrator

def test_workflow():
    """Test the 3-step intelligent workflow"""
    print("🧪 Testing 3-step intelligent workflow...")
    
    # Initialize services
    gemini_service = GeminiService("AIzaSyC_r3bNkIN41mSe7-nrnhePguaW7oq4C2E")
    drive_service = DriveService(None)  # No credentials for basic test
    naming_service = NamingConventionService(drive_service)
    
    # Create workflow orchestrator
    workflow_orchestrator = IntelligentWorkflowOrchestrator(
        gemini_service, drive_service, naming_service
    )
    
    # Test files
    test_files = [
        {
            'filename': 'Skylark Drones Corporate Profile.pdf',
            'file_type': 'application/pdf',
            'file_size': 2800000
        },
        {
            'filename': 'Solar Energy Solutions Brochure.pdf',
            'file_type': 'application/pdf',
            'file_size': 1500000
        },
        {
            'filename': 'Spectra Mining Technical Manual.pdf',
            'file_type': 'application/pdf',
            'file_size': 3200000
        }
    ]
    
    for test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Testing: {test_file['filename']}")
        print(f"{'='*60}")
        
        try:
            result = workflow_orchestrator.execute_intelligent_workflow(
                filename=test_file['filename'],
                file_type=test_file['file_type'],
                file_size=test_file['file_size'],
                marketing_hub_folder_id="1FM66Jay8G6gpXsP-pLGwW64-FmqJszLa"
            )
            
            print("✅ Workflow completed successfully!")
            print(f"Summary: {result.get('summary', 'No summary')[:200]}...")
            print(f"Destination: {result.get('destination', 'No destination')}")
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
    
    print(f"\n{'='*60}")
    print("🧪 Testing completed!")

if __name__ == "__main__":
    test_workflow()


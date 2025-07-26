# Skylark Smart Uploader - Quick Deployment Instructions

## 🚀 Ready for Google Cloud Deployment

This package contains everything needed to deploy the Skylark Smart Uploader to Google Cloud Platform.

### 📦 Package Contents

```
skylark-gcp/
├── main.py                 # Main Flask application with Gemini integration
├── app.yaml               # Google App Engine configuration
├── Dockerfile             # Google Cloud Run configuration
├── requirements.txt       # Python dependencies
├── .gcloudignore         # Files to ignore during deployment
├── static/
│   ├── SkylarkLogo-BirdOrange.png    # Skylark logo
│   └── drone-bg.png                  # Drone background image
└── DEPLOYMENT_INSTRUCTIONS.md        # This file
```

### ⚡ Quick Start (App Engine)

1. **Configure your credentials in `app.yaml`:**
   ```yaml
   env_variables:
     GOOGLE_CLIENT_ID: "YOUR_OAUTH2_CLIENT_ID"
     GOOGLE_CLIENT_SECRET: "YOUR_OAUTH2_CLIENT_SECRET"
     MARKETING_HUB_FOLDER_ID: "YOUR_DRIVE_FOLDER_ID"
     GEMINI_API_KEY: "YOUR_GEMINI_API_KEY"
   ```

2. **Deploy to Google App Engine:**
   ```bash
   gcloud app deploy
   ```

3. **Update OAuth2 redirect URIs in Google Cloud Console:**
   - Add: `https://YOUR_PROJECT_ID.appspot.com/api/auth/callback`

### ⚡ Quick Start (Cloud Run)

1. **Build and deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/skylark-uploader
   
   gcloud run deploy skylark-uploader \
     --image gcr.io/YOUR_PROJECT_ID/skylark-uploader \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="GOOGLE_CLIENT_ID=YOUR_CLIENT_ID,GOOGLE_CLIENT_SECRET=YOUR_SECRET,MARKETING_HUB_FOLDER_ID=YOUR_FOLDER_ID,GEMINI_API_KEY=YOUR_API_KEY"
   ```

2. **Update OAuth2 redirect URIs:**
   - Add the Cloud Run service URL + `/api/auth/callback`

### 🔧 Required Setup

1. **Google Cloud APIs** (enable these):
   - App Engine Admin API
   - Cloud Run API
   - Google Drive API
   - Generative Language API (for Gemini)

2. **OAuth2 Client** (Google Cloud Console):
   - Create OAuth2 client ID
   - Add appropriate redirect URIs
   - Configure consent screen

3. **Gemini API Key**:
   - Enable Generative Language API
   - Create API key
   - Configure restrictions

### 🎯 Features Included

- ✅ **World-class UI/UX** - Minimalistic, professional design
- ✅ **Google Gemini AI** - Real content analysis and categorization
- ✅ **Smart Organization** - Automatic folder placement
- ✅ **OAuth2 Authentication** - Secure Google login
- ✅ **Manual Override** - Custom folder selection
- ✅ **Real-time Progress** - Upload status tracking
- ✅ **Responsive Design** - Works on all devices
- ✅ **Production Ready** - Optimized for Google Cloud

### 📚 Full Documentation

See `SKYLARK_GOOGLE_CLOUD_DEPLOYMENT_GUIDE.md` for comprehensive deployment instructions, troubleshooting, and maintenance procedures.

---

**Ready to deploy your world-class smart file uploader! 🚀**


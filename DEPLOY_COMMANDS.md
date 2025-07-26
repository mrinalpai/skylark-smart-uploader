# Skylark Smart Uploader - Deployment Commands

## 🚀 Ready to Deploy!

Your Skylark Smart Uploader is configured and ready for deployment with:
- ✅ **Gemini API Key**: AIzaSyC_r3bNkIN41mSe7-nrnhePguaW7oq4C2E
- ✅ **OAuth2 Credentials**: Configured for Skylark Drones
- ✅ **Marketing Hub**: Folder ID configured
- ✅ **Custom Domain**: Ready for skylarkcloud.com

---

## 💻 Deployment Commands

### **Step 1: Open Command Line**

**On Windows:**
- Press `Windows + R`
- Type `cmd` and press Enter
- Or search "Command Prompt" in Start menu

**On Mac:**
- Press `Cmd + Space`
- Type `terminal` and press Enter
- Or go to Applications → Utilities → Terminal

**On Linux:**
- Press `Ctrl + Alt + T`
- Or search for "Terminal" in applications

### **Step 2: Navigate to Project Folder**

```bash
# Change to the skylark-ready directory
# Replace "PATH_TO_FOLDER" with the actual path where you extracted the files
cd PATH_TO_FOLDER/skylark-ready

# For example, if it's on your Desktop:
# Windows: cd C:\Users\YourName\Desktop\skylark-ready
# Mac: cd ~/Desktop/skylark-ready
# Linux: cd ~/Desktop/skylark-ready
```

### **Step 3: Initialize Google App Engine (First Time Only)**

```bash
# This creates your App Engine application
gcloud app create --region=us-central1
```

**What this does:** Creates your App Engine application in the US Central region (good for global access)

### **Step 4: Deploy Your Application**

```bash
# Deploy the Skylark Smart Uploader
gcloud app deploy
```

**What this does:** 
- Uploads your application to Google Cloud
- Installs all dependencies
- Starts your application
- Gives you a URL to access it

### **Step 5: Get Your Application URL**

```bash
# Open your deployed application
gcloud app browse
```

**What this does:** Opens your application in your default browser

---

## 🎯 Expected Output

When deployment is successful, you'll see:
```
Deployed service [default] to [https://your-project-id.appspot.com]
```

**Your Skylark Smart Uploader will be live at that URL!**

---

## 🆘 If You Get Stuck

### **Common Issues:**

1. **"gcloud not found"**
   - Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
   - Restart your command line after installation

2. **"You do not currently have an active account"**
   - Run: `gcloud auth login`
   - Follow the browser login process

3. **"No project specified"**
   - Run: `gcloud config set project YOUR_PROJECT_ID`
   - Replace YOUR_PROJECT_ID with your actual Google Cloud project ID

4. **Permission errors**
   - Make sure you're the owner/editor of the Google Cloud project
   - Check that billing is enabled on your project

### **Need Help?**
- Copy and paste any error messages
- I can help troubleshoot specific issues
- All your credentials are already configured correctly

---

## ✅ Success Checklist

After deployment, you should have:
- [ ] Application deployed successfully
- [ ] URL provided (https://your-project-id.appspot.com)
- [ ] Application loads in browser
- [ ] Google login button visible
- [ ] Professional Skylark UI displayed

**🎉 Once deployed, we'll set up skylarkcloud.com to point to your application!**


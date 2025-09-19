# SIH25039
Integrated Platform for Crowdsourced Ocean Hazard Reporting and Social Media Analytics

# Neptune Intel

> **Empowering citizens & authorities with real-time ocean hazard insights through crowdsourced reports and social media intelligence.**

---

## ✨ Overview

This project is a **web + mobile platform** designed to complement **INCOIS** (Indian National Centre for Ocean Information Services) by:

* Collecting **citizen reports** of unusual ocean activity (e.g., flooding, tides, coastal damage).
* Ingesting **social media posts** (Twitter, Facebook, Instagram, YouTube) related to ocean hazards.
* Using **Firebase services** for authentication, hosting, storage, and database management.
* Applying **NLP + H3 spatial indexing** for verification, filtering, and hotspot generation.
* Visualizing incidents in **real-time dashboards** with heatmaps, bar charts, and scatter plots.

---

<h2>📸 UI Preview</h2>
<img src="./Screenshot from 2025-09-19 18-53-23.png" alt="App UI" width="600"/>

---
## 🚀 Features

* 🌍 **Geotagged citizen reports** with photo/video upload
* 🔑 **Role-based access control** (citizens, officials, analysts)
* 📡 **Social media feed integration** with NLP filtering
* 🗺️ **Interactive map visualization** (heatmaps & hotspots)
* 📊 **Analytics dashboard** (sentiment, frequency, sources)
* 🌐 **Multilingual support** for coastal communities
* 📶 **Offline-first mode** (data syncs when connection restores)

---

## 🛠️ Tech Stack

* **Frontend:** React + TailwindCSS
* **Backend:** Firebase Cloud Functions
* **Database:** Firebase Firestore
* **Authentication:** Firebase Auth (Google, Email, Social logins)
* **Storage:** Firebase Storage (media uploads)
* **Hosting:** Firebase Hosting
* **Analytics:** Firebase + NLP APIs + H3 Spatial Indexing

---

## 📂 Project Structure

```bash
📦 coastal-hazard-platform
 ┣ 📂 public          # Static files
 ┣ 📂 src
 ┃ ┣ 📂 components    # UI Components
 ┃ ┣ 📂 pages         # App Pages
 ┃ ┣ 📂 services      # Firebase + API services
 ┃ ┗ 📂 utils         # NLP & Geo indexing utils
 ┣ 📜 firebase.json   # Firebase Hosting config
 ┣ 📜 firestore.rules # Firestore security rules
 ┗ 📜 README.md
```

---

## ⚡ Firebase Services Used

* **Firebase Authentication** → Secure user login with multiple providers
* **Firestore Database** → Store crowdsourced reports + verified hazard data
* **Firebase Storage** → Upload and manage photos/videos of incidents
* **Firebase Hosting** → Deploy and host the web app
* **Cloud Functions** → Automate NLP, H3 indexing, and

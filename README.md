# URL Shortener API
🚀 **Test My Url Shortner Live Demo: No Need To Setup Locally** 
[fahad-innovaxel-hussain.vercel.app](https://fahad-innovaxel-hussain.vercel.app) 
- Note : You can check Network tab to check response of api 

## Overview
This is a  URL shortener API built with Flask and PostgreSQL and deployed on Vercel.

## Main Branch Policy
The main branch is limited to a `README.md` file with setup instructions and API documentation. All development should be done on dev branch before merging.

---

##  How to Setup

### **1️⃣ Clone the Repository**
```sh
$ git clone  https://github.com/fahadcr14/fahad-innovaxel-hussain
$ cd fahad-innovaxel-hussain
```

### **2️⃣ Create a Virtual Environment & Install Dependencies**
```sh
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows use: venv\Scripts\activate
$ pip install -r requirements.txt
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file in the root directory and add the following:
```ini
SHORTURL_POSTGRES_DATABASE=<your_database>
SHORTURL_POSTGRES_USER=<your_username>
SHORTURL_POSTGRES_PASSWORD=<your_password>
SHORTURL_POSTGRES_HOST=<your_host>
SHORTURL_POSTGRES_PORT=5432
```




### **5️⃣ Run the Application**
```sh
$ python app.py
```
The API will be available at: `http://127.0.0.1:5000/`

---

## 🚀 API Endpoints

### **1️⃣ Shorten a URL**
**Endpoint:** `/shorten`  
**Method:** `POST`  
**Request Body:**
```json
{
  "url": "https://example.com"
}
```
**Response:**
```json
{
  "shortCode": "abc123",
  "original_url": "https://example.com",
  "access_count": 0,
  "createdAt": "2025-03-22T10:52:15",
  "updatedAt": "2025-03-22T10:52:15"
}
```

### **2️⃣ Redirect to Original URL**
**Endpoint:** `/<shortCode>`  
**Method:** `GET`  
**Response:** Redirects to the original URL

### **3️⃣ Get URL Statistics**
**Endpoint:** `/stats/<shortCode>/`  
**Method:** `GET`  
**Response:**
```json
{
  "shortCode": "abc123",
  "original_url": "https://example.com",
  "access_count": 10,
  "createdAt": "2025-03-22T10:52:15",
  "updatedAt": "2025-03-22T10:52:15"
}
```

### **4️⃣ Delete a Shortened URL**
**Endpoint:** `/<shortCode>/`  
**Method:** `DELETE`  
**Response:**
```json
{
  "message": "URL deleted"
}
```

### **5️⃣ Update a Shortened URL**
**Endpoint:** `/shorten/<shortCode>/`  
**Method:** `PUT`  
**Request Body:**
```json
{
  "url": "https://new-url.com"
}
```
**Response:**
```json
{
  "shortCode": "abc123",
  "original_url": "https://new-url.com",
  "access_count": 10,
  "createdAt": "2025-03-22T10:52:15",
  "updatedAt": "2025-03-22T11:00:00"
}
```

---





---

## 📜 License
MIT License


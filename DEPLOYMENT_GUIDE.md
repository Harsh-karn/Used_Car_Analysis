# 🚀 Used Cars Analysis - Deployment Guide

## 📋 Overview
This project can be deployed in multiple ways. Choose the option that best fits your needs:

## 🌐 Deployment Options

### 1. **Streamlit Cloud (Recommended)**
**Easiest deployment option**

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/used-cars-analysis.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Deploy!

**Live URL:** `https://yourusername-used-cars-analysis-app-xxxxx.streamlit.app`

### 2. **Heroku**
**Popular cloud platform**

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

3. **Open app:**
   ```bash
   heroku open
   ```

### 3. **Docker Deployment**
**Containerized deployment**

1. **Build and run locally:**
   ```bash
   docker build -t used-cars-app .
   docker run -p 8501:8501 used-cars-app
   ```

2. **Deploy to cloud:**
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances

### 4. **Local Development**
**Run on your machine**

1. **Streamlit App:**
   ```bash
   streamlit run app.py
   ```
   Open: http://localhost:8501

2. **Flask API:**
   ```bash
   python api.py
   ```
   Open: http://localhost:5000

## 📁 File Structure for Deployment

```
used-cars-analysis/
├── app.py                 # Streamlit web app
├── api.py                 # Flask REST API
├── requirements.txt      # Python dependencies
├── Procfile              # Heroku deployment
├── runtime.txt           # Python version
├── setup.sh              # Heroku setup script
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
├── used_cars.csv         # Dataset
└── DEPLOYMENT_GUIDE.md   # This file
```

## 🔧 Configuration Files

### `requirements.txt`
```
streamlit==1.50.0
pandas==2.2.3
numpy==2.2.6
matplotlib==3.10.7
seaborn==0.13.2
plotly==6.1.0
scikit-learn==1.7.2
flask==3.1.2
```

### `Procfile` (for Heroku)
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### `Dockerfile`
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🌟 Features Available in Deployment

### Streamlit Web App (`app.py`)
- 📊 Interactive dashboard
- 🔍 Data exploration tools
- 📈 Real-time visualizations
- 🎛️ Filter controls
- 📱 Responsive design

### Flask API (`api.py`)
- 🔌 RESTful endpoints
- 📊 JSON data responses
- 🔍 Search functionality
- 📈 Statistical analysis
- 🚀 Fast performance

## 🚀 Quick Start Commands

### Local Development
```bash
# Streamlit app
streamlit run app.py

# Flask API
python api.py

# Docker
docker-compose up
```

### Production Deployment
```bash
# Heroku
git push heroku main

# Docker
docker build -t used-cars-app .
docker run -p 8501:8501 used-cars-app
```

## 📊 API Endpoints

### GET Endpoints
- `/api/stats` - Dataset statistics
- `/api/brands` - Brand analysis
- `/api/years` - Year analysis
- `/api/fuel` - Fuel type analysis
- `/api/transmission` - Transmission analysis
- `/api/owner` - Owner type analysis
- `/api/engine` - Engine size analysis
- `/api/correlation` - Feature correlations

### POST Endpoints
- `/api/search` - Search cars with filters

### Example API Usage
```bash
# Get statistics
curl http://localhost:5000/api/stats

# Search cars
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"brand": "Maruti", "fuel_type": "Petrol"}'
```

## 🔒 Security Considerations

1. **Environment Variables:**
   - Set `FLASK_ENV=production` for Flask
   - Use environment-specific configurations

2. **Data Protection:**
   - Dataset is included in deployment
   - No external database required
   - All processing happens locally

3. **Access Control:**
   - Public access (adjust as needed)
   - No authentication required (add if needed)

## 📈 Performance Optimization

1. **Caching:**
   - Streamlit uses `@st.cache_data`
   - Flask loads data once at startup

2. **Data Processing:**
   - Optimized pandas operations
   - Efficient memory usage

3. **Visualizations:**
   - Plotly for interactive charts
   - Cached computations

## 🐛 Troubleshooting

### Common Issues:

1. **Port conflicts:**
   ```bash
   # Change ports in app.py and api.py
   streamlit run app.py --server.port=8502
   ```

2. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Data file not found:**
   - Ensure `used_cars.csv` is in the same directory
   - Check file permissions

4. **Memory issues:**
   - Reduce dataset size for testing
   - Use data sampling for large datasets

## 📞 Support

For deployment issues:
1. Check logs: `heroku logs --tail`
2. Verify requirements: `pip list`
3. Test locally first
4. Check file permissions

## 🎯 Next Steps

1. **Choose deployment method**
2. **Test locally**
3. **Deploy to cloud**
4. **Monitor performance**
5. **Share your app!**

---

**🚀 Your Used Cars Analysis project is ready for deployment!**

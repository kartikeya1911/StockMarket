# 🚀 Setup and Installation Guide

## System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python Version:** 3.8 or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 500MB free space
- **Internet:** Required for fetching stock data

## Step-by-Step Installation

### 1. Install Python

If you don't have Python installed:

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Verify Installation

Open terminal/command prompt and run:
```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip version
```

### 3. Download Project

Option A: If you have Git:
```bash
cd path/to/your/projects
git clone <repository-url>
cd StockMarket
```

Option B: Manual download:
1. Download the ZIP file
2. Extract to desired location
3. Open terminal in the StockMarket folder

### 4. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- streamlit
- pandas
- numpy
- yfinance
- plotly
- scikit-learn
- ta (technical analysis)
- textblob
- newsapi-python

**Installation may take 3-5 minutes**

### 6. Verify Installation

Check if all packages are installed:
```bash
pip list
```

### 7. Run the Application

```bash
streamlit run app.py
```

The application should automatically open in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to that URL.

## 🎯 First Time Setup

### 1. Test the Application

1. The home page should load
2. Click "📊 Stock Analysis" in the sidebar
3. Enter "AAPL" as ticker
4. Click "Analyze Stock"
5. You should see Apple stock data and charts

### 2. Configure News API (Optional)

For real news data:

1. Go to [https://newsapi.org/register](https://newsapi.org/register)
2. Sign up (free)
3. Copy your API key
4. Open `config.py` in a text editor
5. Find line: `NEWS_API_KEY = "YOUR_API_KEY_HERE"`
6. Replace with: `NEWS_API_KEY = "your-actual-api-key"`
7. Save the file
8. Restart the application

### 3. Try Each Feature

✅ **Stock Analysis**
- Enter: AAPL
- Click: Analyze Stock
- Expected: Charts and data appear

✅ **Price Prediction**
- Enter: TSLA
- Model: Linear Regression
- Period: 1 Year
- Click: Generate Prediction
- Expected: Predictions and charts appear

✅ **Technical Indicators**
- Enter: MSFT
- Click: Analyze Indicators
- Expected: RSI, MACD, Bollinger Bands appear

✅ **Portfolio Tracker**
- Click sidebar "Add Stock to Portfolio"
- Enter: AAPL, Quantity: 10, Price: 150
- Click: Add to Portfolio
- Expected: Portfolio appears with stock

✅ **News & Sentiment**
- Enter: GOOGL
- Click: Fetch News
- Expected: News articles and sentiment appear

## 🐛 Troubleshooting

### Issue: "streamlit: command not found"

**Solution:**
```bash
# Ensure you're in the virtual environment
# Then reinstall streamlit
pip install --upgrade streamlit
```

### Issue: "No module named 'yfinance'"

**Solution:**
```bash
pip install yfinance
```

### Issue: "Permission denied"

**Windows Solution:**
```bash
# Run as administrator
```

**macOS/Linux Solution:**
```bash
sudo pip install -r requirements.txt
```

### Issue: Port already in use

**Solution:**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Issue: Slow data fetching

**Causes:**
- Slow internet connection
- yfinance API limitations

**Solution:**
- Wait patiently (first fetch takes longer)
- Try different stock tickers
- Check internet connection

### Issue: Charts not displaying

**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear
# Restart application
```

## 📱 Running on Different Devices

### Access from Other Devices on Same Network

1. Find your computer's IP address:

**Windows:**
```bash
ipconfig
# Look for IPv4 Address
```

**macOS/Linux:**
```bash
ifconfig
# Look for inet address
```

2. Run with network access:
```bash
streamlit run app.py --server.address 0.0.0.0
```

3. On other device, navigate to:
```
http://YOUR-IP-ADDRESS:8501
```

## 🔧 Advanced Configuration

### Change Default Port

Edit `.streamlit/config.toml` (create if doesn't exist):
```toml
[server]
port = 8502
```

### Increase Upload Limit

```toml
[server]
maxUploadSize = 200
```

### Enable CORS

```toml
[server]
enableCORS = false
```

## 📦 Updating the Application

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Update Streamlit

```bash
pip install --upgrade streamlit
```

## 🚀 Deployment (Optional)

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Deploy your repository
5. Share the public URL

### Deploy to Heroku

```bash
# Add Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Add setup.sh
# (Instructions available online)

# Deploy
git push heroku main
```

## ✅ Installation Complete!

You should now have:
- ✅ Python installed
- ✅ All dependencies installed
- ✅ Application running
- ✅ All features working

## 📚 Next Steps

1. Read the [README.md](README.md) for usage guide
2. Explore each feature
3. Try different stock tickers
4. Build your portfolio
5. Customize the code

## 💡 Tips

- Keep the terminal open while using the application
- Use Ctrl+C to stop the application
- Clear browser cache if UI looks broken
- Check console for error messages
- Deactivate virtual environment: `deactivate`

## 🆘 Need Help?

- Check error messages in terminal
- Review README.md documentation
- Verify all installation steps
- Ensure internet connection is active
- Try with popular tickers: AAPL, MSFT, GOOGL

---

**Happy Analyzing! 📈**

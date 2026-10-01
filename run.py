import os
import sys
import threading
import time
import webbrowser
import uvicorn

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Launching ComicCraft AI Studio...")
    print("🌐 Web App URL: http://127.0.0.1:8000")
    print("📚 API Docs:    http://127.0.0.1:8000/docs")
    print("=" * 60)
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Uvicorn server
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

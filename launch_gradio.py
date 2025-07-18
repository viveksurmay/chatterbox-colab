#!/usr/bin/env python3
"""
Launch script for Chatterbox TTS Gradio Live UI
"""

import sys
import subprocess
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import gradio
        import torch
        import librosa
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_requirements():
    """Install requirements if needed"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_gradio.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def main():
    """Main launch function"""
    print("🚀 Chatterbox TTS Gradio Live UI Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("gradio_live_ui.py").exists():
        print("❌ gradio_live_ui.py not found in current directory")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("📦 Installing missing requirements...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("pip install -r requirements_gradio.txt")
            sys.exit(1)
    
    # Set environment variables for better performance
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
    os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
    
    print("🎙️ Starting Chatterbox TTS Live UI...")
    print("📱 The interface will be available at:")
    print("   - Local: http://localhost:7860")
    print("   - Network: http://0.0.0.0:7860")
    print("   - Public URL will be shown when ready")
    print()
    print("💡 Tips:")
    print("   - Use GPU for faster generation")
    print("   - Upload clear audio samples for voice cloning")
    print("   - No watermarks are applied to generated audio")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the gradio app
        from gradio_live_ui import demo
        demo.launch()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Chatterbox TTS Live UI...")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

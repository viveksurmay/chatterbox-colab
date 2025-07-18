# 🎙️ Chatterbox TTS - Simple Gradio UI

A clean, simple Gradio interface for Chatterbox TTS without watermarking.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## 🎯 Features

- **Text-to-Speech**: Convert text to speech with optional voice cloning
- **Voice Conversion**: Convert one voice to another
- **No Watermarks**: Clean audio output without watermarking
- **Simple Interface**: Easy-to-use Gradio web UI

## 🎛️ Controls

### Text-to-Speech
- **Text**: Enter the text you want to synthesize
- **Reference Audio**: Upload audio file for voice cloning (optional)
- **Exaggeration**: Control emotion intensity (0.25-2.0)
- **CFG Weight**: Control pacing (0.0-1.0)
- **Temperature**: Control randomness (0.1-2.0)

### Voice Conversion
- **Source Audio**: Upload the audio you want to convert
- **Target Voice**: Upload the voice you want to convert to

## 📝 Usage

1. Open the web interface (automatically opens after running `python app.py`)
2. Choose either "Text-to-Speech" or "Voice Conversion" tab
3. Upload your audio files and adjust parameters
4. Click "Generate" or "Convert"
5. Download the generated audio

## 💡 Tips

- Use clear, high-quality audio for best results
- Keep audio samples between 3-10 seconds
- Default parameters work well for most cases
- GPU recommended for faster generation

---

**Simple, clean, and effective! 🎉**

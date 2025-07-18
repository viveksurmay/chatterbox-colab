# 🎙️ Chatterbox TTS - Gradio Live UI (No Watermark)

A powerful, user-friendly web interface for Chatterbox TTS with real-time controls, voice cloning, and voice conversion - **without watermarking**.

## 🌟 Features

### 🎤 Text-to-Speech
- **Real-time generation** with progress tracking
- **Voice cloning** from uploaded audio samples
- **Interactive parameter controls** with live feedback
- **Example text categories** for quick testing
- **Seed control** for reproducible results
- **Advanced sampling options** (min_p, top_p, repetition penalty)

### 🔄 Voice Conversion
- **Convert existing speech** to different voices
- **Upload source and target audio** files
- **Real-time processing** with status updates
- **High-quality conversion** without watermarks

### 🎛️ Live Controls
- **Exaggeration slider**: Control emotion intensity (0.25-2.0)
- **CFG Weight**: Adjust pacing and deliberation (0.0-1.0)
- **Temperature**: Control randomness and consistency (0.1-2.0)
- **Advanced parameters**: Fine-tune generation behavior

### 🚀 Enhanced UI
- **Tabbed interface** for different functions
- **Progress bars** with detailed status updates
- **Audio download** buttons for all generated content
- **Responsive design** that works on desktop and mobile
- **Real-time device detection** (GPU/CPU/MPS)

## 🔧 Installation & Setup

### Quick Start
```bash
# Clone the repository
git clone https://github.com/viveksurmay/chatterbox-colab.git
cd chatterbox-colab

# Install dependencies
pip install -r requirements_gradio.txt

# Launch the UI
python launch_gradio.py
```

### Manual Installation
```bash
# Install core dependencies
pip install gradio>=4.0.0 torch torchaudio librosa transformers

# Install Chatterbox TTS
pip install chatterbox-tts

# Run the UI directly
python gradio_live_ui.py
```

## 🎯 Usage

### 1. Launch the Interface
```bash
python launch_gradio.py
```

The interface will be available at:
- **Local**: http://localhost:7860
- **Network**: http://0.0.0.0:7860
- **Public URL**: Automatically generated for sharing

### 2. Text-to-Speech
1. **Enter text** in the text box or select an example category
2. **Upload reference audio** (optional) for voice cloning
3. **Adjust parameters** using the sliders
4. **Click "Generate Speech"** and wait for completion
5. **Play and download** the generated audio

### 3. Voice Conversion
1. **Upload source audio** (speech to convert)
2. **Upload target voice** (voice to convert to)
3. **Click "Convert Voice"** and wait for processing
4. **Play and download** the converted audio

## 🎛️ Parameter Guide

### Core Parameters
- **Exaggeration (0.25-2.0)**
  - `0.5`: Neutral, natural speech
  - `0.7-1.0`: More expressive and emotional
  - `1.5+`: Highly dramatic (may be unstable)

- **CFG Weight (0.0-1.0)**
  - `0.3`: Slower, more deliberate pacing
  - `0.5`: Balanced (default)
  - `0.8+`: Faster speech

- **Temperature (0.1-2.0)**
  - `0.5`: Very consistent output
  - `0.8`: Balanced randomness (default)
  - `1.5+`: More creative but less predictable

### Advanced Parameters
- **min_p**: Newer sampling method (0.02-0.1 recommended)
- **top_p**: Original sampling method (1.0 disables)
- **Repetition Penalty**: Reduces repetitive speech (1.0-2.0)

## 💡 Tips for Best Results

### 🎯 General Usage
- Default settings work well for most cases
- For fast speakers, lower CFG weight to ~0.3
- Use clear, descriptive text for better pronunciation

### 🎭 Expressive Speech
- Lower CFG weight (~0.3) + higher exaggeration (~0.7)
- Higher exaggeration speeds up speech; lower CFG compensates
- Experiment with different combinations

### 🎤 Voice Cloning
- Use clear, high-quality audio samples (3-10 seconds)
- Single speaker recordings work best
- Avoid background noise or music
- Various accents supported (optimized for English)

### 🔄 Voice Conversion
- Both source and target should be clear speech
- Similar speaking styles convert better
- Longer reference audio (5-15 seconds) gives better results

## 🚀 Technical Features

### Performance
- **GPU acceleration** when available
- **Concurrent processing** (up to 2 users)
- **Real-time progress tracking**
- **Efficient model loading** (cached after first use)

### No Watermarking
- **Clean audio output** without any watermarks
- **Modified TTS/VC classes** that skip watermark application
- **Raw audio generation** for maximum quality

### Device Support
- **CUDA GPU**: Fastest performance
- **Apple Silicon (MPS)**: Good performance on M1/M2 Macs
- **CPU**: Slower but functional fallback

## 📁 File Structure

```
chatterbox-colab/
├── gradio_live_ui.py              # Main Gradio interface
├── launch_gradio.py               # Launch script with setup
├── requirements_gradio.txt        # Dependencies for UI
├── src/chatterbox/
│   ├── tts_no_watermark.py       # TTS without watermarking
│   └── vc_no_watermark.py        # VC without watermarking
└── GRADIO_LIVE_README.md         # This file
```

## 🔧 Customization

### Adding New Example Categories
Edit the `examples` dictionary in `gradio_live_ui.py`:
```python
examples = {
    "Your Category": "Your example text here...",
    # ... other categories
}
```

### Modifying UI Layout
The interface uses Gradio Blocks for flexible layout customization. Edit the UI structure in the `with gr.Blocks()` section.

### Changing Default Parameters
Modify the default values in the slider definitions:
```python
exaggeration = gr.Slider(0.25, 2.0, step=0.05, value=0.5)  # Change value=0.5
```

## 🐛 Troubleshooting

### Common Issues
1. **"Model not found"**: Ensure you have internet connection for model download
2. **CUDA out of memory**: Reduce batch size or use CPU
3. **Audio upload fails**: Check file format (WAV, MP3, etc.)
4. **Slow generation**: Enable GPU or reduce text length

### Performance Tips
- **Use GPU** for 5-10x faster generation
- **Keep text under 300 characters** for best performance
- **Use high-quality reference audio** for voice cloning
- **Close other GPU applications** to free memory

## 📄 License

This enhanced UI is provided under the same MIT license as the original Chatterbox project.

## 🤝 Contributing

Feel free to submit issues, suggestions, or improvements to make this UI even better!

---

**🎉 Enjoy creating amazing voices with Chatterbox TTS Live UI!**

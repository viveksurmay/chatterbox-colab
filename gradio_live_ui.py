import random
import numpy as np
import torch
import gradio as gr
import time
import os
from pathlib import Path

# Import the no-watermark versions
from src.chatterbox.tts_no_watermark import ChatterboxTTSNoWatermark
from src.chatterbox.vc_no_watermark import ChatterboxVCNoWatermark

# Device detection
if torch.cuda.is_available():
    DEVICE = "cuda"
    print(f"🚀 Using GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    DEVICE = "mps"
    print("🍎 Using Apple Silicon MPS")
else:
    DEVICE = "cpu"
    print("💻 Using CPU (this will be slower)")

# Global model states
tts_model = None
vc_model = None

def set_seed(seed: int):
    """Set random seed for reproducibility"""
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)

def load_tts_model():
    """Load TTS model (called once on startup)"""
    global tts_model
    if tts_model is None:
        print("🔄 Loading Chatterbox TTS model (no watermark)...")
        tts_model = ChatterboxTTSNoWatermark.from_pretrained(DEVICE)
        print("✅ TTS Model loaded successfully!")
    return tts_model

def load_vc_model():
    """Load VC model (called when needed)"""
    global vc_model
    if vc_model is None:
        print("🔄 Loading Chatterbox VC model (no watermark)...")
        vc_model = ChatterboxVCNoWatermark.from_pretrained(DEVICE)
        print("✅ VC Model loaded successfully!")
    return vc_model

def generate_tts(text, audio_prompt, exaggeration, cfg_weight, temperature, seed_num, min_p, top_p, repetition_penalty, progress=gr.Progress()):
    """Generate TTS with progress tracking"""
    if not text.strip():
        return None, "❌ Please enter some text!"
    
    progress(0.1, desc="Loading model...")
    model = load_tts_model()
    
    if seed_num != 0:
        set_seed(int(seed_num))
    
    progress(0.3, desc="Processing text...")
    
    try:
        start_time = time.time()
        
        progress(0.5, desc="Generating speech...")
        wav = model.generate(
            text,
            audio_prompt_path=audio_prompt,
            exaggeration=exaggeration,
            temperature=temperature,
            cfg_weight=cfg_weight,
            min_p=min_p,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
        )
        
        progress(0.9, desc="Finalizing audio...")
        generation_time = time.time() - start_time
        
        progress(1.0, desc="Complete!")
        
        status = f"✅ Generated in {generation_time:.2f}s | Sample rate: {model.sr}Hz | No watermark applied"
        return (model.sr, wav.squeeze(0).numpy()), status
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def generate_vc(source_audio, target_voice, progress=gr.Progress()):
    """Generate voice conversion with progress tracking"""
    if source_audio is None:
        return None, "❌ Please upload source audio!"
    
    if target_voice is None:
        return None, "❌ Please upload target voice!"
    
    progress(0.1, desc="Loading VC model...")
    model = load_vc_model()
    
    try:
        start_time = time.time()
        
        progress(0.5, desc="Converting voice...")
        wav = model.generate(
            source_audio,
            target_voice_path=target_voice
        )
        
        progress(0.9, desc="Finalizing audio...")
        generation_time = time.time() - start_time
        
        progress(1.0, desc="Complete!")
        
        status = f"✅ Voice converted in {generation_time:.2f}s | Sample rate: {model.sr}Hz | No watermark applied"
        return (model.sr, wav.squeeze(0).numpy()), status
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def get_example_text(category):
    """Get example text based on category"""
    examples = {
        "Neutral": "Welcome to Chatterbox TTS. This is a demonstration of high-quality text-to-speech synthesis with advanced emotion control.",
        "Excited": "This is absolutely incredible! The technology behind this voice synthesis is truly amazing and revolutionary!",
        "Dramatic": "In the depths of the ancient castle, shadows danced across the stone walls as thunder echoed through the night.",
        "Educational": "Machine learning algorithms process vast amounts of data to identify patterns and make intelligent predictions.",
        "Gaming": "Victory is ours! That was an epic battle with incredible teamwork and perfect execution!",
        "Calm": "Take a deep breath and relax. Let your mind settle as you focus on the peaceful present moment."
    }
    return examples.get(category, examples["Neutral"])

# Custom CSS for better styling
custom_css = """
.gradio-container {
    max-width: 1200px !important;
}
.status-box {
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
.header-text {
    text-align: center;
    color: #2d5aa0;
    margin-bottom: 20px;
}
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="🎙️ Chatterbox Live UI") as demo:
    
    # Header
    gr.HTML("""
    <div class="header-text">
        <h1>🎙️ Chatterbox TTS Live UI</h1>
        <p><strong>High-Quality Text-to-Speech & Voice Conversion</strong></p>
        <p><em>No Watermark Version - Enhanced with Live Controls</em></p>
    </div>
    """)
    
    with gr.Tabs():
        # TTS Tab
        with gr.TabItem("🎤 Text-to-Speech", id="tts"):
            with gr.Row():
                with gr.Column(scale=2):
                    # Text input with examples
                    with gr.Group():
                        gr.Markdown("### 📝 Text Input")
                        text_input = gr.Textbox(
                            value="Welcome to Chatterbox TTS! This is a demonstration of high-quality text-to-speech synthesis with emotion control.",
                            label="Text to synthesize",
                            placeholder="Enter your text here...",
                            lines=4,
                            max_lines=8
                        )
                        
                        # Example text selector
                        with gr.Row():
                            example_category = gr.Dropdown(
                                choices=["Neutral", "Excited", "Dramatic", "Educational", "Gaming", "Calm"],
                                value="Neutral",
                                label="Example Categories",
                                scale=2
                            )
                            load_example_btn = gr.Button("📋 Load Example", scale=1)
                    
                    # Voice cloning
                    with gr.Group():
                        gr.Markdown("### 🎭 Voice Cloning")
                        audio_prompt = gr.Audio(
                            sources=["upload", "microphone"],
                            type="filepath",
                            label="Reference Audio (optional - for voice cloning)",
                            value=None
                        )
                    
                    # Parameters
                    with gr.Group():
                        gr.Markdown("### 🎛️ Generation Parameters")
                        
                        with gr.Row():
                            exaggeration = gr.Slider(
                                0.25, 2.0, step=0.05, value=0.5,
                                label="🎭 Exaggeration",
                                info="Emotion intensity (0.5=neutral, higher=more expressive)"
                            )
                            cfg_weight = gr.Slider(
                                0.0, 1.0, step=0.05, value=0.5,
                                label="⚡ CFG Weight",
                                info="Pacing control (lower=slower, more deliberate)"
                            )
                        
                        with gr.Row():
                            temperature = gr.Slider(
                                0.1, 2.0, step=0.1, value=0.8,
                                label="🌡️ Temperature",
                                info="Randomness (lower=more consistent)"
                            )
                            seed_num = gr.Number(
                                value=0,
                                label="🎲 Seed",
                                info="Random seed (0 for random)",
                                precision=0
                            )
                        
                        # Advanced parameters (collapsed by default)
                        with gr.Accordion("🔧 Advanced Parameters", open=False):
                            with gr.Row():
                                min_p = gr.Slider(
                                    0.00, 1.00, step=0.01, value=0.05,
                                    label="min_p",
                                    info="Newer sampler (0.02-0.1 recommended)"
                                )
                                top_p = gr.Slider(
                                    0.00, 1.00, step=0.01, value=1.00,
                                    label="top_p",
                                    info="Original sampler (1.0 disables)"
                                )
                                repetition_penalty = gr.Slider(
                                    1.00, 2.00, step=0.1, value=1.2,
                                    label="Repetition Penalty"
                                )
                    
                    # Generate button
                    generate_btn = gr.Button("🎤 Generate Speech", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    # Output
                    with gr.Group():
                        gr.Markdown("### 🔊 Generated Audio")
                        audio_output = gr.Audio(label="Output", show_download_button=True)
                        status_output = gr.Textbox(label="Status", interactive=False, lines=2)
        
        # Voice Conversion Tab
        with gr.TabItem("🔄 Voice Conversion", id="vc"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📁 Audio Files")
                    source_audio = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Source Audio (speech to convert)"
                    )
                    target_voice = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Target Voice (voice to convert to)"
                    )
                    
                    convert_btn = gr.Button("🔄 Convert Voice", variant="primary", size="lg")
                
                with gr.Column():
                    gr.Markdown("### 🔊 Converted Audio")
                    vc_output = gr.Audio(label="Converted Audio", show_download_button=True)
                    vc_status = gr.Textbox(label="Status", interactive=False, lines=2)
        
        # Tips Tab
        with gr.TabItem("💡 Tips & Info", id="tips"):
            gr.Markdown("""
            ## 💡 Tips for Best Results
            
            ### 🎯 General Usage:
            - **Default settings** work well for most cases (`exaggeration=0.5`, `cfg_weight=0.5`)
            - For **fast speakers**, lower `cfg_weight` to around `0.3`
            - Use **clear, descriptive text** for better pronunciation
            
            ### 🎭 Expressive Speech:
            - **Lower CFG weight** (~0.3) + **higher exaggeration** (~0.7) for dramatic speech
            - Higher exaggeration speeds up speech; lower CFG compensates with slower pacing
            - Experiment with different combinations for unique voices
            
            ### 🎤 Voice Cloning:
            - Use **clear, high-quality** audio samples (3-10 seconds ideal)
            - **Single speaker** recordings work best
            - Avoid background noise, music, or multiple speakers
            - The model works with various accents (optimized for English)
            
            ### 🔄 Voice Conversion:
            - Both source and target audio should be **clear speech**
            - **Similar speaking styles** convert better
            - Longer reference audio (5-15 seconds) gives better results
            
            ### ⚙️ Technical Info:
            - **No watermarking** applied to generated audio
            - Supports **GPU acceleration** for faster generation
            - **Reproducible results** with seed control
            - **Real-time progress** tracking during generation
            
            ---
            
            ## 🚀 Device Information
            - **Current Device**: """ + DEVICE + """
            - **Model**: Chatterbox TTS (No Watermark Version)
            - **Sample Rate**: 24kHz
            """)
    
    # Event handlers
    load_example_btn.click(
        fn=get_example_text,
        inputs=[example_category],
        outputs=[text_input]
    )
    
    generate_btn.click(
        fn=generate_tts,
        inputs=[text_input, audio_prompt, exaggeration, cfg_weight, temperature, seed_num, min_p, top_p, repetition_penalty],
        outputs=[audio_output, status_output]
    )
    
    convert_btn.click(
        fn=generate_vc,
        inputs=[source_audio, target_voice],
        outputs=[vc_output, vc_status]
    )

if __name__ == "__main__":
    # Pre-load TTS model on startup
    print("🚀 Starting Chatterbox Live UI...")
    load_tts_model()
    
    # Launch with live features
    demo.queue(
        max_size=50,
        default_concurrency_limit=2,  # Allow 2 concurrent users
    ).launch(
        share=True,
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        show_error=True,
        show_tips=True,
        enable_queue=True
    )

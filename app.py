import torch
import gradio as gr
from src.chatterbox.tts_no_watermark import ChatterboxTTSNoWatermark
from src.chatterbox.vc_no_watermark import ChatterboxVCNoWatermark

# Device detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# Global models
tts_model = None
vc_model = None

def load_tts_model():
    global tts_model
    if tts_model is None:
        tts_model = ChatterboxTTSNoWatermark.from_pretrained(DEVICE)
    return tts_model

def load_vc_model():
    global vc_model
    if vc_model is None:
        vc_model = ChatterboxVCNoWatermark.from_pretrained(DEVICE)
    return vc_model

def generate_speech(text, audio_file, exaggeration, cfg_weight, temperature):
    if not text.strip():
        return None
    
    model = load_tts_model()
    
    try:
        wav = model.generate(
            text,
            audio_prompt_path=audio_file,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature,
        )
        return (model.sr, wav.squeeze(0).numpy())
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_voice(source_audio, target_audio):
    if source_audio is None or target_audio is None:
        return None
    
    model = load_vc_model()
    
    try:
        wav = model.generate(source_audio, target_voice_path=target_audio)
        return (model.sr, wav.squeeze(0).numpy())
    except Exception as e:
        print(f"Error: {e}")
        return None

# Create Gradio interface
with gr.Blocks(title="Chatterbox TTS") as app:
    gr.Markdown("# 🎙️ Chatterbox TTS (No Watermark)")
    
    with gr.Tabs():
        with gr.Tab("Text-to-Speech"):
            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        label="Text",
                        placeholder="Enter text to synthesize...",
                        lines=3
                    )
                    audio_input = gr.Audio(
                        label="Reference Audio (optional)",
                        type="filepath"
                    )
                    
                    with gr.Row():
                        exaggeration = gr.Slider(
                            0.25, 2.0, value=0.5, step=0.05,
                            label="Exaggeration"
                        )
                        cfg_weight = gr.Slider(
                            0.0, 1.0, value=0.5, step=0.05,
                            label="CFG Weight"
                        )
                        temperature = gr.Slider(
                            0.1, 2.0, value=0.8, step=0.1,
                            label="Temperature"
                        )
                    
                    generate_btn = gr.Button("Generate", variant="primary")
                
                with gr.Column():
                    audio_output = gr.Audio(label="Generated Audio")
        
        with gr.Tab("Voice Conversion"):
            with gr.Row():
                with gr.Column():
                    source_audio = gr.Audio(
                        label="Source Audio",
                        type="filepath"
                    )
                    target_audio = gr.Audio(
                        label="Target Voice",
                        type="filepath"
                    )
                    convert_btn = gr.Button("Convert", variant="primary")
                
                with gr.Column():
                    converted_audio = gr.Audio(label="Converted Audio")
    
    # Event handlers
    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, audio_input, exaggeration, cfg_weight, temperature],
        outputs=audio_output
    )
    
    convert_btn.click(
        fn=convert_voice,
        inputs=[source_audio, target_audio],
        outputs=converted_audio
    )

if __name__ == "__main__":
    app.launch(share=True)

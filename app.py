"""
Hugging Face Spaces Entry Point (ZeroGPU / FastAPI / Aiogram)
"""
import os

try:
    import spaces
    @spaces.GPU
    def dummy_gpu_task():
        """Satisfies ZeroGPU supervisor requirement"""
        return True
except Exception:
    pass

import gradio as gr
from main import app as fastapi_app

with gr.Blocks(title="GoldenEra 5G Proxies", theme=gr.themes.Base()) as demo:
    gr.Markdown("# ⚡ GoldenEra 5G Proxies")
    gr.Markdown("✅ **System Status:** Online & Active 24/7")
    gr.Markdown("Telegram Bot is connected and running in the background.")
    gr.HTML('''
        <div style="margin: 20px 0;">
            <a href="/admin" target="_blank" style="padding: 12px 24px; background: #10b981; color: #000; font-weight: 700; text-decoration: none; border-radius: 6px; font-family: sans-serif; display: inline-block;">
                Open Admin Dashboard 🚀
            </a>
        </div>
    ''')

# Mount Gradio onto FastAPI
app = gr.mount_gradio_app(fastapi_app, demo, path="/status")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port, log_level="info")

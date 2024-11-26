#! /usr/bin/env python

import os
import sys
import click
import gradio as gr

sys.path.append("..")
from cli import configure_model, generate_video

with gr.Blocks() as demo:
    gr.Markdown("Video Generator")
    with gr.Row():
        prompt = gr.Textbox(
            label="Prompt",
            value="A hand with delicate fingers picks up a bright yellow lemon from a wooden bowl filled with lemons and sprigs of mint against a peach-colored background. The hand gently tosses the lemon up and catches it, showcasing its smooth texture. A beige string bag sits beside the bowl, adding a rustic touch to the scene. Additional lemons, one halved, are scattered around the base of the bowl. The even lighting enhances the vibrant colors and creates a fresh, inviting atmosphere.",
        )
        negative_prompt = gr.Textbox(label="Negative Prompt", value="")
        seed = gr.Number(label="Seed", value=1710977262, precision=0)
    with gr.Row():
        width = gr.Number(label="Width", value=848, precision=0)
        height = gr.Number(label="Height", value=480, precision=0)
        num_frames = gr.Number(label="Number of Frames", value=163, precision=0)
    with gr.Row():
        cfg_scale = gr.Number(label="CFG Scale", value=4.5)
        num_inference_steps = gr.Number(label="Number of Inference Steps", value=200, precision=0)
    btn = gr.Button("Generate Video")
    output = gr.Video()

    btn.click(
        generate_video,
        inputs=[
            prompt,
            negative_prompt,
            width,
            height,
            num_frames,
            seed,
            cfg_scale,
            num_inference_steps,
        ],
        outputs=output,
    )


@click.command()
@click.option("--model_dir", required=True, help="Path to the model directory.")
@click.option("--cpu_offload", is_flag=True, help="Whether to offload model to CPU")
@click.option("--gpu_id", default="0", help="GPU ID to use (default: 0). Use 'cpu' to force CPU.")
@click.option("--host", default="0.0.0.0", help="Host to run the server on (default: 0.0.0.0). Use 'localhost' for local access only.")
@click.option("--port", default=7860, help="Port to run the server on")
def launch(model_dir, cpu_offload, gpu_id, host, port):
    # Set the GPU to use
    if gpu_id.lower() == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Force CPU usage
        print("Using CPU for computation.")
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id  # Set the specified GPU
        print(f"Using GPU {gpu_id} for computation.")

    # Configure the model
    configure_model(model_dir, cpu_offload)

    # Launch the Gradio app
    print(f"Launching server on {host}:{port}")
    demo.launch(server_name=host, server_port=port)


if __name__ == "__main__":
    launch()

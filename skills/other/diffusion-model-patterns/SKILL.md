---
name: diffusion-model-patterns
description: Diffusion model training and inference patterns including UNet/DiT architectures, noise schedules, CFG, ControlNet, and LoRA. Use when building or fine-tuning image generation models.
---

# Diffusion Model Patterns

## Architecture Selection

| Architecture | Params | Scaling | Best For |
|-------------|--------|---------|----------|
| **UNet** | Conv-based, skip connections | Moderate (plateaus >2B) | Standard image gen, ControlNet compat |
| **DiT** | Transformer blocks, AdaLN | Scales well (>10B) | Large-scale training, video, high-res |
| **UViT** | Transformer + long skip connections | Good | Bridge between UNet and DiT |

| Formulation | Training | Sampling | When to Use |
|-------------|----------|----------|-------------|
| **DDPM** | Discrete timesteps, epsilon prediction | Slow (1000 steps) | Learning/prototyping |
| **DDIM** | Same training as DDPM | Fast (10-50 steps deterministic) | Drop-in replacement for faster DDPM sampling |
| **Flow Matching** | Continuous time, velocity prediction | Fast, ODE-based | State-of-the-art; SD3, Flux |
| **Rectified Flow** | Straight paths, reflow | Very fast (1-4 steps possible) | Distilled models, real-time inference |

Default recommendation: Flow matching with DiT for new projects. UNet + DDPM/DDIM for compatibility with existing Stable Diffusion ecosystem.

## Training Loop (DDPM, Epsilon Prediction)

```python
import torch
import torch.nn.functional as F
from diffusers import DDPMScheduler, UNet2DConditionModel

noise_scheduler = DDPMScheduler(
    num_train_timesteps=1000,
    beta_schedule="scaled_linear",    # "linear", "scaled_linear", "squaredcos_cap_v2"
    beta_start=0.00085,
    beta_end=0.012,
    prediction_type="epsilon",        # "epsilon", "v_prediction", "sample"
)

def training_step(model, vae, text_encoder, batch, weight_dtype=torch.bfloat16):
    with torch.no_grad():
        latents = vae.encode(batch["pixel_values"].to(weight_dtype)).latent_dist.sample()
        latents = latents * vae.config.scaling_factor
        encoder_hidden_states = text_encoder(batch["input_ids"])[0]

    noise = torch.randn_like(latents)
    timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps,
                              (latents.shape[0],), device=latents.device).long()
    noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

    noise_pred = model(noisy_latents, timesteps, encoder_hidden_states).sample
    loss = F.mse_loss(noise_pred.float(), noise.float())
    return loss
```

## Sampling with Different Schedulers

```python
from diffusers import (
    DDIMScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
)

# Scheduler comparison for inference
scheduler_configs = {
    "ddim_50":    (DDIMScheduler, {"num_inference_steps": 50}),
    "euler_25":   (EulerDiscreteScheduler, {"num_inference_steps": 25}),
    "dpm++_20":   (DPMSolverMultistepScheduler, {"num_inference_steps": 20}),
    "euler_a_30": (EulerAncestralDiscreteScheduler, {"num_inference_steps": 30}),
}

@torch.no_grad()
def sample(pipe, prompt, scheduler_cls, scheduler_kwargs, guidance_scale=7.5):
    pipe.scheduler = scheduler_cls.from_config(pipe.scheduler.config)
    return pipe(
        prompt, guidance_scale=guidance_scale,
        **scheduler_kwargs, generator=torch.Generator("cuda").manual_seed(42),
    ).images[0]
```

### Scheduler Decision

| Scheduler | Steps | Quality | Speed | Notes |
|-----------|-------|---------|-------|-------|
| DDIM | 50 | Good | Slow | Deterministic, invertible |
| Euler | 20-30 | Good | Fast | Reliable default |
| DPM++ 2M Karras | 20 | Great | Fast | Best quality/speed tradeoff |
| Euler Ancestral | 25-30 | Good + varied | Fast | Stochastic, more diverse |
| LCM | 4-8 | Decent | Very fast | Requires LCM-LoRA or distilled model |

## Classifier-Free Guidance (CFG)

```python
@torch.no_grad()
def cfg_sample_step(model, latents, timestep, encoder_hidden_states,
                    guidance_scale=7.5):
    # Duplicate latents for conditional + unconditional
    latent_input = torch.cat([latents] * 2)
    timestep_input = torch.cat([timestep] * 2)

    # Unconditional = empty string embedding; conditional = prompt embedding
    uncond_embeddings = torch.zeros_like(encoder_hidden_states)
    text_input = torch.cat([uncond_embeddings, encoder_hidden_states])

    noise_pred = model(latent_input, timestep_input, text_input).sample
    noise_pred_uncond, noise_pred_cond = noise_pred.chunk(2)

    # CFG formula
    guided = noise_pred_uncond + guidance_scale * (noise_pred_cond - noise_pred_uncond)
    return guided
```

### CFG Scale Guidelines

| Scale | Effect | Use Case |
|-------|--------|----------|
| 1.0 | No guidance (unconditional) | Diversity exploration |
| 3.0-5.0 | Mild guidance | Artistic, less saturated |
| 7.0-8.5 | Standard | General purpose |
| 10.0-15.0 | Strong guidance | Precise prompt following |
| 15.0+ | Over-saturated | Usually too much; artifacts |

## ControlNet Conditioning

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny", torch_dtype=torch.float16
)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
).to("cuda")

# Training a custom ControlNet
from diffusers import ControlNetModel

controlnet = ControlNetModel.from_unet(pretrained_unet)  # init from existing UNet

def controlnet_training_step(controlnet, unet, batch):
    """UNet is frozen; only ControlNet trains."""
    noisy_latents = add_noise(batch["latents"], noise, timesteps)
    controlnet_cond = batch["conditioning_image"]   # edge map, depth, pose, etc.

    down_samples, mid_sample = controlnet(
        noisy_latents, timesteps, encoder_hidden_states,
        controlnet_cond=controlnet_cond, return_dict=False,
    )
    noise_pred = unet(
        noisy_latents, timesteps, encoder_hidden_states,
        down_block_additional_residuals=down_samples,
        mid_block_additional_residual=mid_sample,
    ).sample

    return F.mse_loss(noise_pred.float(), noise.float())
```

## LoRA for Diffusion Models

```python
from diffusers import StableDiffusionPipeline
from peft import LoraConfig

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
)

# Apply LoRA to UNet attention layers
unet_lora_config = LoraConfig(
    r=8, lora_alpha=16, init_lora_weights="gaussian",
    target_modules=["to_q", "to_v", "to_k", "to_out.0"],
)
pipe.unet.add_adapter(unet_lora_config)

# Optionally also train text encoder LoRA (helps with new concepts)
text_lora_config = LoraConfig(
    r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"],
)
pipe.text_encoder.add_adapter(text_lora_config)
```

## Gotchas and Anti-Patterns

### Noise Schedule Selection
- `scaled_linear` is the SD1/SD2 default. `squaredcos_cap_v2` (cosine) is better for high-res
- Wrong noise schedule at inference = broken outputs even with correct weights
- v-prediction requires matching schedule at training AND inference -- cannot swap to epsilon

### EMA Decay
- Use EMA decay 0.9999 for models >100M params. Start EMA after warmup (1000-5000 steps)
- **Anti-pattern**: evaluating the training model instead of EMA model -- results look worse than they are
- EMA doubles memory for model weights; use CPU offload for EMA if constrained

### VAE Encoding
- Always multiply latents by `vae.config.scaling_factor` (0.18215 for SD1.x, 0.13025 for SDXL)
- VAE decode can produce values outside [-1, 1] -- clamp before converting to uint8
- Fine-tuning the VAE decoder separately can fix small artifacts without retraining the diffusion model

### Inference Optimization
- `pipe.enable_model_cpu_offload()` -- moves each component to GPU only when needed
- `pipe.enable_xformers_memory_efficient_attention()` or use PyTorch 2.0+ SDPA (automatic)
- `torch.compile(pipe.unet)` gives 10-30% speedup, but first call is slow (compilation)
- Half precision (`float16`) for inference is fine; `bfloat16` wastes mantissa bits at inference time
- Batch CFG: concatenating cond+uncond doubles batch dim but halves forward passes

### Common Mistakes
- Training at pixel-level resolution instead of latent-space -- 64x memory increase
- Not freezing the VAE and text encoder during UNet training
- Using learning rates above 1e-4 for diffusion fine-tuning -- 1e-5 to 5e-5 is typical
- Ignoring `prediction_type` mismatch between training and scheduler
- Not using `generator` seeds during evaluation -- can't reproduce or compare samples

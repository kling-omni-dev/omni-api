# Kling Omni API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/kling/kling-image-o3?utm_source=github&utm_medium=ugc&utm_campaign=kling-omni-dev&utm_content=readme-badge&utm_term=tier-a)

Kling Omni is Kuaishou's reference-image generation model: you hand it up to ten pictures, address them in the prompt as `@Image1`, `@Image2` and so on, and it produces new images that keep the subjects, products or styles consistent across outputs. This package is a Kling Omni API client for Python: one `pip install` and you can generate single images or coherent series at 1K, 2K or 4K without touching the vendor console.

You get a blocking `run()` that returns output URLs, a submit-and-poll path for batch jobs, webhook delivery on completion, and one runtime dependency (`httpx`). It is aimed at product teams building catalogue, campaign and character pipelines that need the same subject rendered many times.

> **Try it now:** [https://synexa.ai/explore/kling/kling-image-o3](https://synexa.ai/explore/kling/kling-image-o3?utm_source=github&utm_medium=ugc&utm_campaign=kling-omni-dev&utm_content=readme-top&utm_term=tier-a) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Kling Omni](#about-kling-omni)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **There is nothing to self-host.** Kling Omni is a closed model; the only way to run it is through a hosted API. This client gives you that as a Python call rather than a web UI.
- **Multi-reference in one request.** Up to 10 reference images per call, addressed individually in a prompt of up to 2,500 characters, so a product shot, a model and a background can be combined in one generation.
- **Series output.** `result_type="series"` returns 2–9 related images in one prediction, which is what storyboards, lookbooks and multi-angle product pages actually need.
- **Flat per-run pricing.** `kling/kling-image-o3` is $0.028 per run at any resolution up to 4K, billed per prediction with no idle charge.

## Installation

```bash
pip install git+https://github.com/kling-omni-dev/omni-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=kling-omni-dev&utm_content=readme-apikey&utm_term=tier-a)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import omni_api

output = omni_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light",
    "image_urls": [
        "https://example.com/input.png"
    ]
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from omni_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light", "image_urls": ["https://example.com/input.png"]})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`kling/kling-image-o3`](https://synexa.ai/explore/kling/kling-image-o3?utm_source=github&utm_medium=ugc&utm_campaign=kling-omni-dev&utm_content=readme-models&utm_term=tier-a) | image-to-image | Kling Omni 3 generates images from reference pictures with strong subject consistency, up to 4K. | $0.028 |

The default model is **`kling/kling-image-o3`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `kling/kling-image-o3`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `Put the product from @Image1 on a marble…` | — | Text prompt for image generation. Reference images using @Image1, @Image2, etc. (or @Image if only one image). Max 2500 characters. |
| `image_urls` | files | yes | — | — | Reference images (.jpg/.png/.webp), up to 10. Address them in the prompt as @Image1, @Image2, … |
| `resolution` | string | no | `1K` | 1K, 2K, 4K | Image generation resolution. 1K: standard, 2K: high-res, 4K: ultra high-res. |
| `result_type` | string | no | `single` | single, series | Result type. 'single' for one image, 'series' for a series of related images. |
| `num_images` | integer | no | `1` | 1, 9 | Number of images to generate (1-9). Only used when result_type is 'single'. |
| `series_amount` | integer | no | — | 2, 9 | Number of images in series (2-9). Only used when result_type is 'series'. |
| `aspect_ratio` | string | no | `auto` | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9, auto | Aspect ratio of generated images. 'auto' intelligently determines based on input content. |
| `output_format` | string | no | `png` | jpeg, png, webp | The format of the generated image. |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from omni_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Kling Omni

Kling AI is the generative image and video family developed by Kuaishou. Kling Omni is its unified reference-conditioned image model, served on Synexa as `kling/kling-image-o3` (Kling Omni 3). Where a plain text-to-image model starts from noise and a description, Kling Omni starts from the pictures you supply and a prompt that refers to them by position, and its primary strength is subject consistency: the same face, garment or object survives across outputs and across a whole series.

The hosted endpoint accepts `prompt` and `image_urls` as required fields and exposes `resolution` (1K, 2K, 4K), `result_type` (`single` for 1–9 independent images via `num_images`, or `series` for 2–9 related frames via `series_amount`), `aspect_ratio` (including `auto`, which infers a ratio from the inputs) and `output_format`. Reference images are .jpg, .png or .webp.

Typical outputs are photoreal or stylised stills at up to 4K. Practical limits: at most ten references per call, the prompt is capped at 2,500 characters, and, as with any reference-driven model, results degrade when references conflict in lighting or perspective, so pick clean, well-lit sources.

The hosted endpoint used by this client is `kling/kling-image-o3`, which is Kling's own Omni 3 model served through Synexa; this client is not a reimplementation and there are no open weights to self-host. The product and its official documentation are at https://kling.ai.

**Official project:** https://kling.ai

## Use cases

- **Product catalogue variants** — pass a packshot as `@Image1` and prompt for it on different backgrounds or in different colours, with `num_images=4`.
- **Consistent character art** — supply a character sheet and request a `series` of 6 frames showing the same character in a sequence of scenes.
- **Virtual try-on style composites** — reference a garment and a model photo in the same prompt and ask for the garment worn by the model.
- **Campaign key visuals at 4K** — render a hero image at `resolution="4K"` for print after iterating cheaply at 1K.
- **Storyboards** — turn a location reference plus a prop reference into a 9-frame series, then hand the frames to a video model.
- **Bulk localisation** — submit hundreds of `wait=False` predictions that swap backgrounds per market and collect results by webhook.

## FAQ

**Is there a Kling Omni API?**

Yes. Kling Omni 3 is available as the hosted model `kling/kling-image-o3`, and this client wraps that endpoint so you can call it from Python with `run()`.

**How much does the Kling Omni API cost?**

$0.028 per run through the hosted endpoint, regardless of resolution. Billing is per prediction; there is no subscription or idle GPU cost.

**Can I run Kling Omni without a GPU?**

Yes. All generation happens on the hosted service. Your code makes HTTPS requests only, so it runs on a laptop, a serverless function or a CI job.

**Does this client work with the Kling web app or ComfyUI?**

No. It does not log into kling.ai and it is not a ComfyUI node. It talks to the hosted `kling/kling-image-o3` endpoint over HTTP. Kling Omni has no open weights, so there is nothing to load locally.

**What input formats does it accept?**

`prompt` (text, up to 2,500 characters, referencing images as `@Image1`, `@Image2`, ...) and `image_urls` (a list of up to 10 publicly reachable .jpg/.png/.webp URLs). Optional fields control resolution (1K/2K/4K), single vs series output, image count, aspect ratio and output format.

**Is this the official Kling Omni SDK?**

No. This is an independent client and is not affiliated with or endorsed by Kuaishou or Kling AI. The official product is at https://kling.ai.

## Related

- [Kling AI (official site)](https://kling.ai) — product documentation and web app.
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose client this package wraps.
- [kling/kling-image-o3](https://synexa.ai/explore/kling/kling-image-o3) — the hosted Kling Omni 3 model behind this client.

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Kling Omni. Model weights and trademarks belong to their respective owners.


_Last reviewed: 2026-09-22_

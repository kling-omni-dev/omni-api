        """Minimal Kling Omni example: create one prediction and print the output URL(s)."""
        import omni_api

        output = omni_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light",
    "image_urls": [
        "https://example.com/input.png"
    ]
})
        print(output)

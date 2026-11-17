# Safety defaults

Content
- No harassment, slurs, or jokes at the expense of protected groups.
- No private individuals; no real people's faces added to custom images without their consent.
- No tragedies, self-harm, violence, or sexual content.
- No claims of fact you have not verified.
- Memes may carry the memegen.link watermark; keep it and credit the service when posting.

Technical
- Only https requests to the configured image host (default api.memegen.link); redirects cannot leave it.
- Downloads are capped at 12 MB and must be real PNG/JPEG/GIF/WebP images; with Pillow they are decoded and re-encoded.
- Caption text is sent to the image service to render the meme. Do not include secrets or personal data.
- Local images never leave your machine (Pillow overlay). Only an https URL background is fetched by the service.
- The CLI never reads or writes outside the output folder you choose.

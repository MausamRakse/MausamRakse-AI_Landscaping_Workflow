import google.generativeai as genai
import json
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import re

text_model = None
vision_model = None

def init_gemini(api_key):
    """
    Initializes the Google Gemini API clients by finding available models.
    """
    global text_model, vision_model
    genai.configure(api_key=api_key)

    # Find the first available model that supports content generation
    model_name = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            print(f"Found and using model: {model_name}")
            break
    
    if model_name:
        text_model = genai.GenerativeModel(model_name)
        vision_model = genai.GenerativeModel(model_name) # Use the same model for vision
    else:
        raise Exception("Could not find an available generative model.")

def _parse_json_output(text):
    """
    A helper function to parse Gemini's JSON output.
    """
    cleaned_text = text.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {cleaned_text}")
        raise ValueError("Gemini returned malformed JSON.") from e

def generate_text(prompt):
    """
    Generates text using the Gemini text model.
    """
    if not text_model:
        raise Exception("Gemini not initialized. Call init_gemini(api_key) first.")
    
    response = text_model.generate_content(prompt)
    return _parse_json_output(response.text)

def analyze_image(image_base64, mime_type, prompt):
    """
    Analyzes an image with a text prompt using the Gemini vision model.
    """
    if not vision_model:
        raise Exception("Gemini not initialized. Call init_gemini(api_key) first.")

    image_parts = [{
        "mime_type": mime_type,
        "data": base64.b64decode(image_base64)
    }]
    
    response = vision_model.generate_content([prompt, image_parts[0]])
    return response.text

def analyze_image_and_get_json(image_base64, mime_type, prompt):
    """
    Analyzes an image and expects a JSON response.
    """
    text_response = analyze_image(image_base64, mime_type, prompt)
    return _parse_json_output(text_response)

def generate_image(prompt):
    """
    Generates an image using a hypothetical Gemini Image Generation model.
    NOTE: This is a placeholder function. This version creates a more 
    descriptive placeholder image instead of a black square.
    """
    print(f"[Image Generation Stub] Generating image for prompt: \"{prompt[:100]}...\"")

    W, H = (600, 400)
    img = Image.new('RGB', (W, H), color='#E0E0E0') # Light gray background
    d = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("DejaVuSans.ttf", 40)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Extract theme from prompt for context
    theme_name = "Generic Theme"
    match = re.search(r"Landscape Theme: (.*?)\n", prompt)
    if match:
        theme_name = match.group(1)
    else:
        match = re.search(r"in the (.*?) style", prompt)
        if match:
            theme_name = match.group(1)

    title_text = "Placeholder Image"
    theme_text = f"Theme: {theme_name}"

    _, _, w_title, h_title = d.textbbox((0, 0), title_text, font=font_large)
    _, _, w_theme, h_theme = d.textbbox((0, 0), theme_text, font=font_small)

    d.text(((W - w_title) / 2, (H - h_title) / 2 - 20), title_text, font=font_large, fill=(0, 0, 0))
    d.text(((W - w_theme) / 2, (H - h_theme) / 2 + 30), theme_text, font=font_small, fill=(50, 50, 50))

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return base64.b64encode(byte_im).decode('utf-8')

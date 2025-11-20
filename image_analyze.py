import requests
from openai import OpenAI
from PIL import Image
import base64
import io

api_key = "your_api_key_here"
def encode_image_to_base64(image_path: str) -> str:
    """Encodes an image to base64 string."""
    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


def analyze_image_with_qwen(image_path: str, prompt: str = "Describe this image.") -> str:
    """
    Sends an image and a prompt to the specified model via SGLang.

    Args:
        image_path: Path to the image file.
        prompt: Prompt text to instruct the model.

    Returns:
        The model's response.
    """
    base64_img = encode_image_to_base64(image_path)

    # SGLang endpoint for completion
    endpoint = "your_endpoint_here"
    
    client = OpenAI(api_key=api_key, base_url=endpoint)

    try:
        response = client.chat.completions.create(
            model="your_model",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": "what's in this image?" },
                        {
                            "type": "image_url",
                            "image_url": { "url": f"data:image/jpeg;base64,{base64_img}"
                            },
                        },
                    ],
                }
            ]
        )

        return (response.choices[0].message.content)

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    
if __name__ == "__main__":
    image_path = "your_image_here.jpg"  # Replace with your image path
    prompt = "Describe this image."
    
    response_text = analyze_image_with_qwen(image_path, prompt)
    print("Response from specified model:")
    print(response_text)

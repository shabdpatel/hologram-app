import sys
from PIL import Image

def process_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Example processing: convert image to grayscale
        processed_img = img.convert("L")
        # Save the processed image with a new name
        processed_image_path = image_path.replace('.', '_processed.')
        processed_img.save(processed_image_path)
        return processed_image_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    processed_image_path = process_image(image_path)
    print(f"Processed image saved to {processed_image_path}")

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def generate_hologram(target_image, iterations):
    # Initialize the shape of the hologram based on the target image
    hologram_shape = target_image.shape
    
    # Create an initial random phase distribution for the hologram
    hologram = np.exp(1j * np.random.rand(*hologram_shape))  # 1j represents the imaginary unit
    
    # Define the step size for the gradient descent algorithm
    step_size = 0.01  # Smaller step size means finer adjustments

    for i in range(iterations):
        # Apply the Fourier Transform to convert the hologram into the frequency domain
        reconstructed_image = np.fft.fftshift(np.fft.fft2(hologram))

        # Calculate the error by comparing the magnitude of the reconstructed image to the target image
        error = np.abs(np.abs(reconstructed_image) ** 2 - np.abs(target_image) ** 2)

        # Adjust the reconstructed image by the difference between it and the target image
        multiplied_result = reconstructed_image * (np.abs(reconstructed_image) - np.abs(target_image))

        # Apply the Inverse Fourier Transform to convert back to the spatial domain
        inverse_transform = np.fft.ifft2(np.fft.ifftshift(multiplied_result))

        # Update the phase distribution of the hologram using the angle from the inverse transform result
        revised_phase = hologram * np.angle(inverse_transform)

        # Calculate the gradient (direction and rate of change) for updating the hologram
        gradient = -4 * np.imag(revised_phase)  # Using the imaginary part for phase update

        # Update the hologram phase distribution using gradient descent
        hologram = hologram - step_size * gradient

    return hologram

def preprocess_image(image_path, desired_shape):
    # Load the image from the specified path and resize it to the desired shape
    image = Image.open(image_path).resize(desired_shape)

    # Convert the image to grayscale (black and white)
    image = image.convert("L")

    # Normalize the pixel values to a range between 0 and 1
    image = np.array(image) / 255.0

    return image

# Example usage
image_path = "/mnt/sdb4/CSIR Intern/Results/CSIO_oa_1024x1024.bmp"
desired_shape = (256, 256)  # Resize image to 256x256 pixels

# Preprocess the image: load, resize, convert to grayscale, and normalize
image = preprocess_image(image_path, desired_shape)

# Define the number of iterations for generating the hologram
iterations = 100

# Generate the hologram using the preprocessed image and specified iterations
hologram = generate_hologram(image, iterations)

# Display the generated hologram
plt.imshow(np.abs(hologram), cmap='gray')
plt.title("Generated Hologram")
plt.axis('off')  # Hide the axis for better visualization
plt.show()

# Reconstruct the image from the generated hologram
reconstructed_image = np.fft.ifft2(np.fft.ifftshift(hologram))

# Display the reconstructed image
plt.imshow(np.abs(reconstructed_image), cmap='gray')
plt.title("Reconstructed Image")
plt.axis('off')  # Hide the axis for better visualization
plt.show()

import numpy as np
import matplotlib.pyplot as plt


def generate_hologram(target_image, iterations):
    # Initialize variables
    hologram_shape = target_image.shape
    hologram = np.exp(1j * np.random.rand(*hologram_shape))  # Random phase distribution
    step_size = 0.01  # Step length coefficient

    for i in range(iterations):
        # Fourier Transform
        reconstructed_image = np.fft.fftshift(np.fft.fft2(hologram))

        # Error Calculation
        error = np.abs(np.abs(reconstructed_image) ** 2 - np.abs(target_image) ** 2)

        # Multiply
        multiplied_result = reconstructed_image * (np.abs(reconstructed_image) -
                                                   np.abs(target_image))

        # Inverse Fourier Transform
        inverse_transform = np.fft.ifft2(np.fft.ifftshift(multiplied_result))

        # Multiply with Previous Iteration
        revised_phase = hologram * np.angle(inverse_transform)

        # Extract Imaginary Part and Multiply
        gradient = -4 * np.imag(revised_phase)

        # Update Phase Distribution
        hologram = hologram - step_size * gradient

    return hologram


# Example usage
from PIL import Image


def preprocess_image(image_path, desired_shape):
    # Load image and resize
    image = Image.open(image_path).resize(desired_shape)

    # Convert to grayscale
    image = image.convert("L")

    # Normalize pixel values between 0 and 1
    image = np.array(image) / 255.0

    return image


# Example usage
image_path = "/mnt/sdb4/CSIR Intern/Results/CSIO_oa_1024x1024.bmp"
desired_shape = (256, 256)  # Adjust to your desired hologram shape

# Preprocess the image
image = preprocess_image(image_path, desired_shape)
iterations = 100
# Use the generated hologram code
hologram = generate_hologram(image, iterations)

# Assuming 'hologram' contains the generated hologram data
plt.imshow(np.abs(hologram), cmap='gray')
plt.title("Generated Hologram")
plt.axis('off')
plt.show()
reconstructed_image = np.fft.ifft2(np.fft.ifftshift(hologram))

plt.imshow(np.abs(reconstructed_image), cmap='gray')
plt.title("Reconstructed Image")
plt.axis('off')
plt.show()
""" --------LIBRARIES-----------------""" 
import numpy as np  # Importing numpy library for numerical computations
import matplotlib.pyplot as plt  # Importing matplotlib for plotting
import cv2  # Importing OpenCV for image processing
import time  # Importing time module for time-related 
import sys

""" ----------------------------------""" 
def chlo(obj_file):
    # Initialize lists to store results of multiple iterations
    mse_values_f = []  # List to store Mean Squared Error values
    cad_f = []  # List to store the Fourier Transformed CAD results
    holo_f = []  # List to store hologram data

    # Perform the following process 5 times
    for _ in range(5):
        """ ----------------   Section - Setup the Parameters of the optical system   ---------------- """
        
        lamda = 532.e-9  # Wavelength of the laser in meters
        z = 1  # Distance parameter (could represent propagation distance)
        delta_x, delta_y = 6.4e-6, 6.4e-6  # Pixel pitch in meters
        x_dim = 1024  # Dimension of the image along x-axis
        y_dim = x_dim  # Dimension of the image along y-axis (same as x-axis)
        SLM_res_x = 1920  # Spatial Light Modulator resolution along x-axis
        SLM_res_y = 1080  # Spatial Light Modulator resolution along y-axis
        bit_depth = 8  # Bit depth for quantization
        q_level = (2**bit_depth - 1)  # Quantization levels
        max_g = 255  # Maximum grayscale value
        limit = 8  # Number of iterations
        SSE = []  # List to store Sum of Squared Errors (SSE)
        CGH_type = "Fourier"  # Type of Computer-Generated Holography
        
        
        """ ------------------------------------------------------------------------------------------- """
        
        # Function to read an object file and return its grayscale and intensity
        def object_read(object_file):
            gray_double = np.float64(cv2.imread(object_file, 0))  # Read image in grayscale and convert to float64
            Int_double = gray_double**2  # Calculate intensity by squaring the grayscale values
            return (gray_double, Int_double)
        
        # Read the object file
        obj_gray_doub, Int_gray_doub = object_read(obj_file)
        
        # Function to get pixel coordinates of the image
        def pix_coordi(object_file_doub):
            width, height = object_file_doub.shape[1], object_file_doub.shape[0]  # Get image dimensions
            coordi_X, coordi_Y = np.meshgrid(np.arange(-width/2, width/2, 1, dtype=int), np.arange(-height/2, height/2, 1, dtype=int))  # Create meshgrid for coordinates
            return (coordi_X, coordi_Y, width, height)
        
        # Get pixel coordinates of the object image
        X, Y, width, height = pix_coordi(obj_gray_doub)
        w_into_h = width * height  # Total number of pixels in the image
        
        """-----Function 3a: To quantize a phase or amplitude CGH array ----"""
        
        # Function to quantize a CGH array
        def quantize_arr(CGH_arr, mode_qua):
            if(mode_qua == "angle"):
                CGH_ph = np.angle(CGH_arr) + np.pi  # Get the phase and adjust to range [0, 2π]
                # 8-bit Quantization
                CGH = np.uint8(np.round(CGH_ph * (q_level / np.amax(CGH_ph))))  # Quantize the phase
            return(CGH)
        
        """------------------------------------------------------------------"""
        
        """Function 3b: To convert a quantized phase CGH into a complex unit amplitude distribution"""
        
        # Function to convert a quantized phase CGH to a complex amplitude
        def qphi2exp(CGH_ph, mode_exp):
            CGH_quant = (CGH_ph * (2 * np.pi / max_g)) - np.pi  # Convert quantized phase back to original range
            if(mode_exp == "For_Pro"):
                CGH_exp = np.exp(1j * CGH_quant)  # Forward propagation complex amplitude
            if (mode_exp == "Back_Pro"):
                CGH_exp = np.exp(-1j * CGH_quant)  # Backward propagation complex amplitude
            return(CGH_exp)
        
        """--------------------------------------------------------------------------------------------"""
        
        # Get the current time for file naming purposes
        t = time.localtime()
        current_time = time.strftime("%H.%M.%S", t)
        start_time = time.time()  # Record start time
        
        """---------RANDOM NUMBER---------------"""
        """-------------------------------------"""
        
        # Generate a random initial hologram
        Rand_no = np.random.uniform(0, 1, size=(height, width))  # Generate random numbers between 0 and 1
        hologram = np.exp(-1j * (Rand_no - 0.5) * 2 * np.pi)  # Create a random complex hologram
        
        count = 1  # Initialize iteration counter
        
        """--------------------------------------------------------------------------------------------"""
        """----------------------------------LOOP FOR ITERATIONS---------------------------------------"""
        """--------------------------------------------------------------------------------------------"""
        
        # Initialize lists to store results of each iteration
        mse_values = []  # List to store MSE values for each iteration
        cad = []  # List to store CAD results for each iteration
        holo = []  # List to store holograms for each iteration
        
        # Loop for the specified number of iterations
        for count in range(limit):
            # Forward Propagation
            recon_cad_FT = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(hologram)))  # Perform inverse FFT to get the reconstructed CAD
            cad.append(recon_cad_FT)  # Store the reconstructed CAD
            Int_recon = abs(recon_cad_FT)**2  # Calculate intensity of the reconstructed CAD
            error = (Int_gray_doub - Int_recon)  # Calculate error between original and reconstructed intensity
            error_norm = (Int_gray_doub / np.amax(Int_gray_doub)) - (Int_recon / np.amax(Int_recon))  # Normalize the error
            mse =  (np.sum(error_norm**2) / w_into_h)  # Calculate Mean Squared Error
            # mse_values.append(mse)  # Append MSE value to the list
            
            # Backward Propagation
            err_into_recon = error * recon_cad_FT  # Multiply error with reconstructed CAD
            hologram_IFT = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(err_into_recon)))  # Perform FFT to get back to hologram space
            
            # Quantize and convert phase
            CGH_phase_q = quantize_arr(hologram_IFT, "angle")  # Quantize the phase of the hologram
            CGH_phase_FP = qphi2exp(CGH_phase_q, "Back_Pro")  # Convert quantized phase back to complex amplitude
            
            gradient_mse = -4 * np.imag(CGH_phase_FP * hologram_IFT)  # Calculate gradient of MSE
            
            # Optimized step size
            grad_holo = -gradient_mse * np.reciprocal(hologram, dtype=complex)  # Calculate gradient of hologram
            F_grad_holo = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(grad_holo)))  # Perform inverse FFT on gradient
            
            img_gamma = np.imag(np.conj(F_grad_holo) * recon_cad_FT)  # Calculate imaginary part of product
            gamma_num = np.sum(error * img_gamma)  # Numerator for step size calculation
            gamma_den = 2 * np.sum(img_gamma**2)  # Denominator for step size calculation
            step_size = gamma_num / gamma_den  # Calculate step size
            # stp_lngth.append(step_size)  # Append step size to the list
            
            # Update Phase Distribution
            hologram = hologram - step_size * gradient_mse  # Update hologram with gradient descent
            holo.append(hologram)  # Store updated hologram
            
            """--------------TO SAVE CGH AND NRI FOR EVERY ITERATION -----------------""" 
            # Save the current iteration results as images
            # plt.imsave(f'{current_time}_CGH_{count+1}.bmp', np.angle(hologram), cmap='gray')
            # plt.imsave(f'{current_time}_NRI_{count+1}.bmp', abs(recon_cad_FT), cmap='gray')
            # plt.imsave(f'a{count+1}.bmp', abs(recon_cad_FT), cmap='gray')
            # imagess = abs(recon_cad_FT), cmap='gray'
            """-----------------------------------------------------------------------"""   
            
            # Calculate Mean Squared Error between original and current reconstructed image
            array = cad[count]  # Get the current CAD result
            image = cv2.imread(obj_file)  # Read the original image
            image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert original image to grayscale
            
            array2 = np.abs(array)  # Get the magnitude of the current CAD result
            max_value = array2.max()  # Get the maximum value of the magnitude
            scaling_factor = 255 / max_value  # Calculate scaling factor
            scaled_array = array2 * scaling_factor  # Scale the array
            array2 = scaled_array.round().astype(np.uint8)  # Convert to 8-bit integer
            
            squared_diff = (image1.astype("float") - array2.astype("float")) ** 2  # Calculate squared differences
            msee_value = np.mean(squared_diff)  # Calculate Mean Squared Error
            mse_values.append(msee_value)  # Append MSE value to the list
            
            # Compare the image and array using MSE
            print(f"MSE{count+1}:", msee_value)
        
        # Store results of the current run
        mse_values_f.extend(mse_values)  # Add current MSE values to final list
        cad_f.extend(cad)  # Add current CAD results to final list
        holo_f.extend(holo)  # Add current holograms to final list
        
        print("done")

    """-------------------TO PLOT MSE VS ITERATION--------------------------""" 
    # Plot and save MSE vs iteration graph
    # count_numbers = np.arange(1, limit+1)
    # plt.plot(count_numbers, mse_values)
    # plt.xlabel('iteration')
    # plt.ylabel('MSE')
    # plt.title('MSE vs iteration')
    # plt.grid(True)
    # plt.savefig(f'{current_time}mse.png')
    """---------------------------------------------------------------------"""

    """-----------------TO SAVE CGH AND NRI FOR MIN MSE---------------------""" 
    mse_min = min(mse_values_f)  # Find minimum MSE value
    inde_ = mse_values_f.index(mse_min)  # Find index of minimum MSE
    print(mse_min)  # Print minimum MSE value
    print(inde_+1)  # Print iteration number corresponding to minimum MSE
    plt.imsave(f'{current_time}_numeri_re.bmp', abs(cad_f[inde_]), cmap='gray')  # Save corresponding CAD result
    plt.imsave(f'{current_time}_cgh.bmp', np.angle(holo_f[inde_]), cmap='gray')  # Save corresponding hologram
    """---------------------------------------------------------------------"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    processed_image_path = chlo(image_path)
    print(f"Processed image saved to {processed_image_path}")
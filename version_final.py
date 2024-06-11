
""" --------LIBRARIES-----------------""" 
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time

""" ----------------------------------""" 

mse_values_f = []
cad_f = []
holo_f = []
    
for _ in range(5):
     
    
       
    """ ----------------   Section - Setup the Parameters of the optical system   ---------------- """
    
    lamda=532.e-9;                 z=1.;                  delta_x, delta_y = 6.4e-6, 6.4e-6
    
    x_dim = 1024;                  y_dim = x_dim;          SLM_res_x = 1920;            SLM_res_y = 1080 
    
    bit_depth = 8;                 q_level = (2**bit_depth - 1);                       max_g = 255.
    
    limit =8;  '''this is number of iterations'''                                         
    SSE=[];                 
       
    CGH_type = "Fourier"       
    
    obj_file = "/mnt/sdb4/CSIR Intern/Results/CSIO_oa_1024x1024.bmp" 
    
    """ ------------------------------------------------------------------------------------------- """
    
    
    
    def object_read(object_file):
        gray_double = np.float64(cv2.imread(object_file,0))
        Int_double = gray_double**2
        return (gray_double, Int_double)
    
    
    obj_gray_doub, Int_gray_doub = object_read(obj_file)
    
    
    def pix_coordi(object_file_doub):
        width, height = object_file_doub.shape[1], object_file_doub.shape[0]     
        coordi_X, coordi_Y = np.meshgrid(np.arange(-width/2,width/2,1,dtype=int), np.arange(-height/2,height/2,1,dtype=int))
        return (coordi_X, coordi_Y, width, height)
    
    X, Y, width, height = pix_coordi(obj_gray_doub)      
    w_into_h = width*height        
    
    """-----Function 3a: To quantize a phase or amplitude CGH array ----"""
    
    def quantize_arr(CGH_arr, mode_qua):
        if(mode_qua=="angle"):
            CGH_ph=np.angle(CGH_arr)+np.pi
            ## 8-bit Quantization
            CGH=np.uint8(np.round(CGH_ph*(q_level/np.amax(CGH_ph))))                    
        return(CGH)
    """------------------------------------------------------------------"""
    
    
    
    """Function 3b: To convert a quantized phase CGH into a complex unit amplitude distribution"""
    
    def qphi2exp(CGH_ph, mode_exp):
        CGH_quant=(CGH_ph*(2*np.pi/max_g))-np.pi
        if(mode_exp=="For_Pro"):
            CGH_exp=np.exp(1j*CGH_quant)
        if (mode_exp=="Back_Pro"):
            CGH_exp=np.exp(-1j*CGH_quant)
        return(CGH_exp)
    """--------------------------------------------------------------------------------------------"""
    
    
     
    t = time.localtime()
    current_time = time.strftime("%H.%M.%S", t)
    start_time = time.time()
    """---------RANDOM NUMBER---------------"""
    """-------------------------------------"""
    Rand_no = np.random.uniform(0, 1, size=(height, width))
    hologram=np.exp(-1j*(Rand_no-0.5)*2*np.pi)  
    
    
       
    count = 1
    
    
    
    
    
    
    """--------------------------------------------------------------------------------------------"""
    """----------------------------------LOOP FOR ITERATIONS---------------------------------------"""
    """--------------------------------------------------------------------------------------------"""
    mse_values = []
    cad = []
    holo = [] 
    
    for count in range(limit):
                     
    # Forward Propagation
        recon_cad_FT = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(hologram)))
        cad.append(recon_cad_FT)
        Int_recon = abs(recon_cad_FT)**2
        error = (Int_gray_doub - Int_recon)
        #np.savetxt(f"Err_{current_time}.csv", error, delimiter=",")    
        error_norm = (Int_gray_doub/np.amax(Int_gray_doub)) - (Int_recon/np.amax(Int_recon))
        mse =  (np.sum(error_norm**2)/w_into_h)
        #np.savetxt(f"MSE_{current_time}.csv", [mse], fmt='%.8f')
        #print("Max of error: ", np.amax(error), "Min of error: ", np.amin(error), "Max of error_norm: ", np.amax(error_norm), "Min of error_norm: ", np.amin(error_norm), "Mean Square Error is", mse)
        # mse_values.append(mse)
        
        
        
        
    # Backward Propagation
        err_into_recon = error*recon_cad_FT
        hologram_IFT = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(err_into_recon)))
        
        CGH_phase_q = quantize_arr(hologram_IFT, "angle")
        CGH_phase_FP = qphi2exp(CGH_phase_q, "Back_Pro")
    
        gradient_mse = -4*np.imag(CGH_phase_FP*hologram_IFT)
    
        
    
    
    # Optimized step size
        grad_holo = -gradient_mse*np.reciprocal(hologram, dtype=complex)
        F_grad_holo = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(grad_holo)))
                            
        img_gamma = np.imag(np.conj(F_grad_holo) * recon_cad_FT)
        gamma_num = np.sum(error*img_gamma)
        gamma_den = 2*np.sum(img_gamma**2)
        step_size = gamma_num/gamma_den  #0.9  # Step length coefficient
        #print("gamma_num, gamma_den and step_size are:", gamma_num, gamma_den, step_size)
        #stp_lngth.append(step_size)
        
       
    
    # Update Phase Distribution
    
        hologram = hologram - step_size * gradient_mse
        holo.append(hologram)
        
        
        """--------------TO SAVE CGH AND NRI FOR EVERY ITERATION -----------------""" 
        #plt.imsave(f'{current_time}_CGH_{count+1}.bmp', np.angle(hologram), cmap='gray')
        # plt.imsave(f'{current_time}_NRI_{count+1}.bmp', abs(recon_cad_FT), cmap='gray')
        # plt.imsave(f'a{count+1}.bmp', abs(recon_cad_FT), cmap='gray')
        # imagess = abs(recon_cad_FT), cmap='gray'
        """-----------------------------------------------------------------------"""   
        array = cad[count]
        image = cv2.imread(obj_file)    
        image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
            
        array2 = np.abs(array)
        max_value = array2.max()
        scaling_factor = 255 / max_value
        scaled_array = array2 * scaling_factor
        array2 = scaled_array.round().astype(np.uint8)
    
            # array2 = cv2.cvtColor(array2, cv2.COLOR_GRAY2BGR)
        squared_diff = (image1.astype("float") - array2.astype("float")) ** 2
        msee_value = np.mean(squared_diff)
        mse_values.append(msee_value)
    
        # Load the image
        
    
        # Create a complex arraycad[]
        
        # plt.imsave(f'{msee_value}.bmp', abs(array), cmap='gray')
        # Compare the image and array using MSE
        
        print(f"MSE{count+1}:", msee_value)
        
    mse_values_f.extend(mse_values)
    cad_f.extend(cad)
    holo_f.extend(holo)
        
    print("done")
    """--------------------------------------------------------------------------------------------"""
    """--------------------------------------------------------------------------------------------"""
    """--------------------------------------------------------------------------------------------"""
    
    
    
    
    
    
    
    """-------------------TO PLOT MSE VS ITERATION--------------------------""" 
    # count_numbers = np.arange(1, limit+1)
    # plt.plot(count_numbers, mse_values)
    # plt.xlabel('iteration')
    # plt.ylabel('MSE')
    # plt.title('MSE vs iteration')
    # plt.grid(True)
    # plt.savefig(f'{current_time}mse.png')
    """---------------------------------------------------------------------"""
    
    
    
    
    
    """-----------------TO SAVE CGH AND NRI FOR MIN MSE---------------------""" 
mse_min= min(mse_values_f)
inde_=mse_values_f.index(mse_min)
print(mse_min)
print(inde_+1)
plt.imsave(f'{current_time}_numeri_Re{mse_min}.bmp', abs(cad_f[inde_]), cmap='gray')
plt.imsave(f'{current_time}_cgh.bmp', np.angle(holo_f[inde_]), cmap='gray')
"""---------------------------------------------------------------------"""
    
    
        
        
        
    
    
    
    
    
    
    
    
    
        

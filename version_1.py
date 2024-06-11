

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print("Start time is:", current_time)

start_time = time.time()

""" ----------------   Section - Setup the Parameters of the optical system   ---------------- """

lamda=532.e-9;                 z=1.;                  delta_x, delta_y = 6.4e-6, 6.4e-6

x_dim = 1024;                  y_dim = x_dim;         SLM_res_x = 1920;              SLM_res_y = 1080 
bit_depth = 8;                 q_level = (2**bit_depth - 1);                         max_g = 255.

limit = 10;                    SSE=[];                 obj_file = "/mnt/sdb4/CSIR Intern/Results/CSIO_oa_1024x1024.bmp"    #"Opera_1024x1024.bmp"     
CGH_type = "Fourier"       



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

# Function 3a: To quantize a phase or amplitude CGH array 
def quantize_arr(CGH_arr, mode_qua):
    if(mode_qua=="angle"):
        CGH_ph=np.angle(CGH_arr)+np.pi
        ## 8-bit Quantization
        CGH=np.uint8(np.round(CGH_ph*(q_level/np.amax(CGH_ph))))                    
    return(CGH)

# Function 3b: To convert a quantized phase CGH into a complex unit amplitude distribution
def qphi2exp(CGH_ph, mode_exp):
    CGH_quant=(CGH_ph*(2*np.pi/max_g))-np.pi
    if(mode_exp=="For_Pro"):
        CGH_exp=np.exp(1j*CGH_quant)
    if (mode_exp=="Back_Pro"):
        CGH_exp=np.exp(-1j*CGH_quant)
    return(CGH_exp)

    
#phases_LB()
#hologram=np.exp(-1j*(np.random.rand(height, width)))
hologram=np.exp(-1j*(np.random.rand(height, width)-0.5)*2*np.pi)    

#def slo_mod_LB_GD(obj_gray_ph):
for count in range(limit):            
    ## Forward Propagation
    recon_cad_FT = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(hologram)))
    Int_recon = abs(recon_cad_FT)**2
    error = (Int_gray_doub - Int_recon)
    error_norm = (Int_gray_doub/np.amax(Int_gray_doub)) - (Int_recon/np.amax(Int_recon))
    mse =  (np.sum(error_norm**2)/w_into_h)
    #print("Max of error: ", np.amax(error), "Min of error: ", np.amin(error), "Max of error_norm: ", np.amax(error_norm), "Min of error_norm: ", np.amin(error_norm), "Mean Square Error is", mse)

    ## Backward Propagation
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

    # Update Phase Distribution
    hologram = hologram - step_size * gradient_mse

print("done")
plt.imsave('1a.xxx_GeneratedHologram_GD_new.bmp', np.angle(hologram), cmap='gray')
plt.imsave('1b.xxx_ReconstructedObject_GD_new.bmp', abs(recon_cad_FT), cmap='gray')

#return(CGH_phase_FP, recon_obj_gray_ph)




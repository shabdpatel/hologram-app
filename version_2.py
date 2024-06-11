"""----------------LIBRARIES-----------------"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import pandas as pd
"""----------------------------------------"""




for _ in range(1,5):
    
    
    """---------------------TIME---------------"""
    
    t = time.localtime()
    current_time = time.strftime("%H.%M.%S", t)
    # print("Start time is:", current_time)
    start_time = time.time()
    
    """----------------------------------------"""
    
    
    
    
    
    
    """ ----------------   Section - Setup the Parameters of the optical system   ---------------- """
    
    lamda=532.e-9;                 z=1.;                  delta_x, delta_y = 6.4e-6, 6.4e-6
    
    x_dim = 1024;                  y_dim = x_dim;         SLM_res_x = 1920;              SLM_res_y = 1080
     
    bit_depth = 8;                 q_level = (2**bit_depth - 1);                         max_g = 255.
    
    limit_GS =4;               limit_GD =12;                                         SSE=[];                 
            
    obj_file = "/mnt/sdb4/CSIR Intern/Results/CSIO_oa_1024x1024.bmp" ;                                                 CGH_type = "Fourier"
    
    """---------------------------------------------------------------------------------------------"""
    
    
    
    
    
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
       
    Rand_ph_GS=np.exp(-1j*(np.random.rand(height, width)-0.5)*2*np.pi)
    # Function 3a: To quantize a phase or amplitude CGH array 
    def quantize_arr(CGH_arr, mode_qua):
        if(mode_qua=="angle"):
            CGH_ph=np.angle(CGH_arr)+np.pi
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
    
        
    obj_gray_ph = obj_gray_doub*Rand_ph_GS
    obj_abs_doub = np.abs(obj_gray_doub)
    obj_SSE_doub = obj_abs_doub/np.amax(obj_abs_doub)
    
    
    def slo_mod_LB_GS(obj_gray_ph):
        for count in range(limit_GS):            
            ## Forward Propagation
            Fourier_Trans_FP = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(obj_gray_ph)))
            CGH_phase_q = quantize_arr(Fourier_Trans_FP, "angle")
            CGH_phase_FP = qphi2exp(CGH_phase_q, "For_Pro")
    
            ## Backward Propagation
            obj_gray_ph = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(CGH_phase_FP)))
            recon_obj_abs_ph = np.abs(obj_gray_ph)                  
    
            ## Reconstruction plane (or Image plane) constraint
            obj_gray_ph=np.multiply((np.divide(obj_gray_ph, recon_obj_abs_ph)),obj_gray_doub)
    
            ## Error Calculation - SSE part can be enabled or disabled by if condition as per the requirement
            if(count>limit_GS-2):
                obj_SSE_ph = recon_obj_abs_ph/np.amax(recon_obj_abs_ph)
                SSE_p = np.power((obj_SSE_ph - obj_SSE_doub),2)
                SSE.append(np.sum(SSE_p)/w_into_h)
               
    
            ## Final reconstructed image is np.abs(obj_gray_ph) - will be taken out only at the end of loop
            if(count>limit_GS-2):
                recon_obj_gray_ph = recon_obj_abs_ph
               
    
        return(CGH_phase_FP, recon_obj_gray_ph)
    
    
    
    # CGH_phase_FP, recon_obj_gray_ph = slo_mod_LB_GS(obj_gray_ph)
    # np.savetxt(f"array{current_time}_cgh_GS_limit{limit_GS}.csv",CGH_phase_FP, delimiter= ",")
    
    # plt.imsave(f'{current_time}_NR_.bmp', recon_obj_gray_ph, cmap='gray')
    # rotated = np.rot90(CGH_phase_FP, 2)
    # # rotated_NR =  np.rot90( recon_obj_gray_ph, 2)
    # # plt.imsave(f'{current_time}_NR_.bmp',rotated_NR, cmap='gray')
    # added = CGH_phase_FP + rotated
    # # added_NR =  recon_obj_gray_ph + rotated_NR
    # # plt.imsave(f'{current_time}_NR_GS.bmp',added_NR, cmap='gray')
    
    
    mse_values = [];     cad = [];     cghs = [];        count = 1
    
    def slo_mod_LB_GD(obj_gray_ph,hologram):
        for count in range(limit_GD):                 
            ## Forward Propagation
            recon_cad_FT = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(hologram)))
            
            cad.append(recon_cad_FT)
            cghs.append(hologram)
            
            Int_recon = abs(recon_cad_FT)**2
            error = (Int_gray_doub - Int_recon)
            error_norm = (Int_gray_doub/np.amax(Int_gray_doub)) - (Int_recon/np.amax(Int_recon))
            mse =  (np.sum(error_norm**2)/w_into_h)
            mse_values.append(mse)
            
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
            step_size = gamma_num/gamma_den
            
           
        
            # Update Phase Distribution
            hologram = hologram - step_size * gradient_mse
            # plt.imsave(f'{current_time}_CGH_{count+1}.bmp', np.angle(hologram), cmap='gray')
            plt.imsave(f'{current_time}_NR_{count+1}.bmp', abs(recon_cad_FT), cmap='gray')
        
        return(hologram, abs(recon_cad_FT))  
    
        
    added = np.genfromtxt("array18.09.47_cgh_GS_limit4.csv", delimiter=',')
    hologram, recon_obj = slo_mod_LB_GD(obj_gray_ph,added)
    
    
    """ ----------------TO PLOT MSE VS ITERATION---------------- """
    count_numbers = np.arange(1, limit_GD+1)
    plt.plot(count_numbers, mse_values)
    plt.xlabel('iteration')
    plt.ylabel('MSE')
    plt.title('MSE vs iteration')
    plt.grid(True)
    plt.savefig(f'{current_time}___MSE.png')
    """ -------------------------------------------------------- """
    
    
    
    
    """ ----------TO SAVE CGH AND NRI WITH MINIMUM MSE----------- """
    mse_min= min(mse_values)
    inde_=mse_values.index(mse_min)
    print(mse_min)
    print(inde_+1)
    plt.imsave(f'{current_time}_NR_min_MSE.bmp', abs(cad[inde_]), cmap='gray')
    plt.imsave(f'{current_time}_CGH_min_MSE.bmp', abs(cghs[inde_]), cmap='gray')
    """ -------------------------------------------------------- """


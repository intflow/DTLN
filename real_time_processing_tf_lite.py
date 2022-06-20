"""
This is an example how to implement real time processing of the DTLN tf light
model in python.

Please change the name of the .wav file at line 43 before running the sript.
For .whl files of the tf light runtime go to: 
    https://www.tensorflow.org/lite/guide/python
    
Author: Nils L. Westhausen (nils.westhausen@uol.de)
Version: 30.06.2020

This code is licensed under the terms of the MIT-license.
"""

import soundfile as sf
import numpy as np
import tflite_runtime.interpreter as tflite
import time



##########################
# the values are fixed, if you need other values, you have to retrain.
# The sampling rate of 16k is also fix.
block_len = 1536
block_shift = 384
# load models
interpreter_1 = tflite.Interpreter(model_path='./pretrained_model/DTLN_Drone_48k_intflow_4_1.tflite')
interpreter_1.allocate_tensors()
interpreter_2 = tflite.Interpreter(model_path='./pretrained_model/DTLN_Drone_48k_intflow_4_2.tflite')
interpreter_2.allocate_tensors()

# Get input and output tensors.
input_details_1 = interpreter_1.get_input_details()
output_details_1 = interpreter_1.get_output_details()

input_details_2 = interpreter_2.get_input_details()
output_details_2 = interpreter_2.get_output_details()
# create states for the lstms
states_1 = np.zeros(input_details_1[0]['shape']).astype('float32')
states_2 = np.zeros(input_details_2[1]['shape']).astype('float32')
# load audio file at 16k fs (please change)
audio,fs = sf.read('/data/Drone_Audio_dataset_intflow/noisy_real/noisy/mix1.wav')

# Set channel number
if len(audio.shape) == 2:
    ch_num = audio.shape[1]
    print("Multichannel file inputted!!")
else:
    ch_num = 1
    audio = audio.reshape(-1,1)
    print("Mono file inputted!!")

# check for sampling rate
if fs != 48000:
    raise ValueError('This model only supports 48k sampling rate.')
# preallocate output audio
out_file = np.zeros((len(audio), ch_num))
# create buffer
in_buffer = np.zeros((block_len, ch_num)).astype('float32')
out_buffer = np.zeros((block_len, ch_num)).astype('float32')
# calculate number of blocks
num_blocks = (audio.shape[0] - (block_len-block_shift)) // block_shift
time_array = []      
# iterate over the number of blcoks  
for idx in range(num_blocks):
    start_time = time.time()

    for ch in range(0,ch_num):
        # shift values and write to buffer
        in_buffer[:-block_shift,ch] = in_buffer[block_shift:,ch]
        in_buffer[-block_shift:,ch] = audio[idx*block_shift:(idx*block_shift)+block_shift,ch]
        # calculate fft of input block
        in_block_fft = np.fft.rfft(in_buffer[:,ch])
        in_mag = np.abs(in_block_fft)
        in_phase = np.angle(in_block_fft)
        # reshape magnitude to input dimensions
        in_mag = np.reshape(in_mag, (1,1,-1)).astype('float32')
        # set tensors to the first model
        interpreter_1.set_tensor(input_details_1[1]['index'], in_mag)
        interpreter_1.set_tensor(input_details_1[0]['index'], states_1)
        # run calculation 
        interpreter_1.invoke()
        # get the output of the first block
        out_mask = interpreter_1.get_tensor(output_details_1[0]['index']) 
        states_1 = interpreter_1.get_tensor(output_details_1[1]['index'])   
        # calculate the ifft
        estimated_complex = in_mag * out_mask * np.exp(1j * in_phase)
        estimated_block = np.fft.irfft(estimated_complex)
        # reshape the time domain block
        estimated_block = np.reshape(estimated_block, (1,1,-1)).astype('float32')
        # set tensors to the second block
        interpreter_2.set_tensor(input_details_2[1]['index'], states_2)
        interpreter_2.set_tensor(input_details_2[0]['index'], estimated_block)
        # run calculation
        interpreter_2.invoke()
        # get output tensors
        out_block = interpreter_2.get_tensor(output_details_2[1]['index']) 
        states_2 = interpreter_2.get_tensor(output_details_2[0]['index']) 
        
        # shift values and write to buffer
        out_buffer[:-block_shift,ch] = out_buffer[block_shift:,ch]
        out_buffer[-block_shift:,ch] = np.zeros((block_shift))
        out_buffer[:,ch] += np.squeeze(out_block)
        # write block to output file
        out_file[idx*block_shift:(idx*block_shift)+block_shift,ch] = out_buffer[:block_shift,ch]
    time_array.append(time.time()-start_time)
    
# write to .wav file 
sf.write('out.wav', out_file, fs) 
print('Processing Time [ms]:')
print(np.mean(np.stack(time_array))*1000)
print('Processing finished.')

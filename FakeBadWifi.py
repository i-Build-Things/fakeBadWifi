import cv2 #To capture the video from your webcam
import pyaudio # To record and play audio from your mic
import wave #To save the audio as a wave file
import pyvirtualcam #To send image data to a virtual camera
import random #To generate random data
import time #To pause the program

audio = pyaudio.PyAudio() #Creating the PortAudio instance
info = audio.get_host_api_info_by_index(0) #Getting a dictionary with information about audio devices
numDevices = info.get('deviceCount') #NUmber of audio devices

print ('----------Input Devices----------')

#Looping through all the available devices and printing the index of those that can be used as input devices
for i in range (0,numDevices):
    if (audio.get_device_info_by_host_api_device_index(0,i)).get('maxInputChannels') > 0:
        print(f"Input Device Index: {i} - {audio.get_device_info_by_host_api_device_index(0,i).get('name')}")
#Asking the user to choose an input device
inputIndex = int(input('Please choose a device: '))
print ('---------------------------------\n\n')

print ('----------Output Devices----------')
#Looping through all the available devices and printing the index of those that can be used as output devices
for i in range (0,numDevices):
    if (audio.get_device_info_by_host_api_device_index(0,i)).get('maxOutputChannels') > 0:
        print(f"Output Device Index: {i} - {audio.get_device_info_by_host_api_device_index(0,i).get('name')}")
#Asking the user to choose an output device
outputIndex = int(input('Please choose a device: '))
print ('---------------------------------')


def recordAndSaveAudio():
    """
    This function will allow us to record incoming data and save it as a wave file. 
    """
    #Declaring the recording time in seconds
    recordingTime = 0.5
    #Creating the input stream
    stream = audio.open(format = pyaudio.paInt16, channels = 1, rate = 44100, input = True, 
                       input_device_index = inputIndex, frames_per_buffer = 512)
    #Creating an empty list to store the data before conversion
    recordedFrames = []
    #Continuously recording and saving data until the recordingTime's worth of data has been recorded
    for i in range (0, int(44100/512 * recordingTime)):
        data = stream.read(512)
        recordedFrames.append(data)
    #Converting the data to a .wav file and saving it
    waveFile = wave.open('recordedFile.wav', 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(44100)
    waveFile.writeframes(b''.join(recordedFrames))
    waveFile.close()
    
def corruptAndPlayAudio():
    """
    This function randomly decides whether or not to play the audio
    """
    #If the random number generated is 1, no audio is played
    if random.randint(0,1):
        return None
    #Opening the wave file
    waveFile = wave.open('recordedFile.wav', 'rb')
    #Creating the output stream
    stream = audio.open(format = pyaudio.paInt16, channels = 1, rate = 44100, output = True, 
                       output_device_index = outputIndex)
    #Reading the first 512 frames of data
    data = waveFile.readframes(512)
    #If there is no data left to read, an empty bytes string will be returned. As long as we are not getting
    #an empty bytes string, we keep playing the audio and reading the next chunk of data
    while data != b'':
        stream.write(data)
        data = waveFile.readframes(512)

#Creating the video capture device. The integer represents which camera you would like to use. 
cap = cv2.VideoCapture(0)

#Creating the virtual camera instance
with pyvirtualcam.Camera (width = 1280, height = 720, fps = 20) as cam:
    #As long as the webcam is recieving video data, the below code will be executed
    while cap.isOpened():
        #Read the incoming image data
        ret,frame = cap.read()
        #Re-colour the image as openCV saves images in the BGR format while zoom requires it in the RGB format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #Record the incoming audio and corrupt it
        recordAndSaveAudio()
        
        corruptAndPlayAudio()
        #Send the re-coloured image to the virtual camera
        cam.send(image)
        #Pausing the program for a randomly generated time between 0 and 2 seconds. 
        time.sleep(random.random()*2)        
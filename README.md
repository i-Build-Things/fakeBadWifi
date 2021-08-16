# fakeBadWifi
This repository contains the code for the video entitled How to fake bad wifi on Zoom calls with Python!

To run the program you will need to install all the modules. openCV, pyvirtualcam, and wave can be installed using pip. Time and random come pre-installed with Python3+. The pyaudio module requires the portaudio dependencies to be installed. portaudio is a c library and it can be installed directly from their website for windows devices, or using homebrew on OSX. 

Once all the modules are installed, you will also require a virtual camera and virtual microphone. The code has been tested with the OBS virtual camera and the VB virtual audio cable virtual microphone. 

Running the above code during a videocall requires the following steps: 
1. When running the code, select your default input device as the input device and the VB-Cable as the output device. 
2. In zoom, select the VB-Cable as the input device and your regular output device.
3. Select the OBS virtual camera for the camera feed. 

You can vary the recordingTime or the break post each cycle to make this look as laggy or fake as you would like to. 

You can find additional explaantions and help in the tutorial video: https://youtu.be/Y04X2Uwbgj8

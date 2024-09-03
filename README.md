
# Image_Categorizer 
[![GPL License](https://img.shields.io/badge/license-GPL-violet.svg)](http://www.gnu.org/licenses/gpl-3.0) [![Image_Categorizer](https://img.shields.io/badge/source-GitHub-303030.svg?style=flat-square)](https://github.com/agnivadas/Image_Categorizer) ![Maintenance](https://img.shields.io/maintenance/yes/2024) ![Static Badge](https://img.shields.io/badge/contributions-welcome-blue)

Designed to categorize images to memes&docs/people/others from mixture of images using Opencv haarcascades.

It is a lightweight program to support the boring task of sorting memes and people or pets pics from the mixture of images(like Whatsapp images collection)  




## Requirements

- Python(Latest version preferable)

Paste the following in command terminal to install the required libraries:
```bash
pip install opencv-python pytesseract numpy
```
Installation of Tesseract is needed .The latest installers can be downloaded here:

- [tesseract-ocr-w64-setup-5.4.0.20240606.exe (64 bit)](https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe)
or download from their official page [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)


    
## How to use:

After downloading run the script , a GUI windows will be opened and click on select directory to choose the directory which contain the mixture of images .

Click Start categorizing to start the program .The respective input images will be copied to specific folder according to their category.

Status of images processed will be shown in the window.

<img src="/assets/ss1.jpg" width="400px">



## Optimizations

This is a lightweiht program which uses OpenCV Haarcascades for facial recognition and tesserect to rcognize text blocks in images .

As Haarcascades gives false positive reults it is still used as the code is just to support the categorization.

Other more accurate program like Mediapipe, MTCNN could be used for facial recognition but it would make the code more heavy weight and slow for this process.

## Contributing

Contributions and any tips to improve the code are always welcome!



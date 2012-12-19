OCRprep
=======

ocrprep prepares photos taken in less than optimal conditions for optical character recognition.

ocrprep is licensed under the LGPL http://www.gnu.org/licenses/lgpl-3.0.txt
      
We use OpenCV for almost everything

1. adaptive thresholding fixes lighting issue that can occur when using camera phones
2. clean up noisy images using edge preserving median blur, dilation and erosion
2. The hough transform finds lines formed by rows of text
3. Once we know what the lines look like, we can calculate the degree of rotation
4. OpenCV will build a rotation matrix for us given a point around which to rotate, and the angle 



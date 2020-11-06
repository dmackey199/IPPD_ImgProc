Tutorial Code followed by using https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/
Code has been slightly modified from tutorial to measure in mm

To run code use the following command:
	python object_size.py --image [location of image] -- width [size of known object]
For example: 
	python object_size.py -- image images/example_01.png -- width 25.273

Once run, each object will be produced as it's own image with a diagonal of the size. The next image will not populate until the first image is exited. The program will not finish untill all images have been exited.
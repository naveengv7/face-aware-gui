## install dependency

sudo apt-get install python3-tk
sudo apt-get install python3-pil
sudo apt-get install python3-pil.imagetk
pip3 install dlib
pip3 install imutils
pip3 install shapely
python3 -m  pip install cryptography

# for jetson nano, python 3.6 
#if dlib does not install then use this
wget http://dlib.net/files/dlib-19.21.tar.bz2
tar jxvf dlib-19.17.tar.bz2
cd dlib-19.21/
mkdir build
cd build/
#cmake ..
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
cmake --build .
cd ../
$ sudo python3 setup.py install
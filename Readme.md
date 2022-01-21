## install dependency

sudo apt-get install python3-tk
sudo apt-get install python3-pil
sudo apt-get install python3-pil.imagetk
pip3 install dlib

# for jetson nano, python 3.6 
#if dlib does not install then use this
wget http://dlib.net/files/dlib-19.21.tar.bz2
tar jxvf dlib-19.17.tar.bz2
cd dlib-19.17/
mkdir build
cd build/
cmake ..
cmake --build .
cd ../
$ sudo python3 setup.py install
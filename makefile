# This is needed only for *compiling* the yuv2rgb.so file (Python module).
# Not needed for just running the Python code with precompiled .so file.

all: yuv2rgb.so

yuv2rgb.so: yuv2rgb.o
	gcc -s -shared -Wl,-soname,libyuv2rgb.so $(shell pkg-config --libs python3) -o yuv2rgb.so yuv2rgb.o

yuv2rgb.o: yuv2rgb.c
	gcc -fPIC -O3 -fomit-frame-pointer -funroll-loops $(shell pkg-config --cflags python3) -c yuv2rgb.c

clean:
	rm -f yuv2rgb.o yuv2rgb.so

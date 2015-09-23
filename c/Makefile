CXX= g++
CFLAGS=-Wall -O3 -g
CXXFLAGS=-Wall -O3 -g
OBJECTS= main.o gpio.o led-matrix.o thread.o 
BINARIES=led-matrix.run test-clear.run no-scroll.run
LDFLAGS=-lrt -lm -lpthread

all: led-matrix

test-clear: CXXFLAGS += -DCLEARONLY
no-scroll: CXXFLAGS += -DNOSCROLL

led-matrix.o: led-matrix.cc led-matrix.h
main.o: led-matrix.h
main2.o: led-matrix.h

led-matrix : $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@.run $(LDFLAGS)
	
test-clear : $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@.run $(LDFLAGS)

no-scroll : $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@.run $(LDFLAGS)
clean:
	rm -f $(OBJECTS)

clean-binaries:
	rm -f $(BINARIES) $(OBJECTS)

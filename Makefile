CC = g++
CXXFLAGS = -Wall -g -O0 -std=c++20

bin/clean-dump:src/clean-dump.cpp
	    $(CC) $(CXXFLAGS) -o $@ $^

clean:
	    $(RM) bin/clean-dump .*.sw?

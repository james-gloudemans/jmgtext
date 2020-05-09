all: test list

remake: clean all

librope.so: rope.o util.o
	gcc -shared $^ -o $@

%.o: %.c
	gcc -c -Wall -Werror -fpic -I . $^

test: test.o util.o list.o
	gcc -o test test.o util.o list.o

rope: librope.so
	./build_rope.py

clean:
	rm -f test *.o *.so _cffi_rope.c
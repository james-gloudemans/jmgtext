all: test rope

remake: clean all

librope.so: rope.o util.o
	gcc -shared $^ -o $@

%.o: %.c
	gcc -c -Wall -Werror -fpic -I . $^

test: test.o util.o rope.o
	gcc -o test test.o util.o rope.o

rope: librope.so
	./build_rope.py

clean:
	rm -f test *.o *.so _cffi_rope.c
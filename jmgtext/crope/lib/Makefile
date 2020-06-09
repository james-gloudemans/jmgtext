all: test rope pystr

remake: clean all

librope.so: rope.o util.o
	gcc -shared $^ -o $@

libpystr.so: pystr.o util.o
	gcc -shared $^ -o $@ -lbsd

%.o: %.c
	gcc -c -Wall -Werror -fpic -I . $^

test: test.o util.o rope.o pystr.o
	gcc -o rope_test test.o util.o rope.o pystr.o -lm -lbsd

rope: librope.so
	./build_rope.py

pystr: libpystr.so
	./build_pystr.py

clean:
	rm -f rope_test *.o *.so _cffi_rope.c
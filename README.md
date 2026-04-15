# CSE 141 Compiler

Compiler for UC Merced CSE 141 class

## Lab 01

To run the scanner and test on a file, compile the Java classes:

```sh
cd java
javac *.java
```

Then run the scanner on the file:

```sh
java Scanner <path/to/your/file>.c
```

The current working directory must be the directory that contains the `*.class` files.

The scanner will output the processed file as `<file_name>_gen.c` in the same directory as the original file.

## Lab 02

Recursive descent LL(1) parser implemented in C++11.

### Build

Using Make:

```sh
cd cpp
make
```

Using [just](https://github.com/casey/just):

```sh
cd cpp
just build
```

### Test

Using Make:

```sh
make test        # build (incremental) and run all tests
make test-clean  # clean build then run all tests
```

Using just:

```sh
just test        # build (incremental) and run all tests
just test-clean  # clean build then run all tests
```

### Run on a single file

```sh
./bin/parser <path/to/file>.c
```

Or with just:

```sh
just run <path/to/file>.c
```

### Other commands

| Task | Make | Just |
|------|------|------|
| Debug build | `make DEBUG=1` | `just build-debug` |
| Clean artifacts | `make clean` | `just clean` |
| Clean + build | `make rebuild` | `just rebuild` |
| List recipes | — | `just` |

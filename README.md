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

# Simulator of transfer between assembly language and machine language


In this project, you will write a Python program simulator_xxxxxxx.py, where xxxxxxx is your
CSU ID, to implement the language transfer between the assembly code and the machine code in
hexadecimal format (8 hex characters). You use the command line argument “-a” to specify that
the input is an assembly code and “-m” to specify that the input is a machine code. Following the
methodology mentioned in the class, your simulator should be able to finish the following TWO
TASKS: 1) transferring one assembly code to its corresponding machine code, 2) transferring one
machine code to its corresponding assembly code. You can do the self-check by swapping the
input and output.
The following contents in parentheses illustrate the commands to run your program and their
corresponding outputs:
Input1: MIPS assembly code (python3 simulator.py -a 'add $s0, $a1, $t7')
Output1: corresponding machine code in 8 hex characters (00af8020)
Input2: machine code in 8 hex characters (python3 simulator.py -m '00af8020')
Output2: corresponding MIPS assembly code (add $s0, $a1, $t7)


## Converts between machine code and assmebly (MIPS)

## Usage

### Convert assembly instruction to machine code instruction

```shell
./simulator.py -a 'add $s0, $s1, $s2'
```

### Convert machine code instruction to assembly instruction

```shell
./simulator.py -m 02328020

```

### Output Screenshot

![2023-02-28_20-27-29](https://user-images.githubusercontent.com/35831574/222021559-ee3f435c-2cb2-4fea-858e-4d00aef3c66b.png)

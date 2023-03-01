#! /usr/bin/python3

from simulator import AssemblerDisassembler

print("[*] Testing assembly....")
ass = AssemblerDisassembler()
assert ass.assemble('add $s0, $s1, $s2') == '02328020'
assert ass.assemble('addi $t0, $t1, 0x5') == '21280005'
assert ass.assemble('sub $s0, $s1, $s2') == '02328022'
assert ass.assemble('sll $t0, $t1, 0x2') == '00094080'
assert ass.assemble('srl $t0, $t1, 0x3') == '000940c2'
assert ass.assemble('lw $t0, 0x8($s1)') == '8e280008'
assert ass.assemble('sw $t0, 0x12($s1)') == 'ae280012'

print("[*] Testing disassembly....")
disass = AssemblerDisassembler()
assert disass.disassemble('02328020') == 'add $s0, $s1, $s2'
assert disass.disassemble('21280005') == 'addi $t0, $t1, 0x5'
assert disass.disassemble('02328022') == 'sub $s0, $s1, $s2'
assert disass.disassemble('00094080') == 'sll $t0, $t1, 0x2'
assert disass.disassemble('000940c2') == 'srl $t0, $t1, 0x3'
assert disass.disassemble('8e280008') == 'lw $t0, 0x8($s1)'
assert disass.disassemble('ae280012') == 'sw $t0, 0x12($s1)'

print("[\u2713] All test passed")
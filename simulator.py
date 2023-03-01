#! /usr/bin/python3

class MIPS:
    """
    Contains some look up tables and helper routines for MIPS.
    The opcodes and registers are returned binary encoded.
    """

    instructions = {'add': '000000', 'addu': '000000', 'and': '000000', 'nor': '000000',
                    'or': '000000', 'slt': '000000', 'sltu': '000000', 'sll': '000000',
                    'srl': '000000', 'sub': '000000', 'subu': '000000', 'jr': '000000',
                    'mult': '000000', 'mfhi': '000000', 'mflo': '000000', 'addi': '001000',
                    'addiu': '001001', 'andi': '001100', 'beq': '000100', 'bne': '000101',
                    'lw': '100011', 'sw': '101011', 'j': '000010', 'jal': '000011'}

    rtype_functs = {'add': '100000', 'addu': '100001', 'and': '100100', 'nor': '100111',
                    'or': '100101', 'slt': '101010', 'sltu': '101011', 'sll': '000000',
                    'srl': '000010', 'sub': '100010', 'subu': '100011', 'jr': '001000',
                    'mult': '011000', 'mfhi': '010000', 'mflo': '010010'}

    registers = {'$zero': '00000', '$at': '00001', '$v0': '00010', '$v1': '00011',
                 '$a0': '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111',
                 '$t0': '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011',
                 '$t4': '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111',
                 '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011',
                 '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111',
                 '$t8': '11000', '$t9': '11001', '$k0': '11010', '$k1': '11011',
                 '$gp': '11100', '$sp': '11101', '$fp': '11110', '$ra': '11111'}

    def get_opcode(self, instruction):
        """ 
        Get the binary opcode for the given assembly instruction.
        """
        opcode = MIPS.instructions.get(instruction)
        if not opcode:
            raise ValueError(f'Invalid assembly instruction: {instruction}')
        return opcode

    def get_instruction(self, machine_code):
        """ 
        Get the assembly opcode from the given binary machine code instruction.
        We pass entire code because funct is important for identifying R-type instructions.
        """
        if len(machine_code) != 32:
            raise ValueError(f'Invalid instruction format: {machine_code}')
        opcode = machine_code[:6]
        if opcode == '000000':# Is an R-type instruction
            funct = machine_code[-6:]
            for key, value in MIPS.rtype_functs.items():
                if value == funct:
                    return key
        else:  
            for key, value in MIPS.instructions.items():
                if value == opcode:
                    return key
        raise ValueError(f'Invalid opcode instruction: {opcode}')

    def get_funct(self, instruction):
        """
        Get the funct for the given R-type assembly instruction.
        """
        value = MIPS.rtype_functs.get(instruction)
        if value is None:
            raise ValueError(f'Invalid assembly instruction: {instruction}')
        return value

    def get_register_value(self, register):
        """
        Get the binary value for the register with the given symbol.
        """
        value = MIPS.registers.get(register)
        if value is None:
            raise ValueError(f'Invalid register: {register}')
        return value

    def get_register(self, reg_value):
        """
        Get the register with the given binary value.
        """
        for key, value in MIPS.registers.items():
            if value == reg_value:
                return key
        raise ValueError(f'Invalid register: {reg_value}')


class AssemblerDisassembler(MIPS):

    def __init__(self):
        pass

    def assemble(self, asm):
        """
        Given an assembly instruction, return its corresponding machine code in hexadecimal format.
        """
        # Convert input into parts: opcode, operands
        asm = asm.replace(',', '')
        parts = list(filter(lambda x: x, asm.split(' ')))
        opcode = self.get_opcode(parts[0])

        # R-type instructions
        if opcode == '000000':
            if len(parts) != 4:
                raise ValueError(f'Bad instruction format: {asm}')
            funct = self.get_funct(parts[0])
            # Non-shift instructions
            if parts[0] not in ['sll', 'srl', 'sra', 'sllv', 'srlv', 'srav']:
                rd, rs, rt = map(self.get_register_value, parts[1:])
                machine_code = f'{opcode}{rs}{rt}{rd}00000{funct}'
            # Shift instructions
            else:
                rd, rt = map(self.get_register_value, [parts[1], parts[2]])
                shamt = int(parts[3], 16)
                machine_code = f'{opcode}00000{rt}{rd}{shamt:05b}{funct}'

        # J-type instructions
        elif opcode[0] == '000010' or opcode[0] == '000011':
            if len(parts) != 2:
                raise ValueError(f'Bad instruction format: {asm}')
            address = int(parts[1])
            machine_code = f'{opcode}{address:026b}'

        # I-type instructions
        else:
            if opcode == '100011' or  opcode == '101011': # sw, lw
                if len(parts) == 3: # convert e.g sw $t0 0x12($s1) to sw $t0 0x12 $s1
                    rs, rt_offset = self.get_register_value(parts[1]), parts[2]
                    rt, offset = rt_offset.split('(')[::-1]
                    rt, offset = self.get_register_value(rt.strip(')')), int(offset, 16)
                else:
                    rs, rt = self.get_register_value(parts[1]), self.get_register_value(parts[3])
                    offset = int(parts[2], 16)
                machine_code = f'{opcode}{rt}{rs}{offset:016b}'
            else:
                rt, rs = map(self.get_register_value, [parts[1], parts[2]])
                immediate = int(parts[3], 16)
                machine_code = f'{opcode}{rs}{rt}{immediate:016b}'
        
        return f'{int(machine_code, 2):08x}'

    def disassemble(self, hex_code):
        """
        Given machine code in hexadecimal, return the equivalent assembly instruction.
        """
        if len(hex_code) != 8:
            raise ValueError(f'Bad instruction format: {hex_code}')

        # Convert the hex code into binary machine code
        machine_code = f'{int(hex_code, 16):032b}'

        # Get the opcode: binary code and then assembly instruction.
        opcode = machine_code[:6]
        instruction = self.get_instruction(machine_code)

        # R-type instructions
        if opcode == '000000':
            # Non-shift instructions
            if instruction not in ['sll', 'srl', 'sra', 'sllv', 'srlv', 'srav']:
                rs, rt, rd = map(self.get_register, [machine_code[6:11],
                                                     machine_code[11:16],
                                                     machine_code[16:21]])
                asm = f'{instruction} {rd}, {rs}, {rt}'
            # Shift instructions
            else:
                rs, rt = map(self.get_register, [machine_code[11:16],
                                                 machine_code[16:21]])
                shamt = int(machine_code[21:26], 2)
                asm = f'{instruction} {rt}, {rs}, 0x{shamt:x}'
        
        # J-type instructions
        elif opcode == '000010' or opcode == '000011':
            address = int(machine_code[6:], 2)
            asm = f'{instruction} {address}'
        
        # I-type instructions
        else:
            rs, rt = map(self.get_register, [machine_code[6:11],
                                            machine_code[11:16]])
            immediate = int(machine_code[16:], 2)
            if opcode == '100011' or  opcode == '101011': #sw, lw
                asm = f'{instruction} {rt}, 0x{immediate:x}({rs})'
            else:
                asm = f'{instruction} {rt}, {rs}, 0x{immediate:x}'
        
        return asm


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Convert MIPS assembly instruction into machine code or vice versa.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', action='store_true', help='Convert machine code to assembly.')
    group.add_argument('-a', action='store_true', help='Convert assembly to machine code.')
    parser.add_argument('instruction', type=str, help='The MIPS instruction.')

    # Parse the command-line arguments
    args = parser.parse_args()
    if args.a:
        ass = AssemblerDisassembler()
        print(ass.assemble(args.instruction))
    else:
        disass = AssemblerDisassembler()
        print(disass.disassemble(args.instruction))


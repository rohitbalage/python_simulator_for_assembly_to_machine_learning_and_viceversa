INSTRUCTION_SET = {
    'ADD': 0b0000,
    'SUB': 0b0001,
    'AND': 0b0010,
    'OR': 0b0011,
    'MOV': 0b0100,
    'LDR': 0b0101,
    'STR': 0b0110,
    'JMP': 0b0111,
    'HLT': 0b1000
}

def assemble(instruction):
    # Split the instruction into its components
    parts = instruction.split()

    # Get the opcode and the operands
    opcode = INSTRUCTION_SET[parts[0]]
    operands = parts[1:]

    # Assemble the instruction
    if opcode == INSTRUCTION_SET['HLT']:
        # HLT instruction has no operands
        instruction_bits = (opcode << 8)
    elif opcode == INSTRUCTION_SET['JMP']:
        # JMP instruction has one operand (a label)
        label = int(operands[0])
        instruction_bits = (opcode << 8) | label
    else:
        # Other instructions have two operands (registers or immediate values)
        source = operands[0]
        destination = operands[1]

        if source.startswith('R') and destination.startswith('R'):
            # Register-register instruction
            source_register = int(source[1:])
            destination_register = int(destination[1:])
            instruction_bits = (opcode << 8) | (source_register << 5) | destination_register
        elif source.startswith('#') and destination.startswith('R'):
            # Immediate-register instruction
            immediate_value = int(source[1:])
            destination_register = int(destination[1:])
            instruction_bits = (opcode << 8) | (immediate_value << 3) | destination_register
        elif source.startswith('[') and source.endswith(']') and destination.startswith('R'):
            # Load-store instruction
            address_register = int(source[2:-1])
            destination_register = int(destination[1:])
            instruction_bits = (opcode << 8) | (address_register << 5) | destination_register
        else:
            raise ValueError('Invalid instruction: {}'.format(instruction))

    # Return the machine language instruction as an 8-character hexadecimal string
    return '{:08X}'.format(instruction_bits)

def disassemble(instruction_hex):
    # Convert the hexadecimal string to an integer
    instruction = int(instruction_hex, 16)

    # Get the opcode and the operands
    opcode = (instruction >> 8) & 0b1111
    operand_bits = instruction & 0b11111111

    if opcode == INSTRUCTION_SET['HLT']:
        # HLT instruction has no operands
        operands = []
    elif opcode == INSTRUCTION_SET['JMP']:
        # JMP instruction has one operand (a label)
        operands = [str(operand_bits)]
    else:
        # Other instructions have two operands (registers or immediate values)
        source_register = (operand_bits >> 5) & 0b111
        destination_register = operand_bits & 0b111
        if opcode == INSTRUCTION_SET['LDR'] or opcode == INSTRUCTION_SET['STR']:
            # Load-store instruction has an address register instead of a source register
            source = '[R{}]'.format(source_register)
            destination = 'R{}'.format(destination_register)
        elif (opcode == INSTRUCTION_SET['MOV'] and destination_register == 0) or opcode == INSTRUCTION_SET['HLT']:
            # Move-immediate instruction or HLT instruction has an immediate value instead of a
            # source register
            source = '#{}'

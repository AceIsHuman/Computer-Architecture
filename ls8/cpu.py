"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [None] * 8
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.reg[7] = 0xF4
        self.pc = 0
        self.running = False

    def load(self, path):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        try:
            with open(path) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_num = comment_split[0]

                    if possible_num == '':
                        continue

                    if possible_num[0] == '1' or possible_num[0] == '0':
                        num = possible_num[:8]
                        self.ram_write(int(num, 2), address)
                        address += 1
            file.close()
        except FileNotFoundError:
            print(f'{path} not found.')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT  = 0b00000001
        LDI  = 0b10000010
        PRN  = 0b01000111
        ADD  = 0b10100000
        MUL  = 0b10100010
        PUSH = 0b01000101
        POP  = 0b01000110
        CALL = 0b01010000
        RET  = 0b00010001

        def hlt():
            print('Shutting Down... Goodbye')
            self.running = False
            sys.exit(0)

        def ldi():
            reg = self.ram_read(self.pc + 1)
            val = self.ram_read(self.pc + 2)
            self.reg[reg] = val

        def prn():
            reg = self.ram_read(self.pc + 1)
            print(self.reg[reg])

        def add():
            operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
            self.alu("ADD", operand_a, operand_b)

        def mul():
            operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
            self.alu("MUL", operand_a, operand_b)

        def call():
            # get address for instruction
            instruction_address = self.ram_read(self.pc + 1)
            # get the next instruction address
            next_address = self.pc + 2
            ## store in stack
            self.reg[7] -= 1
            self.ram_write(next_address, self.reg[7])
            self.pc = self.reg[instruction_address]

        def ret():
            ret_address = self.ram_read(self.reg[7])
            self.pc = ret_address
            self.reg[7] += 1

        def push():
            # decrement stack pointer
            self.reg[7] -= 1
            # read register value
            reg = self.ram_read(self.pc + 1)
            val = self.reg[reg]
            # write to ram at stack pointer
            self.ram_write(val, self.reg[7])        

        def pop():
            # get value at current stack pointer address
            val = self.ram_read(self.reg[7])
            # store value at given register
            reg = self.ram_read(self.pc + 1)
            self.reg[reg] = val
            # increment stack pointer
            self.reg[7] += 1
  
        instructions = {}
        instructions[HLT] = hlt
        instructions[LDI] = ldi
        instructions[PRN] = prn
        instructions[ADD] = add
        instructions[MUL] = mul
        instructions[PUSH] = push
        instructions[POP] = pop
        instructions[CALL] = call
        instructions[RET] = ret

        self.running = True
        # read memory address stored in PC
        # store in IR

        while self.running:
            ir = self.ram_read(self.pc)
            num_operands = ir >> 6
            instructions[ir]()
            prevent_pc_update = (ir >> 4) & 1
            if prevent_pc_update:
                continue
            self.pc += num_operands + 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

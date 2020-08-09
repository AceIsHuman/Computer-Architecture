"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [None] * 8
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
                        self.ram[address] = int(num)
                        address += 1
            file.close()
        except FileNotFoundError:
            print(f'{path} not found.')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        self.running = True
        # read memory address stored in PC
        # store in IR
        ir = self.ram[self.pc]
        operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)

        while self.running:
            if ir == HLT:
                print('Shutting Down... Goodbye')
                self.running = False
                sys.exit(1)
            elif ir == LDI:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.pc + 2]
                self.reg[reg] = val

                self.pc += 3
            elif ir == PRN:
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])

                self.pc += 2


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

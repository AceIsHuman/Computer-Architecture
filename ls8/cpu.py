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
        ADD = 0b10100000

        self.running = True
        # read memory address stored in PC
        # store in IR

        while self.running:
            ir = self.ram_read(self.pc)
            num_operands = ir >> 6

            if ir == HLT:
                print('Shutting Down... Goodbye')
                self.running = False
                sys.exit(0)

            elif ir == LDI:
                reg = self.ram_read(self.pc + 1)
                val = self.ram_read(self.pc + 2)
                self.reg[reg] = val

            elif ir == PRN:
                reg = self.ram_read(self.pc + 1)
                print(self.reg[reg])

            elif ir == ADD:
                operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
                self.alu("ADD", operand_a, operand_b)
            
            self.pc += num_operands + 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

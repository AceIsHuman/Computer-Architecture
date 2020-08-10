PRINT_ACE       = 0b00000001
HALT            = 0b00000010
PRINT_NUM       = 0b01000011
SAVE            = 0b10000100
PRINT_REGISTER  = 0b01000101
ADD             = 0b10000110

memory = [
  PRINT_ACE,
  PRINT_NUM,
  526,
  SAVE,
  42,
  2,
  SAVE,
  42,
  3,
  ADD,
  2,
  3,
  PRINT_REGISTER,
  2,
  HALT,
]

running = True
pc = 0
​
# Memory bus
## a bunch of wires that the CPU uses to send an address to RAM
## also a data bus: CPU sends data to RAM, RAM sends data to CPU
##     CPU
##  ||||||||
##  ||||||||
##  ||||||||
##     RAM
​
# 0b00000001
# 0b00000010
# 0b11111111

# registers (use as variables)
# R0 - R7
registers = [None] * 8

while running:
  command = memory[pc]
  num_operands = command >> 6

  if command == PRINT_ACE:
    print('Ace!')

  if command == PRINT_NUM:
    num = memory[pc + 1]
    print(num)

  if command == SAVE:
    num = memory[pc + 1]
    index = memory[pc + 2]
    registers[index] = num

  if command == PRINT_REGISTER:
    reg = memory[pc + 1]
    print(registers[reg])

  if command == ADD:
    reg_a = memory[pc + 1]
    reg_b = memory[pc + 2]
    registers[reg_a] += registers[reg_b]

  if command == HALT:
    print('Goodbye')
    running = False
  
  pc += num_operands + 1
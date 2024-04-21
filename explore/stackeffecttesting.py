import dis
import opcode as op

ret = dis.stack_effect(106, 1, jump=False)
print(ret)

data = []

data.pop()
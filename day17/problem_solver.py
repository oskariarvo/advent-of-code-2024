class ProblemSolver:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def combo_operand(self, operand: int):
        if 3 >= operand >= 0:
            value = operand
        elif operand == 4:
            value = self.A
        elif operand == 5:
            value = self.B
        elif operand == 6:
            value = self.C
        elif operand == 7:
            value = "RESERVED"
        return value
    def adv(self, opcode: int, operand: int):
        numerator = self.A
        combo_value = self.combo_operand(operand)
        if combo_value == "RESERVED":
            return 2
        denominator = 2**combo_value
        result = numerator // denominator
        self.A = result
        return 2
    def bxl(self, opcode: int, operand: int):
        self.B = self.B ^ operand
        return 2
    def bsl(self, opcode: int, operand: int):
        combo_value = self.combo_operand(operand)
        if combo_value == "RESERVED":
            return 2
        self.B = combo_value % 8
        return 2
    def jnz(self, opcode: int, operand: int):
        if self.A == 0:
            return 2
        return operand
    def bxc(self, opcode: int, operand: int):
        self.B = self.B ^ self.C
        return 2
    def out(self, opcode: int, operand: int):
        combo_value = self.combo_operand(operand)
        if combo_value == "RESERVED":
            return (2, None)
        result = combo_value % 8
        return (2, result)
    def bdv(self, opcode: int, operand: int):
        numerator = self.A
        combo_value = self.combo_operand(operand)
        if combo_value == "RESERVED":
            return 2
        denominator = 2**combo_value
        result = numerator // denominator
        self.B = result
        return 2
    def cdv(self, opcode: int, operand: int):
        numerator = self.A
        combo_value = self.combo_operand(operand)
        if combo_value == "RESERVED":
            return 2
        denominator = 2**combo_value
        result = numerator // denominator
        self.C = result
        return 2
    def instruction(self, opcode: int, operand: int, pointer: int, outputs=[]):
        if opcode == 0:
            return (pointer + self.adv(0, operand), outputs)
        elif opcode == 1:
            return (pointer + self.bxl(1, operand), outputs)
        elif opcode == 2:
            return (pointer + self.bsl(2, operand), outputs)
        elif opcode == 3:
            if self.A == 0:
                return (pointer + self.jnz(3, operand), outputs)
            else:
                return (self.jnz(3, operand), outputs)
        elif opcode == 4:
            return (pointer + self.bxc(4, operand), outputs)
        elif opcode == 5:
            increase, output = self.out(5, operand)
            if output is not None:
                outputs.append(output)
            return (pointer + increase, outputs)
        elif opcode == 6:
            return (pointer + self.bdv(6, operand), outputs)
        elif opcode == 7:
            return (pointer + self.cdv(7, operand), outputs)

    def program(self, commands: list):
        pointer = 0
        outputs = []
        while len(commands) >= pointer >= 0 and len(commands) >= (pointer+1) >= 0:
            pointer, outputs = self.instruction(commands[pointer], commands[pointer+1], pointer, outputs)
        if len(outputs) != 0:
            print("Resulting program:", ",".join(map(str, outputs)))

    def single_program(self, commands: list, target: int):
        pointer = 0
        outputs = []
        while len(commands) >= pointer >= 0 and len(commands) >= (pointer+1) >= 0:
            if commands[pointer] == 3:
                break
            if commands[pointer] == 0:
                pointer += 2
                continue
            pointer, outputs = self.instruction(commands[pointer], commands[pointer+1], pointer, outputs)
        return outputs

    def find_A(self, commands: list):
        targets = commands[::-1]
        self.A = 0
        corrects = []
        target_index = 0
        while target_index < len(targets):
            #Initialize
            x = self.A + 8
            y = self.A
            while x != y:
                self.A = y
                if len(corrects) != 0 and (self.A // 8 != corrects[target_index - 1]):
                    break
                potential = self.single_program(commands, targets[target_index])
                if not potential:
                    break
                if potential[0] == targets[target_index]:
                    break
                y += 1
            if potential[0] == targets[target_index]:
                corrects.append(self.A)
                self.A = self.A * 8
                target_index += 1
            else:
                while True:
                    self.A = corrects[target_index - 1] + 1
                    corrects.pop(target_index - 1)
                    target_index -= 1
                    if self.A // 8 != corrects[target_index - 1]:
                        continue
                    break
        if corrects[0] == 0:
            print("Register A should be:", self.A)
        else:
            print("Register A should be:", corrects[len(corrects)-1])
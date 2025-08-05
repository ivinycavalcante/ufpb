import sys

# Tabela de opcodes
OPCODES = {
    "ADD":   "000001",
    "SUB":   "000010", 
    "ADDI":  "000011",
    "SUBI":  "000100",
    "MUL2":  "000101",
    "DIV2":  "000110",
    "CLR":   "000111",
    "RST":   "001000",
    "MOV":   "001001",
    "JMP":   "001010",
    "CMP":   "001011",
    "JZ":    "001100",
    "INC":   "001101",
    "DEC":   "001110",
    "LOADM": "001111",
    "STOREM":"010000",
    "RIO":   "010001",
    "WIO":   "010010"
}

def reg_to_bin(reg_str):
    if not reg_str.startswith('R'):
        return None
    reg_num = int(reg_str[1:])
    if reg_num < 0 or reg_num > 7:
        return None
    return format(reg_num, '03b')

def immediate_to_bin(imm_str):
    if imm_str.startswith('0X'):
        value = int(imm_str, 16)
    elif imm_str.startswith('0B'):
        value = int(imm_str, 2)
    else:
        value = int(imm_str)
    
    if value < 0 or value > 255:
        return None
    return format(value, '08b')

def address_to_bin(addr_str):
    if addr_str.startswith('0X'):
        addr = int(addr_str, 16)
    elif addr_str.startswith('0B'):
        addr = int(addr_str, 2)
    else:
        addr = int(addr_str)
    
    if addr < 0 or addr > 4095:
        return None
    return format(addr, '012b')

def assemble_instruction(line):
    line = ' '.join(line.strip().upper().split())
    
    if not line or line.startswith('#'):
        return None
    
    parts = line.split()
    instruction = parts[0]
    args = []
    
    if len(parts) > 1:
        arg_string = ''.join(parts[1:])
        args = [arg.strip() for arg in arg_string.split(',') if arg.strip()]
    
    opcode = OPCODES.get(instruction)
    if opcode is None:
        return f"ERRO: Instrução '{instruction}' não reconhecida"
    
    # R-Type: 2 registradores
    if instruction in ["ADD", "SUB", "MOV", "CMP"]:
        if len(args) != 2:
            return f"ERRO: {instruction} requer 2 argumentos"
        
        regA_bin = reg_to_bin(args[0])
        regB_bin = reg_to_bin(args[1])
        
        if regA_bin is None or regB_bin is None:
            return f"ERRO: Registradores inválidos"
        
        return opcode + regA_bin + regB_bin + "000000"
    
    # I-Type: 1 registrador + valor imediato
    elif instruction in ["ADDI", "SUBI", "LOADM", "STOREM"]:
        if len(args) != 2:
            return f"ERRO: {instruction} requer 2 argumentos"
        
        reg_bin = reg_to_bin(args[0])
        imm_bin = immediate_to_bin(args[1])
        
        if reg_bin is None or imm_bin is None:
            return f"ERRO: Argumentos inválidos"
        
        return opcode + reg_bin + imm_bin
    
    # J-Type: endereço
    elif instruction in ["JMP", "JZ"]:
        if len(args) != 1:
            return f"ERRO: {instruction} requer 1 argumento"
        
        addr_bin = address_to_bin(args[0])
        if addr_bin is None:
            return f"ERRO: Endereço inválido"
        
        return opcode + addr_bin
    
    # Sem operandos
    elif instruction in ["RST", "CLR"]:
        if len(args) != 0:
            return f"ERRO: {instruction} não aceita argumentos"
        return opcode + "000000000000"
    
    # 1 registrador
    elif instruction in ["INC", "DEC", "MUL2", "DIV2", "RIO", "WIO"]:
        if len(args) != 1:
            return f"ERRO: {instruction} requer 1 argumento"
        
        reg_bin = reg_to_bin(args[0])
        if reg_bin is None:
            return f"ERRO: Registrador inválido"
        
        return opcode + reg_bin + "000000000"
    
    return f"ERRO: Formato não implementado"

def main():
    if len(sys.argv) != 2:
        print("Uso: python masm.py arquivo.asm")
        return
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except:
        print(f"ERRO: Não foi possível abrir o arquivo '{filename}'")
        return
    
    pc = 0
    
    for line in lines:
        result = assemble_instruction(line)
        
        if result is None:
            continue
        elif result.startswith("ERRO"):
            print(result)
        else:
            addr_hex = format(pc, '04X')
            print(f"{addr_hex}: {result}")
            pc += 1

if __name__ == "__main__":
    main()
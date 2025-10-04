# mast8
TTA8 Macro Assembler
## Non Instructions
|Type|Prefix|Info|
|--|:--:|--|
|Comment|#|Can be on own line or post instruction with space|
|Label|:|Must be on own line|
|Equate|.|Must be on own line|
## Instructions
Space separates opcode and arguments
Commas separate arguments
|Type|Arg1|Arg2|Info|
|--|:--:|:--:|--|
|MV|dst|src|  |
|MVC|dst|src|  |
|MVZ|dst|src|  |
|MVI|nibble|imm|imm binary(0b), hex(0x) or decimal(no prefix)|

## Macros
Space separates opcode and arguments
Commas separate arguments
|Type|Arg1|Arg2|Arg3|Info|
|--|:--:|:--:|:--:|--|
|JMP|LBL/EQU/imm|  |  |imm binary(0b), hex(0x) or decimal(no prefix)|
|ADD|dst|src1|src2|  |
|AND|dst|src1|src2|  |

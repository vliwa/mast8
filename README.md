# mast8
TTA8 Macro Assembler
## Non Instructions
|Type|Prefix|Info|
|--|:--:|--|
|Comment|#|Can be on own line or post instruction with space|
|Label|:|Must be on own line
## Instructions
Space separates opcode and arguments
Commas separate arguments
|Type|Arg1|Arg2|Info|
|--|:--:|:--:|--|
|MV|dst|src|  |
|MVC|dst|src|  |
|MVZ|dst|src|  |
|MVI|nibble|immediate|  |

MVI immediate argument can be
|Type|Prefix|Info|
|--|:--:|--|
|binary|0b|  |
|hex|0x|  |
|decimal|  |no prefix|

## Macros
Space separates opcode and arguments
Commas separate arguments
|Type|Arg1|Arg2|Arg3|Info|
|--|:--:|:--:|:--:|--|
|JMP|LBL/immediate|  |  |imm 0b or 0x|
|ADD|dst|src1|src2|  |
|AND|dst|src1|src2|  |

from utils.constants import *
from utils.data_classes import Token

RESERVED_KEYWORDS = {
    PROGRAM: Token(PROGRAM, PROGRAM),
    BEGIN: Token(BEGIN, BEGIN),
    END: Token(END, END),
    COMMA: Token(COMMA, COMMA),
    COLON: Token(COLON, COLON),
    DIV: Token(INTEGER_DIV, INTEGER_DIV),
    INTEGER: Token(INTEGER, INTEGER),
    INT: Token(INTEGER, INTEGER),
    FLOAT: Token(FLOAT, FLOAT),
    REAL: Token(REAL, REAL),
    VAR: Token(VAR, VAR),
    PROCEDURE: Token(PROCEDURE, PROCEDURE),
    STRING: Token(STRING, STRING),
    STR: Token(STRING, STRING),
    FUNCTION: Token(FUNCTION, FUNCTION),
    RETURN: Token(RETURN, RETURN),
    BOOLEAN: Token(BOOLEAN, BOOLEAN),
    TRUE: Token(BOOLEAN, TRUE),
    FALSE: Token(BOOLEAN, FALSE),
    FOR: Token(FOR, FOR),
    BREAK: Token(BREAK, BREAK),
    OBJECT: Token(OBJECT, OBJECT),
}

import abc
from enum import Enum
from typing import List


class SymbolTypes(Enum):
    INTEGER = "INTEGER"
    STRING = "STRING"
    REAL = "REAL"
    BOOLEAN = "BOOLEAN"


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'


class NodeVisitor(object):
    def visit(self, node):
        class_name = type(node).__name__
        method_name = 'visit_' + class_name
        method = getattr(self, method_name)
        return method(node)


class AST:
    pass


class Valuable(abc.ABC):
    def get_value(self):
        pass


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Num({self.token.type}, {self.value})'


class Str(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Str({self.value})'


class StrOp(AST):
    def __init__(self, left, add: Token, right):
        self.left = left
        self.add = add
        self.right = right

    def __str__(self):
        return f'StrOp({self.left}, {self.add}, {self.right})'


class BinOp(AST):
    def __init__(self, left, op: Token, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'BinOp({self.left}, {self.op.type}, {self.right})'


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return f'UnaryOp({self.op}, {self.expr})'


class Compound(AST):
    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children

    def __str__(self):
        res = ""
        for node in self.children:
            res += str(node) + ", "

        return f'Compound({res})'


class Var(AST, Valuable):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def get_value(self):
        return self.value

    def __str__(self):
        return f'Var({self.value})'


class Assign(AST):
    def __init__(self, left: Var, op: Token, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'Assign({self.left}, :=, {self.right})'


class NoOp(AST):
    def __str__(self):
        return 'NoOp()'


class VarDecs(AST):
    def __init__(self, variables, base_type: Token):
        self.variables = variables
        self.token = self.type = base_type

    def get_declarations(self):
        return self.variables

    def get_type(self) -> Token:
        return self.type

    def __str__(self):
        res = ""
        for var in self.variables:
            res += var.value + ', '
        return f'VarDecs(({res}), {self.type.value})'


class Program(AST):
    def __init__(self, block):
        self.block = block

    def __str__(self):
        return f'Program({self.block})'


class Block(AST):
    def __init__(self, var_decs: list, compound_statement: Compound):
        self.var_decs = var_decs
        self.compound_statement = compound_statement

    def __str__(self):
        res = ""
        for dec in self.var_decs:
            res += str(dec) + ", "
        return f'Program({res}, {self.compound_statement})'


class AbstractSymbol(abc.ABC):
    def __init__(self, name, *args):
        self.name = name

    def is_symbol(self):
        return isinstance(self, Symbol)

    def is_function(self):
        return isinstance(self, FunctionDecl)


class FunctionDecl(AbstractSymbol, Valuable):
    def __init__(self, proc_name, params, block, return_expression=None):
        super(FunctionDecl, self).__init__(proc_name)
        self.name = proc_name
        self.block = block
        self.params = params if params is not None else []
        self.return_expression = return_expression

    def get_value(self):
        return str(self)

    def __str__(self):
        return f'FunctionDecl({self.name}, {self.params}, {self.block}, {self.return_expression})'


class FunctionCall(AST):
    def __init__(self, name, actual_params, token):
        self.name = name
        self.actual_params = actual_params
        self.token = token

    def __str__(self):
        res = ""
        for param in self.actual_params:
            res += str(param) + ", "
        return f'FunctionCall({self.name}, {res}, {self.token})'


class Symbol(AbstractSymbol):
    def __init__(self, name, value=None, symbol_type=None):
        super().__init__(name)
        self.name = name
        self.value = value
        self.type = symbol_type

    def __str__(self):
        return f'{self.__class__.__name__}({self.name}, {self.value}, {self.type})'

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, value, base_type=None):
        super().__init__(name, value, base_type)


class BooleanSymbol(Symbol):
    def __init__(self, value):
        super().__init__(None, value, SymbolTypes.BOOLEAN)


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)


class NotOp(AST):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f'NotOp({self.expr})'


class BoolOp(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.__class__.__name__}({self.left}, {self.right})'


class BoolOr(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolAnd(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolNotEqual(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolGreaterThan(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolGreaterThanOrEqual(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolLessThan(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolLessThanOrEqual(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class BoolIsEqual(BoolOp):
    def __init__(self, left, right):
        super().__init__(left, right)


class IfBlock(AST):
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def __str__(self):
        return f'IfBlock({self.expr}, {self.block})'


class IfStat(AST):
    def __init__(self, if_blocks: List, else_block):
        self.if_blocks = if_blocks
        self.else_block = else_block

    def __str__(self):
        stats = ""
        for if_block in self.if_blocks:
            stats += str(if_block) + ","
        return f'IfStat({stats}, {self.else_block})'

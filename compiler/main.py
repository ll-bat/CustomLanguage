import os.path
from os.path import exists
from pprint import pprint

from compiler.interpreter import Interpreter
from compiler.parser import Parser
from compiler.semantic_analyzer import SemanticAnalyzer
from utils.errors import *


# Dy -> Dynamic Language
class Dy:
    @staticmethod
    def compile(code: str):
        try:
            # lexer = Lexer(string)
            # while lexer.get_current_token().type is not EOF:
            #     print(lexer.get_current_token())
            #     lexer.go_forward()

            parser = Parser(code)
            tree = parser.parse()
            # print(tree)

            # check for errors
            semantic_analyzer = SemanticAnalyzer(tree)
            semantic_analyzer.analyze()

            # interpret language
            interpreter = Interpreter(tree)
            interpreter.interpret()
            # print(interpreter.get_recursion_count())
        except (ParserError, SemanticError, LexerError) as ex:
            print(ex)
        except Exception as e:
            print(e)

    @staticmethod
    def compile_file(path: str):
        code = Dy.read_file(path)
        Dy.compile(code)

    @staticmethod
    def read_file(path: str):
        # provided path should not include extension
        path = "{}.dy".format(path)
        if not path.startswith('src/'):
            path = 'src/{}'.format(path)

        if not exists(path):
            raise FileNotFoundError(path + " does not exist")

        content = ""
        with open(path, 'r') as f:
            content = f.read()

        return content

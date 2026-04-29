import ir
import ast_nodes as ast

# Register __match_args__ on AST nodes for pattern matching (tagged union support)
ast.Program.__match_args__ = ("functions",)
ast.FunctionDecl.__match_args__ = ("name", "params", "body")
ast.Block.__match_args__ = ("statements",)
ast.VarDecl.__match_args__ = ("name", "init")
ast.Assign.__match_args__ = ("name", "expr")
ast.If.__match_args__ = ("cond", "then_branch", "else_branch")
ast.While.__match_args__ = ("cond", "body")
ast.Return.__match_args__ = ("expr",)
ast.Print.__match_args__ = ("expr",)
ast.IntLiteral.__match_args__ = ("value",)
ast.Var.__match_args__ = ("name",)
ast.BinOp.__match_args__ = ("left", "op", "right")
ast.Call.__match_args__ = ("func", "args")


class Lowerer:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.current_instrs = []

    def fresh_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def fresh_label(self, prefix="L"):
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"

    def emit(self, instr):
        self.current_instrs.append(instr)

    def lower_program(self, program):
        match program:
            case ast.Program(functions):
                return ir.IRProgram([self.lower_function(fn) for fn in functions])

    def lower_function(self, fn):
        match fn:
            case ast.FunctionDecl(name, params, body):
                self.current_instrs = []
                self.lower_block(body)
                return ir.IRFunction(name, params, self.current_instrs)

    def lower_stmt(self, stmt):
        match stmt:
            case ast.VarDecl(name, init):
                t = self.lower_expr(init)
                self.emit(ir.Move(name, t))

            case ast.Assign(name, expr):
                t = self.lower_expr(expr)
                self.emit(ir.Move(name, t))

            case ast.Print(expr):
                t = self.lower_expr(expr)
                self.emit(ir.Print(t))

            case ast.Return(expr):
                t = self.lower_expr(expr)
                self.emit(ir.Return(t))

            case ast.If(cond, then_branch, else_branch):
                t = self.lower_expr(cond)
                l_then = self.fresh_label("L_then")
                l_else = self.fresh_label("L_else")
                l_end = self.fresh_label("L_end")
                self.emit(ir.CJump(t, l_then, l_else))
                self.emit(ir.Label(l_then))
                self.lower_block(then_branch)
                self.emit(ir.Jump(l_end))
                self.emit(ir.Label(l_else))
                self.lower_block(else_branch)
                self.emit(ir.Label(l_end))

            case ast.While(cond, body):
                l_start = self.fresh_label("L_start")
                l_body = self.fresh_label("L_body")
                l_end = self.fresh_label("L_end")
                self.emit(ir.Label(l_start))
                t = self.lower_expr(cond)
                self.emit(ir.CJump(t, l_body, l_end))
                self.emit(ir.Label(l_body))
                self.lower_block(body)
                self.emit(ir.Jump(l_start))
                self.emit(ir.Label(l_end))

            case _:
                raise ValueError(f"Unknown statement type: {type(stmt).__name__}")

    def lower_block(self, block):
        for stmt in block.statements:
            self.lower_stmt(stmt)

    def lower_expr(self, expr):
        match expr:
            case ast.IntLiteral(value):
                t = self.fresh_temp()
                self.emit(ir.Const(t, value))
                return t

            case ast.Var(name):
                return name

            case ast.BinOp(left, op, right):
                l = self.lower_expr(left)
                r = self.lower_expr(right)
                t = self.fresh_temp()
                self.emit(ir.BinOp(t, op, l, r))
                return t

            case ast.Call(func, args):
                arg_temps = [self.lower_expr(a) for a in args]
                t = self.fresh_temp()
                self.emit(ir.Call(t, func, arg_temps))
                return t

            case _:
                raise ValueError(f"Unknown expression type: {type(expr).__name__}")

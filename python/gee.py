import re, sys, string

debug = False
dict = {}
tokens = []


#  Expression class and its subclasses
class Expression(object):
    def __str__(self):
        return ""


class BinaryExpr(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.op) + " " + str(self.left) + " " + str(self.right)


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class VarRef(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class String(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


#  Statement class and its subclasses
class Statement(object):
    def __str__(self):
        return ""


class Block(Statement):
    def __init__(self, stmts):
        self.stmts = stmts

    def __str__(self):
        result = ""
        for stmt in self.stmts:
            result += str(stmt)
        return result


class Assign(Statement):
    def __init__(self, target, expr):
        self.target = target
        self.expr = expr

    def __str__(self):
        return "= " + str(self.target) + " " + str(self.expr) + "\n"


class If(Statement):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __str__(self):
        result = "if " + str(self.condition) + "\n"
        result += str(self.then_block)
        result += "else\n"
        result += str(self.else_block)
        result += "endif\n"
        return result


class While(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        result = "while " + str(self.condition) + "\n"
        result += str(self.body)
        result += "endwhile\n"
        return result


def error(msg):
    sys.exit(msg)


def match(matchtok):
    tok = tokens.peek()
    if tok != matchtok:
        error("Expecting " + matchtok)
    tokens.next()
    return tok


# Expression parsing


def factor():
    tok = tokens.peek()
    if debug:
        print("Factor: ", tok)
    if re.match(Lexer.number, tok):
        expr = Number(tok)
        tokens.next()
        return expr
    if re.match(Lexer.identifier, tok):
        expr = VarRef(tok)
        tokens.next()
        return expr
    if re.match(Lexer.string, tok):
        expr = String(tok)
        tokens.next()
        return expr
    if tok == "(":
        tokens.next()
        expr = expression()
        match(")")
        return expr
    error("Invalid operand")
    return


def term():
    tok = tokens.peek()
    if debug:
        print("Term: ", tok)
    left = factor()
    tok = tokens.peek()
    while tok == "*" or tok == "/":
        tokens.next()
        right = factor()
        left = BinaryExpr(tok, left, right)
        tok = tokens.peek()
    return left


def addExpr():
    tok = tokens.peek()
    if debug:
        print("addExpr: ", tok)
    left = term()
    tok = tokens.peek()
    while tok == "+" or tok == "-":
        tokens.next()
        right = term()
        left = BinaryExpr(tok, left, right)
        tok = tokens.peek()
    return left


def relationalExpr():
    tok = tokens.peek()
    if debug:
        print("relationalExpr: ", tok)
    left = addExpr()
    tok = tokens.peek()
    if tok in ("<", "<=", ">", ">=", "==", "!="):
        op = tok
        tokens.next()
        right = addExpr()
        left = BinaryExpr(op, left, right)
    return left


def andExpr():
    tok = tokens.peek()
    if debug:
        print("andExpr: ", tok)
    left = relationalExpr()
    tok = tokens.peek()
    while tok == "and":
        tokens.next()
        right = relationalExpr()
        left = BinaryExpr(tok, left, right)
        tok = tokens.peek()
    return left


def expression():
    tok = tokens.peek()
    if debug:
        print("expression: ", tok)
    left = andExpr()
    tok = tokens.peek()
    while tok == "or":
        tokens.next()
        right = andExpr()
        left = BinaryExpr(tok, left, right)
        tok = tokens.peek()
    return left


# Statement parsing


def parseStmtList():
    stmts = []
    tok = tokens.peek()
    while tok is not None and tok not in ("~", "else", "endwhile", "endif"):
        stmt = parseStmt()
        stmts.append(stmt)
        tok = tokens.peek()
    return Block(stmts)


def parseStmt():
    tok = tokens.peek()
    if tok == "if":
        return ifStatement()
    if tok == "while":
        return whileStatement()
    return assign()


def assign():
    tok = tokens.peek()
    if debug:
        print("assign: ", tok)
    target = VarRef(tok)
    tokens.next()
    match("=")
    expr = expression()
    match(";")
    return Assign(target, expr)


def ifStatement():
    match("if")
    condition = expression()
    then_block = block()
    tok = tokens.peek()
    if tok == "else":
        match("else")
        else_block = block()
    else:
        else_block = Block([])
    return If(condition, then_block, else_block)


def whileStatement():
    match("while")
    condition = expression()
    body = block()
    return While(condition, body)


def block():
    match(":")
    match(";")
    match("@")
    stmts = parseStmtList()
    match("~")
    return stmts


def parse(text):
    global tokens
    tokens = Lexer(text)
    stmtlist = parseStmtList()
    print(str(stmtlist))
    return


# Lexer
class Lexer:
    special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
    relational = "<=?|>=?|==?|!="
    arithmetic = r"\+|\-|\*|/"
    string = r"'[^']*'" + "|" + r'"[^"]*"'
    number = r"\-?\d+(?:\.\d+)?"
    literal = string + "|" + number
    identifier = r"[a-zA-Z]\w*"
    lexRules = (
        literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
    )

    def __init__(self, text):
        self.tokens = re.findall(Lexer.lexRules, text)
        self.position = 0
        self.indent = [0]

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return None

    def next(self):
        self.position = self.position + 1
        return self.peek()

    def __str__(self):
        return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"


def chkIndent(line):
    ct = 0
    for ch in line:
        if ch != " ":
            return ct
        ct += 1
    return ct


def delComment(line):
    pos = line.find("#")
    if pos > -1:
        line = line[0:pos]
        line = line.rstrip()
    return line


def mklines(filename):
    inn = open(filename, "r")
    lines = []
    pos = [0]
    ct = 0
    for line in inn:
        ct += 1
        line = line.rstrip() + ";"
        line = delComment(line)
        if len(line) == 0 or line == ";":
            continue
        indent = chkIndent(line)
        line = line.lstrip()
        if indent > pos[-1]:
            pos.append(indent)
            line = "@" + line
        elif indent < pos[-1]:
            while indent < pos[-1]:
                del pos[-1]
                line = "~" + line
        print(str(ct) + " \t" + line)
        lines.append(line)
    undent = ""
    for i in pos[1:]:
        undent += "~"
    lines.append(undent)
    return lines


def main():
    global debug
    ct = 0
    for opt in sys.argv[1:]:
        if opt[0] != "-":
            break
        ct = ct + 1
        if opt == "-d":
            debug = True
    if len(sys.argv) < 2 + ct:
        print("Usage:  %s filename" % sys.argv[0])
        return
    parse("".join(mklines(sys.argv[1 + ct])))
    return


main()

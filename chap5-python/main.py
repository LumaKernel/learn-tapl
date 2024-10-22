from dataclasses import dataclass
from typing import NoReturn, Union


# t ::=
#       x           (Var)
#       (λx. t)     (Abs)
#       t t         (App)


@dataclass
class TermVar:
    name: str
    def __repr__(self):
        return self.name

@dataclass
class TermAbs:
    bind: str
    body: 'Term'
    def __repr__(self):
        return f'(λ{self.bind}. {self.body})'

@dataclass
class TermApp:
    callee: 'Term'
    arg: 'Term'
    def __repr__(self):
        return f'({self.callee} {self.arg})'

# 項
Term = Union[TermVar, TermAbs, TermApp]

# AST

# (\x. x x) (\x. x x)
t_omega = TermApp(
    TermAbs('x', TermApp(TermVar('x'), TermVar('x'))),
    TermAbs('x', TermApp(TermVar('x'), TermVar('x')))
)

print(t_omega)


class Parser:
    def __init__(self, src: str):
        self.src = src
        self.pos = 0

    def peek(self) -> str:
        if self.pos >= len(self.src):
            return ''
        return self.src[self.pos]

    def get(self) -> str:
        c = self.peek()
        self.pos += 1
        return c

    def parse_term(self) -> Term:
        self.skip_whitespace()
        c = self.peek()
        if c == '(':
            self.get()
            self.skip_whitespace()
            c = self.peek()
            if c == 'λ' or c == '\\':
                return self.parse_abs()
            else:
                return self.parse_app()
        else:
            return TermVar(self.parse_ident())

    def parse_abs(self) -> Term:
        c = self.get()
        assert c == 'λ' or c == '\\'
        self.skip_whitespace()
        bind = self.parse_ident()
        self.skip_whitespace()
        assert self.get() == '.'
        self.skip_whitespace()
        body = self.parse_term()
        self.skip_whitespace()
        assert self.get() == ')'
        return TermAbs(bind, body)

    def parse_app(self) -> Term:
        callee = self.parse_term()
        self.skip_whitespace()
        arg = self.parse_term()
        self.skip_whitespace()
        assert self.get() == ')'
        return TermApp(callee, arg)

    def parse_ident(self) -> str:
        ident = ''
        c = self.peek()
        while c.isalnum() or c == '_':
            ident += self.get()
            c = self.peek()
        assert ident != ''
        return ident

    def skip_whitespace(self):
        while self.peek().isspace():
            self.get()

def parse(src: str) -> Term:
    p = Parser(src)
    return p.parse_term()

v = parse('((\\x. x x) (\\x. x x))')
print(v)


# (λx. t1)[y := t2] := λx. t1[y := t2] (if x != y)
# (t1 t2)[y := t] := (t1[y := t] t2[y := t])
def subst(term: Term, var: str, val: Term) -> Term:
    if isinstance(term, TermVar):
        # x[y := t] := t (if x = y)
        if var == term.name:
            return val
        # x[y := t] := x (if x != y)
        else:
            return term
    elif isinstance(term, TermAbs):
        # (λx. t1)[y := t2] := λx. t1 (if x = y)
        pass
    elif isinstance(term, TermApp):
        pass
    else:
        assert_never(term)


# (\x. y)
ex1 = TermAbs('x', TermVar('y'))
# print(subst(ex1, 'y', TermVar('z'))) # (\x. z)


def assert_never(x: NoReturn) -> NoReturn:
    assert False, "Unhandled type: {}".format(type(x).__name__)

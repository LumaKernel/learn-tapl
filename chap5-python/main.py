from dataclasses import dataclass
from typing import NoReturn, Union, Optional


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

# print(t_omega)


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

v = parse('((\\x. (x x)) (\\x. (x x)))')
# print(v)

def fv(term: Term) -> set[str]:
    match term:
        case TermVar(name):
            return {name}
        case TermAbs(bind, body):
            return fv(body) - {bind}
        case TermApp(callee, arg):
            return fv(callee) | fv(arg)
        case _:
            assert_never(term)

def subst(term: Term, var: str, val: Term) -> Term:
    match term:
        case TermVar(name):
            if name == var:
                # x[y := t] = t (x == y)
                return val
            else:
                # x[y := t] = x (x != y)
                return term
        case TermAbs(bind, body):
            if fv(val) & {bind}:
                assert False, "Free variable capture"
            if bind == var:
                # (λx. t)[y := t] = λx. t (x == y)
                return term
            else:
                # (λx. t)[y := t] = λx. t[y := t] (x != y)
                return TermAbs(bind, subst(body, var, val))
        case TermApp(callee, arg):
            # (t1 t2)[y := t] = (t1[y := t] t2[y := t])
            return TermApp(subst(callee, var, val), subst(arg, var, val))
        case _:
            assert_never(term)

# (\x. y)
ex1 = TermAbs('x', TermVar('y'))
# print(subst(ex1, 'y', TermVar('z'))) # (\x. z)


def assert_never(x: NoReturn) -> NoReturn:
    assert False, "Unhandled type: {}".format(type(x).__name__)


# print(subst(parse("(\\y. ((\\y. z) (\\x. (x z))))"), "z", parse("(u (\\x. x))")))


# (\y. (\x. x y)) (\x. x)

# 定義域: 閉項
def is_value(term: Term) -> bool:
    match term:
        case TermVar(name):
            return False
        case TermAbs(bind, body):
            return True
        case TermApp(callee, arg):
            return False
        case _:
            assert_never(term)


# 定義域: 閉項 (Closure) (自由変数を持たない)
# 値域: 閉項
def step1(term: Term) -> Optional[Term]:
    assert fv(term) == set(), "term is not closed"

    match term:
        case TermVar(name):
            raise Exception("UNREACHABLE")
        case TermAbs(bind, body):
            return None
        case TermApp(callee, arg):
            if is_value(callee):
                if is_value(arg):
                    # E-AppAbs
                    match callee:
                        # callee = (\x. t_12)
                        # bind = x
                        # body = t_12
                        # arg = v_2
                        case TermAbs(bind, body):
                            return subst(
                                body,
                                bind,
                                arg,
                            )
                        case _:
                            raise Exception("UNREACHABLE")
                else:
                    # E-App2
                    arg1 = step1(arg)
                    if arg1 is None:
                        return None
                    return TermApp(
                            callee,
                            arg1,
                    )
            else:
                # E-App1
                callee1 = step1(callee)
                if callee1 is None:
                    return None
                return TermApp(
                    callee1,
                    arg,
                )
        case _:
            assert_never(term)

def is_normal_form(term: Term) -> bool:
    return step1(term) is None

# 定義域: すべての閉項
# 値域: 正規形
def eval(term: Term) -> Term:
    while not is_normal_form(term):
        term_next = step1(term)
        if term_next is None:
            break
        else:
            term = term_next
    return term


s_id = r'(\x. x)'
ex = parse(rf'((\x. (x x)) (\x. (x x)))')
# print(step1(ex))
# print(step1(step1(ex)))
print(eval(ex))
# print(eval(parse(s_id)))


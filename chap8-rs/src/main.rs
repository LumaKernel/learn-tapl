#![feature(box_patterns)]

enum Term {
    Zero,
    Succ(Box<Term>),
    Pred(Box<Term>),
    IsZero(Box<Term>),
    True,
    False,
    If {
        cond: Box<Term>,
        then_clause: Box<Term>,
        else_clause: Box<Term>,
    },
}

#[derive(Debug, PartialEq, Eq)]
enum Type {
    Nat,
    Bool,
}

fn typing(t: &Term) -> Option<Type> {
    match t {
        // T-Zero
        Term::Zero => Some(Type::Nat),
        // T-Succ
        // t: Nat
        // ===========
        // succ t: Nat
        Term::Succ(t) => {
            if let Some(Type::Nat) = typing(t) {
                Some(Type::Nat)
            } else {
                None
            }
        }
        // T-Pred
        Term::Pred(t) => {
            if let Some(Type::Nat) = typing(t) {
                Some(Type::Nat)
            } else {
                None
            }
        }
        // T-IsZero
        Term::IsZero(t) => {
            if let Some(Type::Nat) = typing(t) {
                Some(Type::Bool)
            } else {
                None
            }
        }
        // T-True
        Term::True => Some(Type::Bool),
        // T-False
        Term::False => Some(Type::Bool),
        // T-If
        Term::If {
            cond,
            then_clause,
            else_clause,
        } => {
            if let Some(Type::Bool) = typing(cond) {
                let ty_then = typing(then_clause);
                let ty_else = typing(else_clause);
                match (ty_then, ty_else) {
                    (Some(Type::Nat), Some(Type::Nat)) => Some(Type::Nat),
                    (Some(Type::Bool), Some(Type::Bool)) => Some(Type::Bool),
                    _ => None,
                }
                //if ty_then == ty_else {
                //    ty_then
                //} else {
                //    None
                //}
            } else {
                None
            }
        }
    }
}

fn main() {
    // if iszero pred 0 then true else false
    let term = Term::If {
        cond: Box::new(Term::IsZero(Box::new(Term::Pred(Box::new(Term::Zero))))),
        then_clause: Box::new(Term::True),
        else_clause: Box::new(Term::False),
    };
    println!("{:?}", typing(&term));
}

#![feature(box_patterns)]

#[derive(Debug)]
enum Term {
    True,
    False,
    If(Box<Term>, Box<Term>, Box<Term>),
    Zero,
    Succ(Box<Term>),
    Pred(Box<Term>),
    IsZero(Box<Term>),
}

fn step_calc(term: Term) -> Option<Term> {
    match term {
        // I-IfTrue
        Term::If(box Term::True, t2, _) => Some(*t2),
        // I-IfFalse
        Term::If(box Term::False, _, t3) => Some(*t3),
        // I-If
        Term::If(t1, t2, t3) => Some(Term::If(Box::new(step_calc(*t1)?), t2, t3)),
        // ..
        Term::Succ(t1) => Some(Term::Succ(Box::new(step_calc(*t1)?))),
        // ..
        Term::Pred(box Term::Zero) => Some(Term::Zero),
        // ..
        Term::Pred(box Term::Succ(t1)) => Some(*t1),
        // ..
        Term::Pred(t1) => Some(Term::Pred(Box::new(step_calc(*t1)?))),
        // ..
        Term::IsZero(box Term::Zero) => Some(Term::True),
        // ..
        Term::IsZero(box Term::Succ(_)) => Some(Term::False),
        // ..
        Term::IsZero(t1) => Some(Term::IsZero(Box::new(step_calc(*t1)?))),
        // termは正規形である
        _ => None,
    }
}

fn main() {
    // if (if true then false else true) then 0 else succ 0
    let term = Term::If(
        Box::new(Term::If(
            Box::new(Term::True),
            Box::new(Term::False),
            Box::new(Term::True),
        )),
        Box::new(Term::Zero),
        Box::new(Term::Succ(Box::new(Term::Zero))),
    );
    println!("{:?}", term);
    let term = step_calc(term);
    println!("{:?}", term);
    let term = step_calc(term.unwrap());
    println!("{:?}", term);
    let term = step_calc(term.unwrap());
    println!("{:?}", term);
}

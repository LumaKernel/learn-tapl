#![feature(box_patterns)]
// #[feature(deref_pure_trait)]

#[derive(Clone, Debug)]
enum Term {
    True,
    False,
    If(Box<Term>, Box<Term>, Box<Term>),
    Zero,
    Succ(Box<Term>),
    Pred(Box<Term>),
    IsZero(Box<Term>),
}

impl Term {
    fn is_normal_form(&self) -> bool {
        self.step_calc().is_none()
    }
    fn is_numeric_value(&self) -> bool {
        match self {
            Term::Zero => true,
            Term::Succ(t1) => t1.is_numeric_value(),
            _ => false,
        }
    }
    fn is_value(&self) -> bool {
        match self {
            Term::True | Term::False => true,
            t if t.is_numeric_value() => true,
            _ => false,
        }
    }
    fn step_calc(&self) -> Option<Term> {
        match self {
            // I-IfTrue
            Term::If(box Term::True, t2, _) => Some(*t2.clone()),
            // I-IfFalse
            Term::If(box Term::False, _, t3) => Some(*t3.clone()),
            // I-If
            Term::If(t1, t2, t3) => Some(Term::If(t1.step_calc()?.into(), t2.clone(), t3.clone())),
            // ..
            Term::Succ(t1) if t1.is_numeric_value() => Some(Term::Succ(t1.step_calc()?.into())),
            // ..
            Term::Pred(box Term::Zero) => Some(Term::Zero),
            // ..
            Term::Pred(box Term::Succ(t1)) if t1.is_numeric_value() => Some((**t1).clone()),
            // ..
            Term::Pred(t1) if t1.is_numeric_value() => Some(Term::Pred(Box::new(t1.step_calc()?))),
            // ..
            Term::IsZero(box Term::Zero) => Some(Term::True),
            // ..
            Term::IsZero(box Term::Succ(t1)) if t1.is_numeric_value() => Some(Term::False),
            // ..
            Term::IsZero(t1) => Some(Term::IsZero(t1.step_calc()?.into())),
            // termは正規形である
            _ => None,
        }
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
    let term = term.step_calc();
    println!("{:?}", term);
    let term = term.unwrap().step_calc();
    println!("{:?}", term);
    let term = term.unwrap().step_calc();
    println!("{:?}", term);
}

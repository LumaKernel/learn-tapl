use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Clone, Copy, Hash, Eq, PartialEq, Serialize, Deserialize)]
pub struct Q(usize);
// spaceは0
// Sigmaに偶数は入ってない
#[derive(Clone, Copy, Hash, Eq, PartialEq, Serialize, Deserialize)]
pub struct Sigma(usize);
impl Sigma {
    pub fn new(n: usize) -> Self {
        if n % 2 == 0 {
            panic!("Sigmaに偶数は入れられません");
        }
        Self(n)
    }
}
#[derive(Clone, Copy, Hash, Eq, PartialEq, Serialize, Deserialize)]
pub struct Gamma(usize);
impl Gamma {
    pub fn new(n: usize) -> Self {
        Self(n)
    }
}
#[derive(Clone, Copy, Hash, Eq, PartialEq, Serialize, Deserialize)]
pub enum Move {
    L,
    R,
}

#[derive(Serialize, Deserialize)]
pub struct TuringMachine {
    pub sigma: HashMap<(Q, Gamma), (Q, Gamma, Move)>,
    pub accept: Q,
    pub reject: Q,
}
impl TuringMachine {
    pub fn sigma(&self, q: Q, gamma: Gamma) -> (Q, Gamma, Move) {
        self.sigma
            .get(&(q, gamma))
            .copied()
            .unwrap_or_else(|| (Q(0), Gamma::new(0), Move::L))
    }
}

fn main() {
    // a = 1
    // b = 3
    let char_sp = Gamma::new(0);
    let char_a = Gamma::new(1);
    let char_b = Gamma::new(3);
    let state_start = Q(0);
    let state_wait_b = Q(1);
    let tm = TuringMachine {
        sigma: vec![((state_start, char_a), (state_wait_b, char_sp, Move::R))]
            .into_iter()
            .collect(),
        accept: Q(10),
        reject: Q(11),
    };
}

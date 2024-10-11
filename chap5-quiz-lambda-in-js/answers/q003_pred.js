import { show_nat_stream, show_nat_to_bool, show_nat_to_nat } from "../lib.js";

const c0 = (f) => (z) => z;
const succ = (n) => (f) => (z) => f(n(f)(z));
const pair = (a) => (b) => (f) => f(a)(b);
const fal = (t) => (f) => f;
const tru = (t) => (f) => t;
const pair0 = (p) => p(tru);
const pair1 = (p) => p(fal);

const pred = (n) =>
  pair0(n((p) => pair(pair1(p))(succ(pair1(p))))(pair(c0)(c0)));

show_nat_to_nat(pred);

import { show_nat_stream, show_nat_to_bool, show_nat_to_nat } from "./lib.js";

const c0 = (f) => (z) => z;
const succ = (n) => (f) => (z) => f(n(f)(z));
const pair = (a) => (b) => (f) => f(a)(b);
const fal = (t) => (f) => f;
const tru = (t) => (f) => t;
const pair0 = (p) => p(tru);
const pair1 = (p) => p(fal);

show_nat_to_nat((_) => c0);

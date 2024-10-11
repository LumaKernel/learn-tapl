import { show_nat_stream, show_nat_to_bool, show_nat_to_nat } from "../lib.js";

const c0 = (f) => (z) => z;
const succ = (n) => (f) => (z) => f(n(f)(z));
const c1 = succ(c0);
const c2 = succ(c1);
const pair = (a) => (b) => (f) => f(a)(b);
const fal = (t) => (f) => f;
const tru = (t) => (f) => t;
const pair0 = (p) => p(tru);
const pair1 = (p) => p(fal);
const is_zero = (n) => n((_) => fal)(tru);
const pred = (n) =>
  pair0(n((p) => pair(pair1(p))(succ(pair1(p))))(pair(c0)(c0)));

const mod3 = (n) =>
  n(
    (k) =>
      is_zero(k)(
        c1,
      )(
        is_zero(pred(k))(
          c2,
        )(
          c0,
        ),
      ),
  )(
    c0,
  );
const is3k = (n) => is_zero(mod3(n));

show_nat_to_bool(is3k);

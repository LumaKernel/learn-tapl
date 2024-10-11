import { show_nat_stream, show_nat_to_bool, show_nat_to_nat } from "../lib.js";

const c0 = (f) => (z) => z;
const succ = (n) => (f) => (z) => f(n(f)(z));
const pair = (a) => (b) => (f) => f(a)(b);
const fal = (t) => (f) => f;
const tru = (t) => (f) => t;
const pair0 = (p) => p(tru);
const pair1 = (p) => p(fal);

const c1 = succ(c0);
const c2 = succ(c1);

const is_zero = (n) => n((_) => fal)(tru);

const pred = (n) =>
  pair0(n((p) => pair(pair1(p))(succ(pair1(p))))(pair(c0)(c0)));

const and = (p) => (q) => p(q)(fal);
const or = (p) => (q) => p(tru)(q);
const not = (p) => p(fal)(tru);

const lt = (m) => (n) => not(is_zero(m(pred)(n)));
const ge = (m) => (n) => not(lt(m)(n));
const eq = (m) => (n) => and(ge(m)(n))(ge(n)(m));

/** m % n */
const mod = (m) => (n) => m((k) => eq(n)(succ(k))(c0)(succ(k)))(c0);
/**
 * m | n
 * m divides n
 */
const divides = (m) => (n) => is_zero(mod(n)(m));

const is_prime = (n) =>
  and(
    ge(n)(c2),
  )(
    pair0(
      n(
        (p) =>
          p(
            (b) => (cur) =>
              pair(
                and(
                  b,
                )(
                  or(
                    lt(
                      cur,
                    )(
                      c2,
                    ),
                  )(
                    not(
                      divides(
                        cur,
                      )(
                        n,
                      ),
                    ),
                  ),
                ),
              )(succ(cur)),
          ),
      )(
        pair(tru)(c0),
      ),
    ),
  );

show_nat_to_bool(is_prime, 30);

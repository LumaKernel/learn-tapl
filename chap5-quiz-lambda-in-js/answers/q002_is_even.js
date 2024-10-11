import { show_nat_stream, show_nat_to_bool, show_nat_to_nat } from "../lib.js";

const fal = (_) => (f) => f;
const tru = (t) => (_) => t;
const is_zero = (n) => n((b) => b(fal)(tru))(tru);

show_nat_to_bool(is_zero);

function churchNatToBigInt(cn) {
  return cn((n) => n + 1n)(0n);
}
function churchBoolToBoolean(cb) {
  return cb(true)(false);
}
function bigIntToChurchNat(/** @type bigint */ n) {
  return n > 0
    ? (f) => (z) => f(bigIntToChurchNat(n - 1n)(f)(z))
    : (f) => (z) => z;
}
function defer(/** @type number */ ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
function formatBigInt(/** @type bigint */ n, /** @type string */ width) {
  return n.toString().padStart(width, " ");
}

export async function show_nat_stream(v) {
  let k = 0n;
  while (true) {
    const value = v((t) => (f) => t);
    const next = v((t) => (f) => f);
    const output = churchNatToBigInt(value);
    console.log("v[%s] = %s", formatBigInt(k, 3), formatBigInt(output, 5));
    await defer(300);
    v = next();
    k += 1n;
  }
}

export function show_nat_to_bool(v, /** @type bigint */ to = 10n) {
  for (let n = 0n; n < to; n += 1n) {
    const cn = bigIntToChurchNat(n);
    console.log(
      "v (%s) = %s",
      formatBigInt(n, 3),
      churchBoolToBoolean(v(cn)).toString(),
    );
  }
}

export function show_nat_to_nat(v, /** @type bigint */ to = 10n) {
  for (let n = 0n; n < to; n += 1n) {
    const cn = bigIntToChurchNat(n);
    const output = churchNatToBigInt(v(cn));
    console.log(
      "v (%s) = %s",
      formatBigInt(n, 3),
      formatBigInt(output, 5),
    );
  }
}

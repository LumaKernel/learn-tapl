// ルール:
//   1引数アロー関数のみを利用する
//   関数適用と呼びだし
//   変数宣言はトップレベルのみ許可される
//   自己参照禁止

const c0 = (f) => (z) => z;
const succ = (n) => (f) => (z) => f(n(f)(z));
const pair = (a) => (b) => (f) => f(a)(b);
const fal = (t) => (f) => f;
const tru = (t) => (f) => t;

//answer(theStream);

quiz_stream();

/////// ^^^^ Write answer above here ^^^^^ ///////

function churchNatToBigInt(cn) {
  return cn((n) => n + 1n)(0n);
}
function churchBoolToBoolean(cb) {
  return cb(true)(false);
}
function bigIntToChurchNat(n) {
  return n > 0
    ? (f) => (z) => f(bigIntToChurchNat(n - 1n)(f)(z))
    : (f) => (z) => z;
}
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function quiz_stream(v) {
  while (true) {
    const value = v((t) => (f) => t);
    const next = v((t) => (f) => f);
    console.log(churchNatToBigInt(value));
    await defer(300);
    v = next();
  }
}

async function quiz_nat(v) {
  for (let n = 0n; n < 100n; n += 1n) {
    const cn = bigIntToChurchNat(n);
    console.log(n, churchBoolToBoolean(v(cn)));
  }
}

// ルール:
//   アロー関数のみを利用する
//   関数適用と呼びだし
//   変数宣言はトップレベルのみ許可される

const id = (x) => x;
const k = (x) => (y) => x;
const f = (x) => k(id);

// answer(theStream);

/////// ^^^^ Write answer above here ^^^^^ ///////

const churchNatToBigInt = (cn) => {
  return cn((n) => n + 1n)(0n);
};
const defer = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const answer = async (v) => {
  while (true) {
    const value = v((t) => (f) => t);
    const next = v((t) => (f) => f);
    console.log(churchNatToBigInt(value));
    await defer(300);
    v = next();
  }
};

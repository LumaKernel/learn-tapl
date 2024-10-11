# JSで純粋なラムダ式を実装してみよう

## ルール

- JSでラムダ式を疑似的に記述します
    - 評価戦略は値呼びになる点に注意してください
- 1引数のアロー関数が利用できます。
    - :o: `(v) => v` など
    - 引数を捨てる場合は `v => _ => v` のように書くか、 `v => () => v` のように 0引数アロー関数を利用してください
- 1引数での関数適用(呼び出し)が利用できます
    - :o: `(f) => (v) => f(v)` など
- 変数宣言は `const` を利用したトップレベルのみ許可されます
    - :o: `const c0 = (f) => (z) => z;` など
    - :x: `const f = { const id = (x) => x; return id; };` のようにローカル変数を定義するのは禁止
- 変数はそれまでに定義したものをすべて参照してよいですが、自分自信や、後続のものは参照してはいけません
    - :o:
    ```js
    const id = (x) => x;
    const f = (z) => id;
    const g = f;
    ```
    - :x: 自己参照はダメ
    ```js
    const foo = (n) => foo(n);
    ```
    - :x: 後方参照はダメ
    ```js
    const foo = (n) => bar(n);
    const bar = (x) => x;
    ```
- それ以外の構文は利用できません。括弧は自由につけて問題ありません。定義した以外のグローバルな変数を利用できません
    - :x: `if (v) return 3;` などはダメ
    - :x: `v => Number.parseInt(v)` などはダメ
- ただし、先頭に `import { ... } from "../lib.js";` をおいてください。その他の import はできません。

## 回答の書き方

`template.js` を適当にコピーして書きかえてください。 (例: `cp template.js ans_q1.js`)

なお、先頭の `import` 文以外は消してしまっても差し支えありません。完全にヒントなしで試したい場合は `template-plain.js` を代わりに利用してください。

必要に応じて作成した回答の関数やストリームを表示する関数を呼び出してください。クイズ項目自体にも使うべき関数は書かれています。

## 実行方法

DenoかBunを利用することで実行できます。

```sh
deno run ./your-answer.js
```

```sh
bun run ./your-answer.js
```

用意されている回答を実行する場合にも同様です。

```sh
deno run ./answers/some-stream.js
```

## 定義一覧

### Church Nat

自然数 $n$ を2変数f,zを受け取り関数 `(f) => (z) => f(f(...(f(z))...))` 

## クイズ一覧

### クイズ1: ゼロか判定するis_zeroを実装してください

Church Natを受けとり、0の場合にChurch true、そうでない場合にChurch falseを返す関数を定義してください。

回答は以下の形式で確認してください。

```js
// ...テンプレートは省略...

const is_zero = ...;

show_nat_to_bool(is_zero);
```

以下のように出力されれば成功です。

```sh
v (  0) = true
v (  1) = false
v (  2) = false
v (  3) = false
v (  4) = false
v (  5) = false
v (  6) = false
v (  7) = false
v (  8) = false
v (  9) = false
```

想定回答は [`./answers/q001_is_zero.js`](./answers/q001_is_zero.js) にあります。

### クイズ2: 偶数か判定するis_evenを実装してください

Church Natを受けとり、偶数の場合にChurch true、奇数の場合にChurch falseを返す関数を定義してください。

回答は以下の形式で確認してください。

```js
// ...テンプレートは省略...

const is_even = ...;

show_nat_to_bool(is_even);
```

以下のように出力されれば成功です。

```sh
v (  0) = true
v (  1) = false
v (  2) = true
v (  3) = false
v (  4) = true
v (  5) = false
v (  6) = true
v (  7) = false
v (  8) = true
v (  9) = false
```

想定回答は [`./answers/q002_is_even.js`](./answers/q002_is_even.js) にあります。


### クイズ3: 前者関数predを実装してください

Church Natを受けとり、0のときは0を、k+1のときはkを返す前者関数を実装してください。

回答は以下の形式で確認してください。

```js
// ...テンプレートは省略...

const pred = ...;

show_nat_to_nat(pred);
```

以下のように出力されれば成功です。

```sh
v (  0) =     0
v (  1) =     0
v (  2) =     1
v (  3) =     2
v (  4) =     3
v (  5) =     4
v (  6) =     5
v (  7) =     6
v (  8) =     7
v (  9) =     8
```

想定回答は [`./answers/q003-pred.js`](./answers/q003-pred.js) にあります。


### クイズ4: 3の倍数かを判定するis_3kを実装してください

Church Natを受けとり、3の倍数の場合にChurch true、そうでない場合にChurch falseを返す関数を定義してください。

回答は以下の形式で確認してください。

```js
// ...テンプレートは省略...

const is_3k = ...;

show_nat_to_bool(is_3k);
```

以下のように出力されれば成功です。

```sh
```

想定回答は [`./answers/q004_is_3k.js`](./answers/q004_is_3k.js) にあります。


### クイズX: 階乗を計算するfactを実装してください
### クイズX: 素数を判定するis_primeを実装してください
### クイズX: 約数の和を計算するdivisor_sumを実装してください

### クイズX: 自然数を列挙するnaturalsを実装してください
### クイズX: 0,1,2を繰り返し列挙するtripleを実装してください
### クイズX: 偶数を列挙するevensを実装してください
### クイズX: 素数を列挙するprimesを実装してください
### クイズX: 平方数を列挙するsquaresを実装してください


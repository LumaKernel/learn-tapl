const TRUE = (t: any) => (f: any) => t;
const FALSE = (t: any) => (f: any) => f;

const AND = (a: any) => (b: any) => a(b(TRUE)(FALSE))(FALSE);

console.log(AND(TRUE)(TRUE)); // TRUE
console.log(AND(TRUE)(FALSE)); // FALSE
console.log(AND(FALSE)(TRUE)); // FALSE
console.log(AND(FALSE)(FALSE)); // FALSE

// if a { } else { }

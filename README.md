# pylie
A very small Python library for use with computations in Lie algebras

Currently this is a short program/library I wrote to perform computations in sl2-like Lie algebras. That is, given an associative algebra A,
and the Lie algebra L arising from multiplication in A, suppose L is sl2. Then one might like to investigate the structure of L and some of its
properties. 

# Example
It turns out that such a Lie algebra is impossible to have, as h^2 has similar properties to I_2 in (the actual) gl2. Of course, one
can use the very same bracket for writing computations in terms of the standard basis elements of sl2.

Using h^2 as our guiding example, we would like to show that h^2 is central in L. So we set a = xy + yx - h^2. Then one sees that our first 
choice doesn't quite work out.

![alt text](https://i.imgur.com/QBUGIYw.png)

Thus, we don't immediately see that h^2 is central in L. However, if we observe what would need to be done to make [x, a] = 0 in the 
above computations, then we can try b = xy + yx + (1/2) h^2.

![alt text](https://i.imgur.com/rNNNrx0.png)

Thus we have show that b in L is a central element. Since sl2 is simple, hence so is L. This means b = 0, which allows us to conclude that 
0 = xy + yx + (1/2)h^2.

Proceeding in a similiar manner will yield a contradiction.

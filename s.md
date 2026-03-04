This lecture covers the fundamental concepts of number theory essential for cryptography, focusing on how integers relate through division.

1. Divisibility and Divisors

The concept of divisibility describes a relationship between two integers where one can be expressed as a multiple of the other without a remainder.


Definition: For any two integers $a$ and $b$ (where $b \neq 0$), we say $b$ divides $a$ if there exists an integer $m$ such that:

$a = m \cdot b$

Notation: This is denoted as $b \mid a$. If $b$ does not divide $a$, we write $b \nmid a$.

Terminology: When $b \mid a$, we call $b$ a divisor or factor of $a$.


Examples:


$13 \mid 182$ because $182 = 14 \times 13$.

$17 \mid 0$ because $0 = 0 \times 17$.

The divisors of $24$ are $\{\pm 1, \pm 2, \pm 3, \pm 4, \pm 6, \pm 8, \pm 12, \pm 24\}$.


2. Properties of Divisibility

Divisibility follows several algebraic rules that are frequently used to simplify proofs and modular arithmetic operations:


Unit Divisors: If $a \mid 1$, then $a = \pm 1$.

Mutual Divisibility: If $a \mid b$ and $b \mid a$, then $a = \pm b$.

Divisibility of Zero: Any non-zero integer $b$ divides $0$ ($b \mid 0$).

Transitivity: If $a \mid b$ and $b \mid c$, then $a \mid c$.

Example: Since $11 \mid 66$ and $66 \mid 198$, it follows that $11 \mid 198$.



Linearity: If $b \mid g$ and $b \mid h$, then $b$ divides any linear combination of $g$ and $h$:

$b \mid (m \cdot g + n \cdot h) \quad \text{for any integers } m, n$


3. The Division Algorithm

Despite its name, the Division Algorithm is a theorem stating that for any integer $a$ and a positive integer $n$, there exist unique integers $q$ (quotient) and $r$ (remainder) such that:

$a = q \cdot n + r \quad \text{where } 0 \le r < n$


The remainder $r$ is often called the residue of $a$ modulo $n$.

The quotient is calculated as $q = \lfloor a/n \rfloor$, where $\lfloor \cdot \rfloor$ is the floor function.


Examples:


For $a = 11, n = 7$:

$11 = 1 \cdot 7 + 4 \implies q = 1, r = 4$

For $a = -11, n = 7$:

$-11 = -2 \cdot 7 + 3 \implies q = -2, r = 3$

(Note: The remainder $r$ must always be non-negative and less than $n$.)



4. Greatest Common Divisor (GCD)

The Greatest Common Divisor of two integers $a$ and $b$ is the largest positive integer that divides both $a$ and $b$.


Definition: $\text{gcd}(a, b) = \max \{k : k \mid a \text{ and } k \mid b\}$.

Properties:

Since we require the GCD to be positive, $\text{gcd}(a, b) = \text{gcd}(|a|, |b|)$.

$\text{gcd}(60, 24) = 12$ because the common divisors are $\{1, 2, 3, 4, 6, 12\}$, and $12$ is the largest.




5. Relatively Prime Property

Two integers $a$ and $b$ are said to be relatively prime (or coprime) if their only common positive integer factor is $1$.


Condition: $a$ and $b$ are relatively prime if and only if:

$\text{gcd}(a, b) = 1$

This property is crucial in cryptography (e.g., RSA) for ensuring that modular inverses exist.

## List of algorithms and explanation

### `memoised-prime-sieve.py`

- **Testing prime numbers using a memoised, dynamically-extending sieve of Eratosthenes (up to the square root of the input).**

This was a challenging algorithm to implement, but became surprisingly elegant once recursion was introduced to extend the sieve.

This was inspired by a (long) "one-liner" non-memoised Haskell implementation, which I found mind-boggling when I first saw it.

To find out whether or not n is prime, we maintain a record `prime` of whether `[0, ..., k]` are prime/non-prime (`True`/`False`), or untested (`None`).

When `is_prime(n)` is called, if `n` is already known to be (non-)prime, that information can be returned immediately.

Otherwise the list `prime` is extended if necessary, and all primes up to `sqrt(n)` are tested to see if they are factors of `n`.

First the known primes are tested. If no factors are found, we implement the sieve of Eratosthenes by recursively calling `is_prime` on each number `r` up to `sqrt(n)`. These recursive calls have the effect of sieving each number `r` by all known primes up to `sqrt(r)`, and automatically updating the relevant records (e.g. setting `prime[r]`) -- quite elegant!

In the process, we check if `r` is a new prime factor of `n`. If so, we can stop sieving -- any new information we found about (non-)primality of those numbers has been recorded for future use.

To achieve this sieving, we maintain a sorted list of CONSECUTIVE primes -- possibly smaller than `k` -- which are a subset of the indices where `prime[i]` is `True`. (This list is called `primes`.)

If our sieving has uncovered any new primes adjacent to this list, we add them to the list of consecutive primes.

To maintain the list more efficiently, we also keep track of the largest range of CONSECUTIVE numbers `0 ... m` for which primality is known to be true or false -- a superset of `primes`. The last such index is recorded in variable `cts_until`.

*P.S. I'm sure you are deeply concerned to ask if `0` is prime or not? I'll just observe that every natural number divides it with a remainder of zero. How about negative numbers? Please refer to the zeroes of the Riemann zeta function for further details and stop pestering me.*

from math import isqrt

# Memoised sieve-of-Eratosthenes prime testing

# To find out whether or not n is prime, we maintain a record ("prime")
# of whether [0, ..., k] are prime/non-prime (T/F), or untested (None).

# When is_prime(n) is called, if n is already known to be (non-)prime,
# that information can be returned immediately.

# Otherwise the list prime is extended if necessary, and all primes up to
# sqrt(n) are tested to see if they are factors of n.

# First the known primes are tested. If no factors are found,
# we use the sieve of Eratosthenes to progressively check each number r
# up to sqrt(n) for primality, recording the result in prime[r], and then
# checking if r is a new prime factor of n.

# To achieve this, we maintain a sorted list of CONSECUTIVE primes -- possibly
# smaller than k -- which are a subset of the indices where prime[i] is True.
# (This list is called "primes".)

# If our sieving has uncovered any new primes adjacent to this list,
# we add them to the list of consecutive primes.

# To maintain this list more efficiently, we also keep track of
# the largest range of CONSECUTIVE numbers 0...m, a superset of primes,
# for which primality is known to be true or false.
# The last such index is recorded in variable cts_until.


prime = [False, False, True]
primes = [2]
cts_until = 2

# prime[i] is either a boolean (if it is known to be prime/not prime),
# or None if not known.
# primes is a (sorted) list of numbers known to be prime, such that prime[i]
# is known for all values up to the last prime.
# cts_until is the largest index m where prime[i] is not None for all i <= m


def is_prime(n):
    global primes, prime, cts_until
    
    # Is n known (not) to be prime?
    if n <= len(prime) - 1 and prime[n]:
        return prime[n]

    # Extend list prime so we can later store the answer (T/F) for n
    prime.extend((n - len(prime) + 1) * [None])
    
    # First, check n against the known primes
    for p in primes:
        if n % p == 0:
            prime[n] = False
            break
    
    # If this hasn't identified any prime factors of n, we need to
    # extend our sieve (up to isqrt(n)), checking for new prime factors of n.
    if prime[n] is None:
        lim = isqrt(n)  # The largest possible prime factor of n
        
        for r in range(cts_until + 1, lim + 1):
            # If r has been sieved out (is known not to be prime), ignore it
            if prime[r] is False:
                continue
            # If r is known to be prime (from a previous call to is_prime),
            # check if r divides n.
            # If we don't know whether or not r is prime, we can check by
            # recursively calling is_prime(r), which has the side-effect of
            # updating cts_until and primes if necessary.
            # If r divides n, stop sieving: n is now known to be non-prime.
            else:
                if prime[r] or is_prime(r):
                    if n % r == 0:
                        prime[n] = False
                        break
    
    # If we got here without setting prime[n] (to False),
    # then we extended the sieve up to the square root of n,
    # but found no prime factors -- so n must be prime.
    if prime[n] is None:
        prime[n] = True
    
    # It can happen that prime[i] is now known
    # for a larger range of 0 <= i <= k, where k is greater than cts_until.
    # This requires updating cts_until and primes.
    for i in range(cts_until + 1, len(prime) + 1):
        if i == len(prime) or prime[i] is None:
            # Either prime[i] is known for all indices (i == len(prime)),
            # or we found the first i where prime[i] is unknown.
            # Either way, the continuous range of known indices is <= i - 1
            cts_until = i - 1
            break
        elif prime[i]:
            # This prime is the next one after the list of primes,
            # so add it to the list (no need to update cts_until here)
            primes.append(i)
    
    return prime[n]
 

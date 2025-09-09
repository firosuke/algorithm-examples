from math import isqrt

# Memoised sieve-of-Eratosthenes prime testing
# At the moment there is a small bug in the way cts_until / primes are extended, which occurs if the input comes in a zig-zaggy order. E.g.:
# is_prime(3); is_prime(5); is_prime(4); is_prime(7)
# resulting in primes==[2,3,7] and cts_until==3. Not too hard to fix, but I need to stop here for now. :-)

prime = [False, False, True]
primes = [2]
cts_until = 2

# prime[i] is either a boolean (if it is known to be prime/not prime), or None if not known.
# primes is a (sorted) list of numbers known to be prime, such that prime[i] is known for all values up to the last prime.
# Whenever is_prime(n) is called, if n is already known (not) to be prime, we immediately return the answer.
# Otherwise, we extend prime to have length (n + 1), find out whether n is prime, store that information in prime[n] for future use, and return the answer.
# To find out whether n is prime or not, we use a dynamic sieve-of-Eratosthenes to discover primes and non-primes <= sqrt(n).
# First we check if any known primes 
# cts_until is the largest prime such that prime[i] is not None for all i <= cts_until
# primes is the list of all primes up to and including cts_until


def is_prime(n):
    global cts_until, primes, prime
    
    # Is n known (not) to be prime?
    if n <= len(prime) - 1 and prime[n]:
        return prime[n]

    prime.extend((n - len(prime) + 1) * [None])
    
    # Check n against the known primes
    for p in primes:
        if n % p == 0:
            prime[n] = False
            return False
    
    lim = isqrt(n)  # The largest possible factor of n

    # Sieve out all multiples of known primes, up to lim
    # (This part is not entirely lazy -- some of this work could have been postponed in theory -- but it seems to be very ugly. I'll leave that as a TODO.)
    for p in primes:
        for i in range((cts_until + 1) + -(cts_until + 1) % p, lim + 1, p):
            prime[i] = False
        
    # Extend the sieve fully up to lim, finding any new primes if any, and check for prime factors of n
    for r in range(cts_until + 1, lim + 1):
        # If r is known not to be prime, ignore it
        if prime[r] is False:
            continue

        # The first number we encounter which is not known to be prime,
        # has not been sieved out. Therefore it is prime!
        # Sieve out all multiples of this new prime, up to lim
        if prime[r] is None:
            prime[r] = True
            primes.append(r)
            cts_until = r
            for i in range(2 * r, lim + 1, r):
                prime[i] = False
        
        # If we reach this point, r must be a prime.
        # Check if it is a factor of n.
        # If so, don't investigate further -- be lazy and just answer "no"
        if n % r == 0:
            prime[n] = False
            if None not in prime[cts_until + 1:n]:
              cts_until = n
            return False
    # If we got here, we extended the sieve up to the square root of n, but found no prime factors
    prime[n] = True
    # It can happen that prime[i] is now known for all i < n. In which case cts_until can be increased to n, and n can be added to the list of primes <= cts_until.
    if None not in prime[primes[-1] + 1:n + 1]:
      cts_until = n
      primes.append(n)
    return True
 

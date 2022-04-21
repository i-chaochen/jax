# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for pseudo-random number generation.

The ``jax.random`` package provides a number of routines for deterministic
generation of sequences of pseudorandom numbers.

Basic usage
-----------

>>> seed = 1701
>>> num_steps = 100
>>> key = jax.random.PRNGKey(seed)
>>> for i in range(num_steps):
...   key, subkey = jax.random.split(key)
...   params = compiled_update(subkey, params, next(batches))  # doctest: +SKIP

PRNG Keys
---------

Unlike the *stateful* pseudorandom number generators (PRNGs) that users of NumPy and
SciPy may be accustomed to, JAX random functions all require an explicit PRNG state to
be passed as a first argument.
The random state is described by two unsigned 32-bit integers that we call a **key**,
usually generated by the :py:func:`jax.random.PRNGKey` function::

    >>> from jax import random
    >>> key = random.PRNGKey(0)
    >>> key
    DeviceArray([0, 0], dtype=uint32)

This key can then be used in any of JAX's random number generation routines::

    >>> random.uniform(key)
    DeviceArray(0.41845703, dtype=float32)

Note that using a key does not modify it, so reusing the same key will lead to the same result::

    >>> random.uniform(key)
    DeviceArray(0.41845703, dtype=float32)

If you need a new random number, you can use :meth:`jax.random.split` to generate new subkeys::

    >>> key, subkey = random.split(key)
    >>> random.uniform(subkey)
    DeviceArray(0.10536897, dtype=float32)

Advanced
--------

Design and Context
==================

**TLDR**: JAX PRNG = `Threefry counter PRNG <http://www.thesalmons.org/john/random123/papers/random123sc11.pdf>`_
+ a functional array-oriented `splitting model <https://dl.acm.org/citation.cfm?id=2503784>`_

See `docs/design_notes/prng.md <https://github.com/google/jax/blob/main/docs/design_notes/prng.md>`_
for more details.

To summarize, among other requirements, the JAX PRNG aims to:

1.  ensure reproducibility,
2.  parallelize well, both in terms of vectorization (generating array values)
    and multi-replica, multi-core computation. In particular it should not use
    sequencing constraints between random function calls.

Advanced RNG configuration
==========================

JAX provides several PRNG implementations (controlled by the
`jax_default_prng_impl` flag).

-   **default**
    `A counter-based PRNG built around the Threefry hash function <http://www.thesalmons.org/john/random123/papers/random123sc11.pdf>`_.
-   *experimental* A PRNG that thinly wraps the XLA Random Bit Generator (RBG) algorithm. See
    `TF doc <https://www.tensorflow.org/xla/operation_semantics#rngbitgenerator>`_.

    -   "rbg" uses ThreeFry for splitting, and XLA RBG for data generation.
    -   "unsafe_rbg" exists only for demonstration purposes, using RBG both for
        splitting (using an untested made up algorithm) and generating.

    The random streams generated by these experimental implementations haven't
    been subject to any empirical randomness testing (e.g. Big Crush). The
    random bits generated may change between JAX versions.

The possible reasons not use the default RNG are:

1.  it may be slow to compile (specifically for Google Cloud TPUs)
2.  it's slower to execute on TPUs

Here is a short summary:

.. table::
   :widths: auto

   =================================   =================  ===  ==========
   Property                            ThreeFry, default  rbg  unsafe_rbg
   =================================   =================  ===  ==========
   Fast on TPU                                             ✅   ✅
   always correct w/ scan               ✅                 ✅
   always correct w/ remat              ✅                 ✅
   identical across CPU/GPU/TPU         ✅                 ✅
   identical across JAX/XLA versions    ✅
   identical across shardings           ✅
   =================================   =================  ===  ==========

"""

# TODO(frostig): replace with KeyArray from jax._src.random once we
# always enable_custom_prng
from jax._src.prng import PRNGKeyArray
KeyArray = PRNGKeyArray

from jax._src.random import (
  PRNGKey as PRNGKey,
  bernoulli as bernoulli,
  beta as beta,
  categorical as categorical,
  cauchy as cauchy,
  choice as choice,
  default_prng_impl as default_prng_impl,
  dirichlet as dirichlet,
  double_sided_maxwell as double_sided_maxwell,
  exponential as exponential,
  fold_in as fold_in,
  gamma as gamma,
  gumbel as gumbel,
  laplace as laplace,
  logistic as logistic,
  loggamma as loggamma,
  maxwell as maxwell,
  multivariate_normal as multivariate_normal,
  normal as normal,
  pareto as pareto,
  permutation as permutation,
  poisson as poisson,
  rademacher as rademacher,
  randint as randint,
  random_gamma_p as random_gamma_p,
  rbg_key as rbg_key,
  shuffle as shuffle,
  split as split,
  t as t,
  threefry_2x32 as threefry_2x32,
  threefry2x32_key as threefry2x32_key,
  threefry2x32_p as threefry2x32_p,
  truncated_normal as truncated_normal,
  uniform as uniform,
  unsafe_rbg_key as unsafe_rbg_key,
  weibull_min as weibull_min,
)

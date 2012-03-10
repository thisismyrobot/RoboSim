The Gist
========

Finally dev'ing a hunch - can you train a Neural Network using just "good" or
"bad" as feedback?

I say a Neural Network for now, but I will use whatever "brain" seems to work.

That said and done, this may just all "turn to custard" and I'll move onto
something else...

So far
======

Well, I've managed to get it bascially working - essentially if the output is
"bad" it is slightly mutated and tried again until it is "good" at which time
it forms part of a training set. The set is fixed length because old
"knowledge" just isn't as important as current "knowledge".

Gates
=====

Goals to achieve in order to ensure that time isn't wasted if there is a
massive fundamental flaw :)

 1. XOR training replication - Done
 2. Multi-output training replication - Done
 3. Analogue inputs
 4. Linear analogue outputs
 5. A set of tests to help understand the effects of the variables

Requirements
============

This has been developed/tested on:
 * Ubuntu 11.10
 * Python 2.7.2+

# Pole and particles

A system contains a pre-defined number of particles (n) moving left or right along a pole of
pre-defined length (l) at a pre-defined constant velocity (v).

The following rules apply in this system:
- When a particle reaches either end of the pole, it drops off
- If particles collide, they reverse direction

At the beginning of the simulation, the positions of the particles on the pole are known, but the
direction of their movement is unknown.

What is:
- The earliest possible time for all the particles to drop off
- The latest possible time for all the particles to drop off

What direction are the particles moving at the beginning of the simulation for:
- All particles to drop off at the earliest possible time
- All particles to drop off at the latest possible time

## Tests
To run tests: `python -m doctest -v simulation.py`

## Sample
Variables:
- Starting positions: [11, 12, 7, 13, 176, 23, 191]
- Length of pole: 214
- Velocity: 1

Results:
- Expected earliest possible time for all the particles to drop off: 39
- Expected latest possible time for all the particles to drop off: 208

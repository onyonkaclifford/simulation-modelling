import itertools
from enum import Enum
from typing import List, Generator, Tuple


Direction = Enum("Direction", "RIGHT LEFT")


class Particle:
    """
    An object that can move either to the right or to the left
    """

    def __init__(self, position: int, direction: Direction):
        self.position = position
        self.direction = direction

    def change_direction(self) -> None:
        """ Reverses the direction of the particle

        >>> particle1 = Particle(1, Direction.RIGHT)
        >>> particle1.change_direction()
        >>> particle1.direction == Direction.LEFT
        True

        >>> particle2 = Particle(2, Direction.LEFT)
        >>> particle2.change_direction()
        >>> particle2.direction == Direction.RIGHT
        True
        """
        self.direction = Direction.LEFT if self.direction == Direction.RIGHT else Direction.RIGHT

    def change_position(self, steps: float) -> None:
        """ Changes the position of a particle by adding steps to the current position if the particle is moving right,
        or subtracting steps if the particle is moving left

        >>> particle = Particle(1, Direction.RIGHT)
        >>> particle.change_position(5)
        >>> particle.position == 6
        True

        :param steps: number of steps the particle's position changes by
        """
        self.position = self.position + steps if self.direction == Direction.RIGHT else self.position - steps


class Pole:
    """
    A 1D line that can hold particles that can each move either to the right or to the left at constant velocity
    """

    def __init__(self, length: int, velocity: int, particles: List[Particle]):
        self.length = length
        self.velocity = velocity
        self.particles = particles
        self.removed_particles = []
        self.times_of_particles_removal = [-1 for _ in particles]

    def is_particle_to_be_removed(self, idx: int) -> bool:
        """ Checks if a particle satisfies the requirements necessary for it to be removed from the pole

        >>> particle1 = Particle(-1, Direction.RIGHT)
        >>> particle2 = Particle(5, Direction.RIGHT)
        >>> particle3 = Particle(6, Direction.RIGHT)
        >>> pole = Pole(5, 1, [particle1, particle2, particle3])
        >>> pole.is_particle_to_be_removed(0)
        True
        >>> pole.is_particle_to_be_removed(1)
        False
        >>> pole.is_particle_to_be_removed(2)
        True

        :param idx: index of particle being checked
        :return: bool
        """
        return self.particles[idx].position > self.length or self.particles[idx].position < 0

    def is_particle_removed(self, idx: int) -> bool:
        """ Checks if a particle has already been removed from the pole

        >>> particle1 = Particle(-1, Direction.RIGHT)
        >>> particle2 = Particle(5, Direction.RIGHT)
        >>> pole = Pole(5, 1, [particle1, particle2])
        >>> pole.removed_particles.append(pole.particles[0])
        >>> pole.is_particle_removed(0)
        True
        >>> pole.is_particle_removed(1)
        False

        :param idx: index of particle being checked
        :return: bool
        """
        return self.particles[idx] in self.removed_particles

    def are_particles_in_same_position(self, indices: List[int]) -> bool:
        """ Checks if a list of particles are in the same position

        >>> particle1 = Particle(1, Direction.RIGHT)
        >>> particle2 = Particle(5, Direction.RIGHT)
        >>> particle3 = Particle(5, Direction.RIGHT)
        >>> pole = Pole(5, 1, [particle1, particle2, particle3])
        >>> pole.are_particles_in_same_position([0, 1])
        False
        >>> pole.are_particles_in_same_position([1, 2])
        True

        :param indices: list of indices of the particles to be checked
        :return: bool
        """
        return all([self.particles[i].position == self.particles[indices[0]].position for i in indices])

    def are_particles_moving_in_same_direction(self, indices: List[int]) -> bool:
        """ Checks if a list of particles are moving in the same direction

        >>> particle1 = Particle(1, Direction.RIGHT)
        >>> particle2 = Particle(5, Direction.RIGHT)
        >>> particle3 = Particle(5, Direction.LEFT)
        >>> pole = Pole(5, 1, [particle1, particle2, particle3])
        >>> pole.are_particles_moving_in_same_direction([0, 1])
        True
        >>> pole.are_particles_moving_in_same_direction([1, 2])
        False

        :param indices: list of indices of the particles to be checked
        :return: bool
        """
        return all([self.particles[i].direction == self.particles[indices[0]].direction for i in indices])

    def move_particle(self, idx: int, steps: float, current_time: int) -> None:
        """ Moves a particle by a certain number of steps

        >>> particle1 = Particle(2, Direction.RIGHT)
        >>> particle2 = Particle(2, Direction.LEFT)
        >>> pole = Pole(5, 1, [particle1, particle2])
        >>> pole.move_particle(0, 1, 1)
        >>> pole.move_particle(1, 1, 1)
        >>> particle1.position == 3
        True
        >>> particle2.position == 1
        True

        :param idx: index of particle being moved
        :param steps: number of steps to move the particle by
        :param current_time: the current state of the simulation clock
        """
        self.particles[idx].change_position(steps)
        if self.is_particle_to_be_removed(idx):
            self.removed_particles.append(self.particles[idx])
            self.times_of_particles_removal[idx] = current_time

    def simulate(self, current_time: int) -> None:
        """ Simulate movement of particles along the pole

        >>> particle1 = Particle(1, Direction.RIGHT)
        >>> particle2 = Particle(2, Direction.LEFT)
        >>> pole = Pole(5, 1, [particle1, particle2])
        >>> pole.simulate(1)
        >>> particle1.direction == Direction.LEFT
        True
        >>> particle1.position == 1
        True
        >>> particle2.direction == Direction.RIGHT
        True
        >>> particle2.position == 2
        True
        >>> pole.simulate(2)
        >>> pole.is_particle_removed(0)
        False
        >>> pole.is_particle_removed(1)
        False
        >>> pole.simulate(3)
        >>> pole.is_particle_removed(0)
        True
        >>> pole.is_particle_removed(1)
        False

        :param current_time: the current state of the simulation clock
        """
        mini_steps = 0.5
        for _ in range(int(self.velocity / mini_steps)):
            i = 0
            while i < len(self.particles):
                if not self.is_particle_removed(i):
                    num_of_particles_changed = 0
                    try:
                        while self.are_particles_in_same_position([i, i + num_of_particles_changed + 1]):
                            if not self.are_particles_moving_in_same_direction([i, i + num_of_particles_changed + 1]):
                                num_of_particles_changed += 1
                                self.particles[i + num_of_particles_changed].change_direction()
                                self.move_particle(i + num_of_particles_changed, mini_steps, current_time)
                    except IndexError:
                        pass
                    if num_of_particles_changed > 0:
                        self.particles[i].change_direction()
                    self.move_particle(i, mini_steps, current_time)
                    i += num_of_particles_changed
                i += 1


class World:
    """
    An object that runs the whole simulation process
    """

    def __init__(self, poles: List[Pole]):
        self.poles = poles
        self.removed_poles = {}
        self.current_time = 0

    def simulate(self) -> Generator:
        """ Run the simulation one time unit at a time while yielding control after each run so as to check the current
        state of the world, if such a need arises

        >>> particle1 = Particle(1, Direction.RIGHT)
        >>> particle2 = Particle(2, Direction.LEFT)
        >>> pole1 = Pole(5, 1, [particle1, particle2])
        >>> world = World([pole1])
        >>> _ = [t for t in world.simulate()]
        >>> world.removed_poles[0] == pole1
        True
        """
        while len(self.poles) > len(self.removed_poles.keys()):
            yield self.current_time
            self.current_time += 1
            for i, pole in enumerate(self.poles):
                if i not in self.removed_poles.keys():
                    pole.simulate(self.current_time)
                    if len(pole.particles) == len(pole.removed_particles):
                        idx = self.poles.index(pole)
                        self.removed_poles[idx] = pole
        yield self.current_time


def get_direction_permutations(number_of_particles: int) -> List[Tuple[Direction, Direction]]:
    """ Returns all the possible direction permutations that can be obtained from a certain number of particles

    >>> perms = get_direction_permutations(2)
    >>> len(perms)
    4
    >>> (Direction.RIGHT, Direction.LEFT) in perms
    True
    >>> (Direction.LEFT, Direction.RIGHT) in perms
    True
    >>> (Direction.RIGHT, Direction.RIGHT) in perms
    True
    >>> (Direction.LEFT, Direction.LEFT) in perms
    True

    :param number_of_particles: total number of particles whose possible direction permutations are required
    :return: List[Tuple[Direction, Direction]]
    """
    directions = [Direction.RIGHT, Direction.LEFT]
    permutations = [i for i in itertools.product(directions, repeat=number_of_particles)]
    return permutations


def main(length_of_pole: int, velocity: int, starting_positions: List[int], verbose: boolean = True) -> Tuple[int, int]:
    """The program's entry point
    
    >>> main(214, 1, [11, 12, 7, 13, 176, 23, 191], False)
    (39, 208)
    
    :param length_of_pole: how long the pole is
    :param velocity: how fast the particles move left or right along the pole
    :param starting_positions: location of particles at the beginning of the simulation
    :param verbose: whether to print results of the simulation
    :return: Tuple[int, int]
    """
    starting_positions.sort()
    direction_permutations = get_direction_permutations(len(starting_positions))
    direction_permutations_char = [["R" if j == Direction.RIGHT else "L" for j in i] for i in direction_permutations]
    poles = []
    
    if verbose:
        print("Starting positions:", starting_positions, "\n")

    for permutation in direction_permutations:
        particles = []
        for idx, starting_position in enumerate(starting_positions):
            particles.append(Particle(starting_position, permutation[idx]))
        poles.append(Pole(length_of_pole, velocity, particles))

    world = World(poles)
    _ = [t for t in world.simulate()]

    times_of_particles_removal = []
    for pole in poles:
        times_of_particles_removal.append(pole.times_of_particles_removal)

    earliest_drop_off_time = -1
    latest_drop_off_time = -1
    for d, t in zip(direction_permutations_char, times_of_particles_removal):
        maximum = max(t)
        earliest_drop_off_time = maximum if earliest_drop_off_time == -1 or maximum < earliest_drop_off_time \
            else earliest_drop_off_time
        latest_drop_off_time = maximum if latest_drop_off_time == -1 or maximum > latest_drop_off_time \
            else latest_drop_off_time
        if verbose:
            print(f"Particles whose starting directions are {d} drop off at {t}")
    if verbose:
        print()

    earliest_to_drop = {earliest_drop_off_time: []}
    latest_to_drop = {latest_drop_off_time: []}
    for d, t in zip(direction_permutations_char, times_of_particles_removal):
        maximum = max(t)
        if maximum == earliest_drop_off_time:
            earliest_to_drop[earliest_drop_off_time].append(d)
        if maximum == latest_drop_off_time:
            latest_to_drop[latest_drop_off_time].append(d)
    
    if verbose:
        print(
            f"Permutations whose particles drop off earliest: "
            f"{earliest_to_drop[earliest_drop_off_time]} at time {earliest_drop_off_time}"
        )
        print(
            f"Permutations whose particles drop off latest: "
            f"{latest_to_drop[latest_drop_off_time]} at time {latest_drop_off_time}"
        )
    
    return earliest_drop_off_time, latest_drop_off_time


if __name__ == "__main__":
    time1, time2 = main(214, 1, [11, 12, 7, 13, 176, 23, 191])

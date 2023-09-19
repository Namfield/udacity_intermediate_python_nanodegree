"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can Override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator
import models
from datetime import datetime
import itertools


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""

class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can Override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        # the operation corresponding to either <=, ==, or >= - 
        # Python's operator module makes these available to us as operator.le, operator.eq, and operator.ge
        self.op = op
        # the reference value to compare
        self.value = value

    # makes instance objects of this type behave as callables
    # (The __call__ magic method in Python allows an object to be called as if it were a function)
    # "calling" the AttributeFilter with a CloseApproach object will get the attribute of interest (self.get(approach))
    # and compare it (via self.op) to the reference value (self.value), 
    # returning either True or False, representing whether that close approach satisfies the criterion.
    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must Override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Return a string representation of the class AttributeFilter."""
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"

# a class supported filter on the date attribute. 
class DateFilter(AttributeFilter):
    """A derived class to filter the date attribute of a given CloseApproach."""

    @classmethod
    def get(cls, approach):
        """Override the get method to Return the date component of the time attribute of the approach object."""
        # date() to convert the datetime object to date
        return approach.time.date()

# a class supported filter on the distance attribute. 
class DistanceFilter(AttributeFilter):
    """A derived class to filter the distance attribute of a given CloseApproach."""

    @classmethod
    def get(cls, approach):
        """Override the get method to Return the distance attribute of the approach object."""
        return approach.distance

# a class supported filter on the velocity attribute.
class VelocityFilter(AttributeFilter):
    """A derived class to filter the velocity attribute of a given CloseApproach."""

    @classmethod
    def get(cls, approach):
        """Override the get method to Return the velocity attribute of the approach object."""
        return approach.velocity

# a class supported filter on the diameter attribute.
class DiameterFilter(AttributeFilter):
    """A derived class to filter the diameter attribute of a given CloseApproach."""

    @classmethod
    def get(cls, approach):
        """Override the get method to Return the diameter attribute of the approach object."""
        return approach.neo.diameter
# a class supported filter on the hazardous attribute.
class HazardousFilter(AttributeFilter):
    """A derived class to filter the hazardous attribute of a given CloseApproach."""

    @classmethod
    def get(cls, approach):
        """Override the get method to Return the hazardous attribute of the approach object."""
        return approach.neo.hazardous

def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    # Decide how you will represent your filters.
    # we iterate through each of the input arguments and check if they have a value. 
    # If a value is present, we create an instance of the corresponding filter class and 
    # add it to a filters list.
    
    # a collection of filters
    filters = []

    # apply the filters
    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        filters.append(DiameterFilter(operator.le, diameter_max))
    # differentiate between hazardous being False (from --not-hazardous) and None (from no option).
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))
    
    return filters

def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    # Produce at most `n` values from the given iterator.
    if not n or n <= 0:
        return iterator
    else:
        # create a new iterator that produces at n elements from the original iterator
        return itertools.islice(iterator, n)

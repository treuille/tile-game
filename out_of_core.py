"""A set of out-of-core data structures so that I can search larger boards."""

import os
from typing import List
import numpy as np
import random
import pickle


class IntSet:
    """This class implements add-only, set-like semantics for a large number of Python
    ints."""

    def __init__(self, items_per_bundle: int = 1000000):
        """
        Constucts a new IntSet.

        Parameters
        ----------
        items_per_bundle: int - the number of ints we store in each mem-mapped array
        """
        self._current_bundle: set = set()
        self._frozen_bundles: List[np.memmap] = []
        self._items_per_bundle = items_per_bundle
        self._data_dir: str = "./dat"

        # Create a fresh data directory
        os.system(f'rm -rf "{self._data_dir}" && mkdir -v "{self._data_dir}"')

    def __contains__(self, item: int) -> bool:
        """True if item is in the set."""
        if item in self._current_bundle:
            return True
        for frozen_bundle in self._frozen_bundles:
            index = np.searchsorted(frozen_bundle, item)
            if index == self._items_per_bundle:
                # This indicates that item is larger than all elements in the bundle.
                continue
            if frozen_bundle[index] == item:
                return True
        return False

    def __len__(self) -> int:
        """The number of elments in this set."""
        return (
            len(self._current_bundle)
            + len(self._frozen_bundles) * self._items_per_bundle
        )

    def add(self, item: int):
        """Adds an element to this set."""
        self._current_bundle.add(item)
        if len(self._current_bundle) == self._items_per_bundle:
            bundle_filename = f"{self._data_dir}/{len(self._frozen_bundles):05d}.dat"
            print(f"Adding a new bundle: {bundle_filename}")
            bundle = np.memmap(
                bundle_filename,
                dtype=np.int_,
                mode="w+",
                shape=self._items_per_bundle,
            )

            # Isert sorted data into the bundle.
            bundle[:] = np.fromiter(self._current_bundle, dtype=np.int_)
            np.ndarray.sort(bundle)

            # Clean up memory
            bundle.flush()
            self._current_bundle.clear()

            # Remember this new frozen_bundle
            self._frozen_bundles.append(bundle)

    @staticmethod
    def test():
        """Test case for this class."""
        print("Testing...")
        int_set = IntSet(items_per_bundle=10)
        even_ints = list(range(0, 1000, 2))
        random.shuffle(even_ints)
        for x in even_ints:
            int_set.add(x)
        for x in range(1000):
            if x % 2 == 0:
                assert x in int_set, f"{x} should be in int_set"
            else:
                assert x not in int_set, f"{x} shouldn't be in int_set"
        print("Test passed.")


class GiantQueue:
    """This class implements append() and pop() for a giant number of pickleable python
    types. The output order of pop() is not guaranteed."""

    def __init__(self, items_per_bundle: int = 10):
        """
        Constucts a new IntSet.

        Parameters
        ----------
        items_per_bundle: int - the number of ints we store in each mem-mapped array
        """
        self._current_bundle: List = []
        self._frozen_bundle_filenames: List[str] = []
        self._items_per_frozen_bundle = items_per_bundle
        self._max_current_bundle_items = self._items_per_frozen_bundle * 2
        self._data_dir: str = "./queue"

        # Create a fresh data directory
        os.system(f'rm -rf "{self._data_dir}" && mkdir -v "{self._data_dir}"')

    def __len__(self) -> int:
        """Returns the number of elements in this queue."""
        return (
            len(self._current_bundle)
            + len(self._frozen_bundle_filenames) * self._items_per_frozen_bundle
        )

    def append(self, item):
        """Appends a new item to the queue."""
        self._current_bundle.append(item)
        if len(self._current_bundle) >= self._max_current_bundle_items:
            assert len(self._current_bundle) == self._max_current_bundle_items
            num_files = len(self._frozen_bundle_filenames)
            bundle_filename = f"{self._data_dir}/{num_files:05d}.dat"
            print(f"Adding a new bundle: {bundle_filename}")
            with open(bundle_filename, "wb") as file_handle:
                pickle.dump(
                    self._current_bundle[: self._items_per_frozen_bundle], file_handle
                )
            self._current_bundle = self._current_bundle[self._items_per_frozen_bundle :]
            self._frozen_bundle_filenames.append(bundle_filename)

    def pop(self):
        """Pops a new item to the queue."""
        if self._current_bundle:
            return self._current_bundle.pop()
        elif self._frozen_bundle_filenames:
            bundle_filename = self._frozen_bundle_filenames.pop()
            with open(bundle_filename, "rb") as file_handle:
                self._current_bundle = pickle.load(file_handle)  # type: ignore
            os.system(f"rm {bundle_filename}")
            return self._current_bundle.pop()
        else:
            raise IndexError("pop from empty GiantQueue")

    @staticmethod
    def test():
        """Runs a test on giant queue."""
        print("Testing...")
        giant_queue = GiantQueue(items_per_bundle=10)
        even_ints = set(range(0, 1000, 2))
        dequeued = set()
        for x in even_ints:
            giant_queue.append(x)
        while len(giant_queue) * 2 >= len(even_ints):
            dequeued.add(giant_queue.pop())
        assert dequeued != even_ints, "Sets shouldn't be equal."
        for x in list(even_ints - dequeued):
            giant_queue.append(x)
        while giant_queue:
            dequeued.add(giant_queue.pop())
        assert dequeued == even_ints, "Sets should be equal."
        print("All tests pass.")


if __name__ == "__main__":
    # IntSet.test()
    GiantQueue.test()

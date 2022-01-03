"""A set of out-of-core data structures so that I can search larger boards."""

import os
from typing import List
import numpy as np
import random


class IntSet:
    """This class implements add-only, set-like semantics for a large number of Python
    ints."""

    def __init__(self, items_per_bundle: int = 10):
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

        # print(f"{10:05d}")
        # raise NotImplementedError("constructor")

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
                print("Found", item, "in", frozen_bundle, "at", index)
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
                shape=(self._items_per_bundle),
            )

            # print(list(bundle[:]))
            # temp_array = np.array(self._current_bundle, np.int_)
            # print(temp_array.dtype)

            bundle[:] = np.fromiter(self._current_bundle, dtype=np.int_)

            # print(list(self._current_bundle))
            # print(list(bundle[:]))

            np.ndarray.sort(bundle)

            # print(list(sorted(self._current_bundle)))
            # print(list(bundle[:]))

            bundle.flush()
            self._current_bundle.clear()

            # print("flushed bundle")
            # print(list(self._current_bundle))
            # the_hash = hash("hello")
            # print(the_hash, type(the_hash))
            # print(bundle_filename)

            self._frozen_bundles.append(bundle)

            # print(list(sorted(self._current_bundle)))
            # print(list(self._frozen_bundles[-1]))

            print(f"There are now {len(self._frozen_bundles)} frozen bundles.")

            # # print(list(self._current_bundle))
            # # the_hash = hash("hello")
            # # print(the_hash, type(the_hash))
            # # print(bundle_filename)

            # raise NotImplementedError("add")

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


if __name__ == "__main__":
    IntSet.test()

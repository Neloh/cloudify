########################################################################
#
# Class for creating a data-set consisting of all files in a directory.

# Implemented in Python 3.5
#
########################################################################
#
# This file is an extract of the TensorFlow Tutorials available at:
#
# https://github.com/Hvass-Labs/TensorFlow-Tutorials (by Magnus Erik Hvass Pedersen)

# The author of this file is Sibonelo Ngobese
# Data Science Intern at Bytes Systems Integration, Gauteng, Midrand 
########################################################################

import numpy as np
import os
import shutil
from cache import cache

########################################################################


def one_hot_encoded(class_numbers, num_classes=None):
    """
    Generate the One-Hot encoded class-labels from an array of integers.

    For example, if class_number=2 and num_classes=4 then
    the one-hot encoded label is the float array: [0. 0. 1. 0.]

    :param class_numbers:
        Array of integers with class-numbers.
        Assume the integers are from zero to num_classes-1 inclusive.

    :param num_classes:
        Number of classes. If None then use max(class_numbers)+1.

    :return:
        2-dim array of shape: [len(class_numbers), num_classes]
    """

    # Find the number of classes if None is provided.
    # Assumes the lowest class-number is zero.
    if num_classes is None:
        num_classes = np.max(class_numbers) + 1

    return np.eye(num_classes, dtype=float)[class_numbers]


########################################################################


class DataSet:
    def __init__(self, in_dir, exts='.jpg'):
        """
        Create a data-set consisting of the filenames in the given directory
        and sub-dirs that match the given filename-extensions.

        For example, the clouds data-set (see cloudy.py) has the
        following dir-structure:

        clouds-images/cirrus/
        clouds-images/cumulus/
        clouds-images/nimbus/
        clouds-images/stratus/
        
        clouds-images/cirrus/test/
        clouds-images/cumulus/test/
        clouds-images/nimbus/test/
        clouds-images/stratus/test/

        This means there are 4 classes called: cirrus, cumulus, nimbus and stratus.

        If we set in_dir = "clouds-images/" and create a new DataSet-object
        then it will scan through these directories and create a training-set
        and test-set for each of these classes.

        The training-set will contain a list of all the *.jpg filenames
        in the following directories:

        clouds-images/cirrus/
        clouds-images/cumulus/
        clouds-images/nimbus/
        clouds-images/stratus/

        The test-set will contain a list of all the *.jpg filenames
        in the following directories:

        clouds-images/cirrus/test/
        clouds-images/cumulus/test/
        clouds-images/nimbus/test/
        clouds-images/stratus/test/


        :param in_dir:
            Root-dir for the files in the data-set.
            This would be 'clouds-images/' in the example above.

        :param exts:
            String or tuple of strings with valid filename-extensions.
            Not case-sensitive.

        :return:
            Object instance.
        """

        # Extend the input directory to the full path.
        in_dir = os.path.abspath(in_dir)

        # Input directory.
        self.in_dir = in_dir

        # Convert all file-extensions to lower-case.
        self.exts = tuple(ext.lower() for ext in exts)

        # Names for the classes.
        self.class_names = []

        # Filenames for all the files in the training-set.
        self.filenames = []

        # Filenames for all the files in the test-set.
        self.filenames_test = []

        # Class-number for each file in the training-set.
        self.class_numbers = []

        # Class-number for each file in the test-set.
        self.class_numbers_test = []

        # Total number of classes in the data-set.
        self.num_classes = 0

        # For all files/dirs in the input directory.
        for name in os.listdir(in_dir):
            # Full path for the file / dir.
            current_dir = os.path.join(in_dir, name)

            # If it is a directory.
            if os.path.isdir(current_dir):
                # Add the dir-name to the list of class-names.
                self.class_names.append(name)

                # Training-set.

                # Get all the valid filenames in the dir (not sub-dirs).
                filenames = self._get_filenames(current_dir)

                # Append them to the list of all filenames for the training-set.
                self.filenames.extend(filenames)

                # The class-number for this class.
                class_number = self.num_classes

                # Create an array of class-numbers.
                class_numbers = [class_number] * len(filenames)

                # Append them to the list of all class-numbers for the training-set.
                self.class_numbers.extend(class_numbers)

                # Test-set.

                # Get all the valid filenames in the sub-dir named 'test'.
                filenames_test = self._get_filenames(os.path.join(current_dir, 'test'))

                # Append them to the list of all filenames for the test-set.
                self.filenames_test.extend(filenames_test)

                # Create an array of class-numbers.
                class_numbers = [class_number] * len(filenames_test)

                # Append them to the list of all class-numbers for the test-set.
                self.class_numbers_test.extend(class_numbers)

                # Increase the total number of classes in the data-set.
                self.num_classes += 1

    def _get_filenames(self, dir):
        """
        Create and return a list of filenames with matching extensions in the given directory.

        :param dir:
            Directory to scan for files. Sub-dirs are not scanned.

        :return:
            List of filenames. Only filenames. Does not include the directory.
        """

        # Initialize empty list.
        filenames = []

        # If the directory exists.
        if os.path.exists(dir):
            # Get all the filenames with matching extensions.
            for filename in os.listdir(dir):
                if filename.lower().endswith(self.exts):
                    filenames.append(filename)

        return filenames

    def get_paths(self, test=False):
        """
        Get the full paths for the files in the data-set.

        :param test:
            Boolean. Return the paths for the test-set (True) or training-set (False).

        :return:
            Iterator with strings for the path-names.
        """

        if test:
            # Use the filenames and class-numbers for the test-set.
            filenames = self.filenames_test
            class_numbers = self.class_numbers_test

            # Sub-dir for test-set.
            test_dir = "test/"
        else:
            # Use the filenames and class-numbers for the training-set.
            filenames = self.filenames
            class_numbers = self.class_numbers

            # Don't use a sub-dir for test-set.
            test_dir = ""

        for filename, cls in zip(filenames, class_numbers):
            # Full path-name for the file.
            path = os.path.join(self.in_dir, self.class_names[cls], test_dir, filename)

            yield path

    def get_training_set(self):
        """
        Return the list of paths for the files in the training-set,
        and the list of class-numbers as integers,
        and the class-numbers as one-hot encoded arrays.
        """

        return list(self.get_paths()), \
               np.asarray(self.class_numbers), \
               one_hot_encoded(class_numbers=self.class_numbers,
                               num_classes=self.num_classes)

    def get_test_set(self):
        """
        Return the list of paths for the files in the test-set,
        and the list of class-numbers as integers,
        and the class-numbers as one-hot encoded arrays.
        """

        return list(self.get_paths(test=True)), \
               np.asarray(self.class_numbers_test), \
               one_hot_encoded(class_numbers=self.class_numbers_test,
                               num_classes=self.num_classes)

    def copy_files(self, train_dir, test_dir):
        """
        Copy all the files in the training-set to train_dir
        and copy all the files in the test-set to test_dir.

        For example, the normal directory structure for the
        different classes in the training-set is:

        clouds-images/cirrus/
        clouds-images/cumulus/
        clouds-images/nimbus/
        clouds-images/stratus/

        Normally the test-set is a sub-dir of the training-set:

        clouds-images/cirrus/test/
        clouds-images/cumulus/test/
        clouds-images/nimbus/test/
        clouds-images/stratus/test/

        But some APIs use another dir-structure for the training-set:
        
        clouds-images/train/cirrus/
        clouds-images/train/cumulus/
        clouds-images/train/nimbus/
        clouds-images/train/stratus/

        and for the test-set:
        
        clouds-images/test/cirrus/
        clouds-images/test/cumulus/
        clouds-images/test/nimbus/
        clouds-images/test/stratus/

        :param train_dir: Directory for the training-set e.g. 'clouds-images/train/'
        :param test_dir: Directory for the test-set e.g. 'clouds-images/test/'
        :return: Nothing. 
        """

        # Helper-function for actually copying the files.
        def _copy_files(src_paths, dst_dir, class_numbers):

            # Create a list of dirs for each class:
            class_dirs = [os.path.join(dst_dir, class_name + "/")
                          for class_name in self.class_names]

            # Check if each class-directory exists, otherwise create it.
            for dir in class_dirs:
                if not os.path.exists(dir):
                    os.makedirs(dir)

            # For all the file-paths and associated class-numbers,
            # copy the file to the destination dir for that class.
            for src, cls in zip(src_paths, class_numbers):
                shutil.copy(src=src, dst=class_dirs[cls])

        # Copy the files for the training-set.
        _copy_files(src_paths=self.get_paths(test=False),
                    dst_dir=train_dir,
                    class_numbers=self.class_numbers)

        print("- Copied training-set to:", train_dir)

        # Copy the files for the test-set.
        _copy_files(src_paths=self.get_paths(test=True),
                    dst_dir=test_dir,
                    class_numbers=self.class_numbers_test)

        print("- Copied test-set to:", test_dir)


########################################################################


def load_cached(cache_path, in_dir):
    """
    Wrapper-function for creating a DataSet-object, which will be
    loaded from a cache-file if it already exists, otherwise a new
    object will be created and saved to the cache-file.

    This is useful if you need to ensure the ordering of the
    filenames is consistent every time you load the data-set,
    for example if you use the DataSet-object in combination
    with Transfer Values saved to another cache-file.

    :param cache_path:
        File-path for the cache-file.

    :param in_dir:
        Root-dir for the files in the data-set.
        This is an argument for the DataSet-init function.

    :return:
        The DataSet-object.
    """

    print("Creating dataset from the files in: " + in_dir)

    # If the object-instance for DataSet(in_dir=data_dir) already
    # exists in the cache-file then reload it, otherwise create
    # an object instance and save it to the cache-file for next time.
    dataset = cache(cache_path=cache_path,
                    fn=DataSet, in_dir=in_dir)

    return dataset


########################################################################

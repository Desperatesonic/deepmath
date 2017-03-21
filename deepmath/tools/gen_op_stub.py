# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Generate a stub Python file which calls tf.load_op_library."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys


def main():
  script, name = sys.argv
  print('''\
# Autogenerated by %s.  DO NOT EDIT!
import os
import tensorflow as tf
lib = tf.load_op_library(
    os.path.join(tf.resource_loader.get_data_files_path(), '%s.so'))
globals().update(lib.__dict__)
''' % (script, name))


if __name__ == '__main__':
  main()
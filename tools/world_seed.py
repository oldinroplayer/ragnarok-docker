#!/usr/bin/env python3

import hashlib
import sys

mnemonic = sys.argv[1]

h = hashlib.sha256(mnemonic.encode()).hexdigest()

seed = int(h[:16],16)

print(seed)

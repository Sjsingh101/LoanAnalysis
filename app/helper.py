from collections import Counter
import numpy as np


def gen_dist(ages):
    gen = []
    for age in ages:
        if age in np.arange(9,25,1):
            gen.append("Gen Z")
        elif age in np.arange(25,41,1):
            gen.append("Millennials")
        elif age in np.arange(41,57,1):
            gen.append("Gen X")
        elif age in np.arange(57,67,1):
            gen.append("Boomers II")
    return gen
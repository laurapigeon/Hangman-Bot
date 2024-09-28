"prints every pair of bubs"

import copy
bubsList = ["sheepy", "poly", "platy",
            "meepy", "roly", "splaty",
            "tipi", "boly", "ratty",
            "beepy", "moly", "raratty", "ratsy",
            "geepy", "woly", "naty"]

for bub1 in bubsList[::-1]:
    newBubsList = copy.copy(bubsList)
    newBubsList.remove(bub1)

    for bub2 in newBubsList:
        print(bub1, bub2)

    bubsList.remove(bub1)

class game:

    # added as roster_db document items
    golfers = []

    def __init__(self, p_golfers):
        self.golfers = p_golfers

    def __str__(self):
        r = ''
        for g in self.golfers:
            r += g['name'] + '\t'
        return r

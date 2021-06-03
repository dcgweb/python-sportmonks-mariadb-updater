import constants, os
from pathlib import Path

class Iterator:
    def __init__(self):
        self.iteration = self.get_iterator()

    def get_iterator(self):
        # Check if iter.txt exist
        if(os.path.exists(Path(constants.ITER_TXT_FILE))):
            with open(Path(constants.ITER_TXT_FILE)) as iter_file:
                line = iter_file.readline()
                if(line == ""):
                    self.set_iterator(constants.BASE_ITERATION)
                    self.iteration = constants.BASE_ITERATION
                else:
                    # file is not empty, read contents
                    self.iteration = int(line)
        return self.iteration


    def set_iterator(self, iteration = None):
        if iteration == None: return False

        with open(Path(constants.ITER_TXT_FILE), 'w') as iter_file:
            iter_file.write(str(iteration))
            self.iteration = int(iteration)
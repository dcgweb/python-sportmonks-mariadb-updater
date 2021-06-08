import constants, os
from pathlib import Path

class Iterator:
    def __init__(self):
        self.iteration = self.get_iterator()
        self.iter_file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.logger.error(f'Suppressing exception: {exc_type}')
            self.logger.error(f'Traceback: {exc_tb}')
        return True


    def get_iterator(self):
        # Check if iter.txt exist
        if(os.path.exists(Path(constants.ITER_TXT_FILE))):
            with open(Path(constants.ITER_TXT_FILE)) as self.iter_file:
                line = self.iter_file.readline()
                if(line == ""):
                    self.set_iterator(constants.BASE_ITERATION)
                    self.iteration = constants.BASE_ITERATION
                else:
                    # file is not empty, read contents
                    self.iteration = int(line)
                self.iter_file.close()
        return self.iteration


    def set_iterator(self, iteration = None):
        if iteration == None: return False

        with open(Path(constants.ITER_TXT_FILE), 'w') as self.iter_file:
            self.iter_file.write(str(iteration))
            self.iteration = int(iteration)
            self.iter_file.close()
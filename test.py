import games.meteorito.Meteoritos as s

import unittest

class testColision(unittest.TestCase):

    def testMeteorito(self):
        print(s.Meteoritos.colision(2, -2, 0, 2, ))


if __name__ == '__main__':
    unittest.main()

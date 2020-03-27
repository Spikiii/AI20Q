import time
import unittest
from io import StringIO
from unittest.mock import patch
from unittest import TestCase
import game
import random as Rd


class Test(unittest.TestCase):
    #Done with help from https://andressa.dev/2019-07-20-using-pach-to-test-inputs/

    inputs = ['invalid_input', 0, 'd', 'g', 'invalid_input', 0, "a"] + Rd.choices(["y", "n"], [1, 1], k = 20)

    @patch('builtins.input', side_effect = inputs)
    def test_play_game(self, mock_inputs):
        guess = game.playGame()
        self.assertEqual(guess, "Tomato") #Fails unless it guesses a Tomato

if __name__ == '__main__':
    unittest.main()
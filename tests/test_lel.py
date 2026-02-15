import unittest
import io
import sys
import os
from contextlib import redirect_stdout

# Add the /src/ directory to the path so we can find the interpreter
# Since test_interpreter.py is in /tests/, we go up one level and then into /src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from interpreter import LiterallyEveryLang

class TestLiterallyEveryLang(unittest.TestCase):
    def setUp(self):
        self.interpreter = LiterallyEveryLang()

    def test_incentivise_and_cctb(self):
        """Test if we can set assets and print them."""
        code = """
        inc bonus = 5000
        cctb bonus
        """
        f = io.StringIO()
        with redirect_stdout(f):
            self.interpreter.run(code)
        output = f.getvalue()
        self.assertIn("[BOARD_MEMO]: 5000", output)

    def test_calculate_sales(self):
        """Test the 'cs' math operation."""
        code = """
        inc revenue = 100 cs 250
        cctb revenue
        """
        f = io.StringIO()
        with redirect_stdout(f):
            self.interpreter.run(code)
        output = f.getvalue()
        self.assertIn("[BOARD_MEMO]: 350", output)

    def test_pivot_on_kpi_true(self):
        """Test if 'pok' executes when condition is met."""
        code = """
        inc sales = 100
        pok (sales > 50) { cctb "Target Met" }
        """
        f = io.StringIO()
        with redirect_stdout(f):
            self.interpreter.run(code)
        output = f.getvalue()
        self.assertIn("[BOARD_MEMO]: Target Met", output)

    def test_pivot_on_kpi_false(self):
        """Test if 'pok' skips when condition is not met."""
        code = """
        inc sales = 10
        pok (sales > 50) { cctb "Target Met" }
        """
        f = io.StringIO()
        with redirect_stdout(f):
            self.interpreter.run(code)
        output = f.getvalue()
        self.assertNotIn("Target Met", output)

    def test_light_building_on_fire(self):
        """Test if 'ltbof' terminates the session."""
        code = """
        ltbof
        inc after_fire = 1
        cctb after_fire
        """
        f = io.StringIO()
        with redirect_stdout(f):
            self.interpreter.run(code)
        output = f.getvalue()
        self.assertIn("Building is on fire", output)
        self.assertNotIn("[BOARD_MEMO]: 1", output)

    def test_synergy_coercion(self):
        """Test the 'JS-style' loose typing/synergy blobs."""
        # Trying to do math with an undefined variable/bad string
        code = """
        inc mess = unknown_asset cs 10
        cctb mess
        """
        f = io.StringIO()
        with redirect_stdout(f):
            self.interpreter.run(code)
        output = f.getvalue()
        self.assertIn("SYNERGY_BLOB", output)

if __name__ == "__main__":
    unittest.main()

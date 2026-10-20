import unittest

from bot.risk import RiskConfig, position_notional
from bot.simulator import run_simulation, synthetic_bars
from bot.strategy import Bar, crossover_signal, rsi, sma


class StrategyTests(unittest.TestCase):
    def test_sma(self):
        self.assertEqual(sma([1, 2, 3], 2), 2.5)
        self.assertIsNone(sma([1], 2))

    def test_rsi_flat(self):
        self.assertEqual(rsi([4.0] * 16, 14), 50.0)

    def test_no_early_signal(self):
        self.assertEqual(crossover_signal([Bar(i, 1.0) for i in range(10)]), 0)


class RiskTests(unittest.TestCase):
    def test_notional_is_capped(self):
        cfg = RiskConfig()
        self.assertLessEqual(position_notional(1000, 100, cfg), 250)

    def test_rejects_leverage(self):
        with self.assertRaises(ValueError):
            position_notional(1000, 100, RiskConfig(max_leverage=2))


class SimulationTests(unittest.TestCase):
    def test_deterministic_and_discloses_synthetic_data(self):
        bars1, bars2 = synthetic_bars(250, 11), synthetic_bars(250, 11)
        t1, r1 = run_simulation(bars1)
        t2, r2 = run_simulation(bars2)
        self.assertEqual(t1, t2)
        self.assertEqual(r1, r2)
        self.assertIn("synthetic", r1["data_source"])

    def test_invalid_bar_count(self):
        with self.assertRaises(ValueError):
            synthetic_bars(0)


if __name__ == "__main__":
    unittest.main()

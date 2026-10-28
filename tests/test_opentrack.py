import unittest
from dataclasses import FrozenInstanceError

from opentrack import Market, RaceSnapshot, Runner, Selection, hypothetical_return


class OpenTrackTests(unittest.TestCase):
    def test_snapshot_preserves_source_identity_without_claiming_discipline(self):
        runner = Runner("runner-1", "Synthetic Runner", 1, 3, None, None, None, None, None)
        selection = Selection("outcome-1", "runner-1", "native-disabled", "3.50", "3.50", "1", None, None, None)
        market = Market("native-market", "native-group", "win", None, "9007199254740993", (selection,))
        race = RaceSnapshot(
            source="synthetic", source_id="race-1", name="Synthetic race", meeting=None,
            country=None, scheduled_at=None, cutoff_at=None, observed_at="2026-10-28T00:00:00Z",
            source_status="native-status", discipline=None, runners=(runner,),
            markets=(market,), warnings=("Synthetic fixture only",),
        )
        data = race.to_dict()
        self.assertIsNone(data["discipline"])
        self.assertEqual(data["markets"][0]["sequence"], "9007199254740993")
        self.assertEqual(data["markets"][0]["selections"][0]["decimal_odds"], "3.50")
        self.assertEqual(data["markets"][0]["selections"][0]["source_status"], "native-disabled")
        with self.assertRaises(FrozenInstanceError):
            runner.name = "Changed"

    def test_hypothetical_return(self):
        self.assertEqual(hypothetical_return("10", "3.5"), "35.00")
        self.assertEqual(hypothetical_return("0.10", "1.10"), "0.11")

    def test_invalid_preview_inputs(self):
        for stake, odds in [("NaN", "2"), ("10", "Infinity"), ("0", "2"),
                            ("-1", "2"), ("10", "1"), ("invalid", "2"),
                            ("1000001", "2"), ("10", "1000001")]:
            with self.subTest(stake=stake, odds=odds), self.assertRaises(ValueError):
                hypothetical_return(stake, odds)


if __name__ == "__main__":
    unittest.main()

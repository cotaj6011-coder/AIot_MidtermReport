import unittest
from unittest.mock import patch

from src.connectors import JsonApiConnector
from src.prediction import PersistenceBaseline


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return b'{"records":[{"id":"A"}]}'


class ConnectorBaselineTests(unittest.TestCase):
    @patch("src.connectors.http_json.urlopen", return_value=FakeResponse())
    def test_json_connector_parses_response(self, mocked_open):
        result = JsonApiConnector("https://example.invalid/api", timeout=2).fetch()
        self.assertEqual(result["records"][0]["id"], "A")
        self.assertEqual(mocked_open.call_args.kwargs["timeout"], 2)

    def test_persistence_is_capacity_bounded(self):
        result = PersistenceBaseline().predict({"facility_id": "A", "available_spaces": 12, "total_spaces": 10}, 30)
        self.assertEqual(result["available_spaces"], 10)
        self.assertEqual(result["model"], "persistence")


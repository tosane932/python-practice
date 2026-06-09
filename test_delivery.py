import unittest
from delivery import calculate_delivery_time

class TestDelivery(unittest.TestCase):
    def test_calculate_delivery_time(self):
        # 正常なケース
        self.assertEqual(calculate_delivery_time(4.0, 8.0), 4.0)
        # エラーになるケースをチェック
        with self.assertRaises(ValueError):
            calculate_delivery_time("4時", 8.0)

if __name__ == '__main__':
    unittest.main()
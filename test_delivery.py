# test_delivery.py
import unittest
from delivery import calculate_delivery_time

class TestDelivery(unittest.TestCase):
    # 正常なケース
    def test_normal_calculation(self):
        self.assertEqual(calculate_delivery_time(4.0, 8.0), 4.0)

    # エラーが出るべきケース
    def test_invalid_time_order(self):
        # 終了時間が開始時間より早いとエラーになるか確認
        with self.assertRaises(ValueError):
            calculate_delivery_time(8.0, 4.0)

if __name__ == '__main__':
    unittest.main()
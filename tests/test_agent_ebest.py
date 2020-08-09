import unittest
from stocklab.agent.ebest import EBest
import inspect
import time


class TestEBest(unittest.TestCase):
    def setUp(self):
        self.ebest = EBest("DEMO")
        self.ebest.login()

    def tearDown(self):
        self.ebest.logout()

    def test_get_code_list(self):
        print(inspect.stack()[0][3])
        all_result = self.ebest.get_code_list("ALL")
        assert all_result is not None
        kosdaq_result = self.ebest.get_code_list("KOSDAQ")
        assert kosdaq_result is not None
        kospi_result = self.ebest.get_code_list("KOSPI")
        assert kospi_result is not None
        try:
            error_result = self.ebest.get_code_list("KOS")
        except:
            error_result = None
        assert error_result is None
        print("result:", len(all_result), len(kosdaq_result), len(kospi_result))

    def test_get_stock_price_list_by_code(self):
        print("=========삼성전자 최근 2일치 데이터 조회=========")
        print(inspect.stack()[0][3])
        # 005930 삼성전자 최근 2일치 데이터 조회
        result = self.ebest.get_stock_price_by_code("005930", "2")
        assert result is not None
        print(result)


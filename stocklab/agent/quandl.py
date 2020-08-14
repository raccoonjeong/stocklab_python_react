import quandl

quandl.ApiConfig.api_key = 'bla_bla'
data = quandl.get('BCHARTS/BITFLYERUSD', start_date='2019-03-07', end_date='2019-03-07')

print(data)
# 데이터 마켓을 이용하는 방법도 있다.. 패스...


from datetime import date
from windtrend.core import run
from windtrend.schema import TrendRequest

if __name__ == "__main__":
    req = TrendRequest(
        lat=48.43,
        lon=-123.37,
        start_date=date(2015, 1, 1),
        end_date=date(2024, 12, 31),
    )
    print(run(req).model_dump())

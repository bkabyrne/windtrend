from windtrend.core import run
from windtrend.schema import TrendRequest

def handler(event, context):
    req = TrendRequest(**event)
    return run(req).model_dump()

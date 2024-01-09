def hello(event, context):
    try:
        print(event)
        print(context)
        param = event.body.detailParams
        name = param.name.value
        number = param.number.value
        return {
        "version":"2.0",
        "template":
            {"outputs":[{"simpleText":{"text":"hello I'm "+name +": "+number}}]}
        }
    except:
        return {
        "version":"2.0",
        "template":
            {"outputs":[{"simpleText":{"text":"오류가 발생했습니다."}}]}
        }       


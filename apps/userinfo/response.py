from django.http import JsonResponse


class Response:

    def base(self, values=None, message="", status=200, success='True'):
        if values is None:
            values = []

        return JsonResponse({
            'success': success,
            'values': values,
            'message': message
        }, status=status)

    def getMultipleBase(self, values=None, message="", status=200, success='True', count=0):
        if values is None:
            values = []

        return JsonResponse({
            'success': success,
            'values': values,
            'message': message,
            'count': count
        }, status=status)

    @staticmethod
    def ok(values=None, message="", success=True):
        return Response().base(success=True, values=values, message=message, status=200)

    @staticmethod
    def badRequest(values=None, message="", success=False):
        return Response().base(success=success, values=values, message=message, status=400)

    @staticmethod
    def okReturnCount(values=None, message="", success=True, count=0):
        return Response().getMultipleBase(success=True, values=values, message=message, status=200, count=count)

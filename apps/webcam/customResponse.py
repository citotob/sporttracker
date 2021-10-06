from rest_framework.response import Response
from rest_framework import status as HTTPStatus


class CustomResponse:

    def base(self, values=None, message="", status=200, success='True'):
        try:
            if values is None:
                values = []

            res = {}

            res['success'] = success

            if isinstance(values, list) and len(values) > 0:
                res['count'] = len(values)

            res['values'] = values

            if message != '':
                res['message'] = message
            return Response(res, status=status)
        except Exception as e:
            print(e)

    @staticmethod
    def ok(values=None, message="", success=True):
        return CustomResponse().base(success=True, values=values, message=message, status=200)

    @staticmethod
    def badRequest(values=None, message="", success=False):
        return CustomResponse().base(success=success, values=values, message=message, status=400)

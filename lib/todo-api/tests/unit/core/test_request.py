import unittest
import json

from src.core.request import Request


class TestRequest(unittest.TestCase):
    emptyEvent = json.loads("{}")

    eventNoIdentityId = json.loads(
        """{
           "body":null,
           "resource":"/v1/users/current",
           "requestContext":{
              "resourceId":"87p5cd",
              "apiId":"t2ioikuoyh",
              "resourcePath":"/v1/users/current",
              "httpMethod":"GET",
              "requestId":"d2267aea-ad1e-11e6-abe7-2da452458d80",
              "accountId":"390572732222",
              "identity":{
                "apiKey": null,
                "userArn": null,
                "cognitoAuthenticationType": null,
                "accessKey": null,
                "caller": null,
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
                "user": null,
                "cognitoIdentityPoolId": null,
                "cognitoIdentityId": null,
                "cognitoAuthenticationProvider": null,
                "sourceIp": "1.2.3.4",
                "accountId": null
              },
              "stage":"DefaultStage"
           },
           "queryStringParameters":{
              "filter":"",
              "start":"",
              "end":"",
              "properties":""
           },
           "httpMethod":"GET",
           "pathParameters":null,
           "headers":{},
           "stageVariables":null,
           "path":"/v1/users/current",
           "isBase64Encoded":false
        }"""
    )
    eventGuest = json.loads(
        """{
           "body":null,
           "resource":"/v1/users/current",
           "requestContext":{
              "resourceId":"87p5cd",
              "apiId":"t2ioikuoyh",
              "resourcePath":"/bookings",
              "httpMethod":"GET",
              "requestId":"d2267aea-ad1e-11e6-abe7-2da452458d80",
              "accountId":"xxxxxxxxxxxxxx",
              "identity":{
                 "apiKey":null,
                 "userArn":"arn:aws:sts::xxxxxxxxxxx:assumed-role/cognito-pcp-idpool/CognitoIdentityCredentials",
                 "cognitoAuthenticationType":"unauthenticated",
                 "accessKey":"ASIAISXOPTPOOVO4OS3Q",
                 "caller":"AROAJGNYQMFDUYIVMQ5JC:CognitoIdentityCredentials",
                 "userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                 "user":"AROAJGNYQMFDUYIVMQ5JC:CognitoIdentityCredentials",
                 "cognitoIdentityPoolId":"eu-west-1:2906e022-b49e-412c-8763-3ef3f4bea1b7",
                 "cognitoIdentityId":"eu-west-1:b449e9f7-b883-43a1-9ff4-ee2c80567789",
                 "cognitoAuthenticationProvider":null,
                 "sourceIp":"1.2.3.4",
                 "accountId":"xxxxxxxxxxxxxx"
              },
              "stage":"DefaultStage"
           },
           "queryStringParameters":{
              "filter":"",
              "start":"",
              "end":"",
              "properties":""
           },
           "httpMethod":"GET",
           "pathParameters":null,
           "headers":{
              "Origin":"http://localhost:8000",
              "Via":"1.1 b8e590a2ef13316d12372907731333d5.cloudfront.net (CloudFront)",
              "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
              "Accept-Encoding":"gzip, deflate, sdch, br",
              "CloudFront-Is-SmartTV-Viewer":"false",
              "CloudFront-Forwarded-Proto":"https",
              "X-Forwarded-For":"1.2.3.4, 54.239.202.5",
              "CloudFront-Viewer-Country":"AU",
              "Accept":"application/json",
              "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
              "Host":"api.alpha.airbus.cloud",
              "X-Forwarded-Proto":"https",
              "Referer":"http://localhost:8000/",
              "CloudFront-Is-Tablet-Viewer":"false",
              "X-Forwarded-Port":"443",
              "X-Amz-Cf-Id":"Ksg5jjeUheEu_M-orKHDAKfhpuY3SMTDMCnWREHzdLavFUFDRfWvFA==",
              "x-amz-security-token":"AgoGb3JpZ2luEBsaDmFwLW5vcnRoZWFzdC0xIoACOnvyPsSLTqGjTpu2cqjcSMZCKRSEoR6YvCINCRbRKFjLiHPCiQSO5QW6Df1V7j4FK7gJQrTRXJFVzkVYSuCh2NOP5z3xyoahUucFlecb+uVfbgZXgo7tDxwUjGA4hmFfo7ur1KmkeeZnmTLmAUaJyGg04n5Cmu3cv5Iy/UnETXzajjzGCLRCjNYTKzVV/iFD+Xcfi2mZEcXZ4kXUu7J/3IG99/Q8+RGzdHxkc6WdWrmcOaQboT+kYTpN4dKEm8Q5rkuOloY4lRHweE7waYewIZbSpJro56ARyX1Zse6mToZUAx6kBb1wL/yAf37bFH/THb7Ip8Da9GH",
              "CloudFront-Is-Mobile-Viewer":"false",
              "X-AMZ-Date":"20161117T233736Z",
              "CloudFront-Is-Desktop-Viewer":"true"
           },
           "stageVariables":null,
           "path":"/v1/users/current",
           "isBase64Encoded":false
        }"""
    )
    event = json.loads(
        """{
           "body":null,
           "resource":"/v1/users/current",
           "requestContext":{
              "resourceId":"n3n0wp",
              "apiId":"f91si1mjkd",
              "resourcePath":"/v1/users/current",
              "httpMethod":"GET",
              "requestId":"f7c55844-a579-11e6-9085-25b78f31d72e",
              "accountId":"xxxxxxxxxxxx",
              "identity":{
                 "apiKey":null,
                 "userArn":"arn:aws:sts::xxxxxxxxxxx:assumed-role/cognito-pcp-idpool/CognitoIdentityCredentials",
                 "cognitoAuthenticationType":"authenticated",
                 "accessKey":"ASIAIRWQI32RSH5XWOGA",
                 "caller":"AROAJHA2AZVWSTYA2OI2Q:CognitoIdentityCredentials",
                 "userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                 "user":"AROAJHA2AZVWSTYA2OI2Q:CognitoIdentityCredentials",
                 "cognitoIdentityPoolId":"eu-west-1:2906e022-b49e-412c-8763-3ef3f4bea1b7",
                 "cognitoIdentityId":"eu-west-1:080d6d23-9cce-4f90-8070-9ce872cf4ab8",
                 "cognitoAuthenticationProvider":"cognito-idp.eu-west-1.amazonaws.com/eu-west-1_p4Yt34xeG,cognito-idp.eu-west-1.amazonaws.com/eu-west-1_p4Yt34xeG:CognitoSignIn:6956356d-7a59-4954-9901-73997745cb03",
                 "sourceIp":"1.2.3.4",
                 "accountId":"xxxxxxxxxxxxx"
              },
              "stage":"DefaultStage"
           },
           "queryStringParameters":{
              "filter":"",
              "start":"",
              "end":"",
              "properties":""
           },
           "httpMethod":"GET",
           "pathParameters":null,
           "headers":{
              "Origin":"http://localhost:8000",
              "Via":"1.1 d4dbc6987ddd22a023698236d3f09b02.cloudfront.net (CloudFront)",
              "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
              "Accept-Encoding":"gzip, deflate, sdch, br",
              "CloudFront-Is-SmartTV-Viewer":"false",
              "CloudFront-Forwarded-Proto":"https",
              "X-Forwarded-For":"1.2.3.4, 54.240.152.117",
              "CloudFront-Viewer-Country":"AU",
              "Accept":"application/json",
              "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
              "Host":"xxxxxxxxxx.execute-api.eu-west-1.amazonaws.com",
              "X-Forwarded-Proto":"https",
              "Referer":"http://localhost:8000/",
              "CloudFront-Is-Tablet-Viewer":"false",
              "X-Forwarded-Port":"443",
              "X-Amz-Cf-Id":"kkhv9kXmJzu1Ngn-u-dzpk9ItHl6fAH-i79QVPxREbpW9tWsCJYNdA==",
              "x-amz-security-token":"AgoGb3JpZ2luEDIaDmFwLW5vcnRoZWFzdC0xIoACM0WGcRFoa82CUqmQ5FSh5xrxREXY/m3X3f0TJK63XbRexqkWKElExCCA0X01RdmKkDzfFTILtITNwcfFer6LaDRJ02Nkb2DtisDES2u78y2UP0/Of3owRl0Fkdu/ab5SrOGC/gWpHjnTZnWQCP6Z/2Zp/BXuX2v0QdJY2XS6w8NRu/xQ/5ofnAIib5IgZwPk6s2vLd36anpbOpLjd1M922WSgFiDJJHIKbqjh4jwzLJQhqvWD9nfEkvmh3VHqzOiJLLM5fx1P5Y79FAv44QbTZ6K0jqh9euWdPJrYiUalGGC887ZE+gJo+1PwQxoWSYJwV6kyJRkmor",
              "CloudFront-Is-Mobile-Viewer":"false",
              "X-AMZ-Date":"20161108T060954Z",
              "CloudFront-Is-Desktop-Viewer":"true"
           },
           "stageVariables":null,
           "path":"/v1/users/current"
        }"""
    )

    eventApplication = json.loads(
        """{
           "body":null,
           "resource":"/v1/users/current",
           "requestContext":{
              "resourceId":"n3n0wp",
              "apiId":"f91si1mjkd",
              "resourcePath":"/v1/users/current",
              "httpMethod":"GET",
              "requestId":"f7c55844-a579-11e6-9085-25b78f31d72e",
              "accountId":"xxxxxxxxxxxx",
              "identity":{
                 "apiKey":null,
                 "userArn":"arn:aws:sts::xxxxxxxxxxx:assumed-role/cognito-pcp-idpool/CognitoIdentityCredentials",
                 "cognitoAuthenticationType":"authenticated",
                 "accessKey":"ASIAIRWQI32RSH5XWOGA",
                 "caller":"AROAJHA2AZVWSTYA2OI2Q:CognitoIdentityCredentials",
                 "userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                 "user":"AROAJHA2AZVWSTYA2OI2Q:CognitoIdentityCredentials",
                 "cognitoIdentityPoolId":"eu-west-1:2906e022-b49e-412c-8763-3ef3f4bea1b7",
                 "cognitoIdentityId":"eu-west-1:080d6d23-9cce-4f90-8070-9ce872cf4ab8",
                 "cognitoAuthenticationProvider":"cognito-idp.eu-west-1.amazonaws.com/eu-west-1_p4Yt34xeG,cognito-idp.eu-west-1.amazonaws.com/eu-west-1_p4Yt34xeG:CognitoSignIn:6956356d-7a59-4954-9901-73997745cb03",
                 "sourceIp":"1.2.3.4",
                 "accountId":"xxxxxxxxxxxxx"
              },
              "stage":"DefaultStage"
           },
           "queryStringParameters":{
              "filter":"",
              "start":"",
              "end":"",
              "properties":""
           },
           "httpMethod":"GET",
           "pathParameters":{
               "aspireCode":"1z21"
           },
           "headers":{
              "Origin":"http://localhost:8000",
              "Via":"1.1 d4dbc6987ddd22a023698236d3f09b02.cloudfront.net (CloudFront)",
              "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
              "Accept-Encoding":"gzip, deflate, sdch, br",
              "CloudFront-Is-SmartTV-Viewer":"false",
              "CloudFront-Forwarded-Proto":"https",
              "X-Forwarded-For":"1.2.3.4, 54.240.152.117",
              "CloudFront-Viewer-Country":"AU",
              "Accept":"application/json",
              "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
              "Host":"xxxxxxxxxx.execute-api.eu-west-1.amazonaws.com",
              "X-Forwarded-Proto":"https",
              "Referer":"http://localhost:8000/",
              "CloudFront-Is-Tablet-Viewer":"false",
              "X-Forwarded-Port":"443",
              "X-Amz-Cf-Id":"kkhv9kXmJzu1Ngn-u-dzpk9ItHl6fAH-i79QVPxREbpW9tWsCJYNdA==",
              "x-amz-security-token":"AgoGb3JpZ2luEDIaDmFwLW5vcnRoZWFzdC0xIoACM0WGcRFoa82CUqmQ5FSh5xrxREXY/m3X3f0TJK63XbRexqkWKElExCCA0X01RdmKkDzfFTILtITNwcfFer6LaDRJ02Nkb2DtisDES2u78y2UP0/Of3owRl0Fkdu/ab5SrOGC/gWpHjnTZnWQCP6Z/2Zp/BXuX2v0QdJY2XS6w8NRu/xQ/5ofnAIib5IgZwPk6s2vLd36anpbOpLjd1M922WSgFiDJJHIKbqjh4jwzLJQhqvWD9nfEkvmh3VHqzOiJLLM5fx1P5Y79FAv44QbTZ6K0jqh9euWdPJrYiUalGGC887ZE+gJo+1PwQxoWSYJwV6kyJRkmor",
              "CloudFront-Is-Mobile-Viewer":"false",
              "X-AMZ-Date":"20161108T060954Z",
              "CloudFront-Is-Desktop-Viewer":"true"
           },
           "stageVariables":null,
           "path":"/v1/users/current"
        }"""
    )

    event_params = json.loads(
        """{
            "body":null,
            "pathParameters":{
                "mandatory1":"foo"
            },
            "queryStringParameters": null
        }"""
    )

    def test_check_params_mandatory_not_empty(self):
        event = json.loads(
            """{
               "body":null,
               "queryStringParameters":{
                  "mandatory1":"",
                  "mandatory2":"bar",
                  "optional1":"baz",
                  "extra1":"quux"
               }
            }"""
        )
        req = Request(event, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        (err, res) = req.get_and_check_params(['mandatory1', 'mandatory2'], ['optional1'])
        self.assertFalse(res)
        self.assertEqual('Empty or missing mandatory parameter(s): mandatory1', str(err))

    def test_check_params(self):
        event = json.loads(
            """{
               "body":null,
               "queryStringParameters":{
                  "mandatory1":"foo",
                  "mandatory2":"bar",
                  "optional1":"baz",
                  "extra1":"quux"
               },
               "pathParameters":null
            }"""
        )
        req = Request(event, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        (err, res) = req.get_and_check_params(['mandatory1', 'mandatory2'], ['optional1'])
        self.assertTrue(res)
        self.assertEqual(['mandatory1', 'mandatory2', 'optional1'], sorted(req.params.keys()))

    def test_check_params_optional(self):
        event = json.loads(
            """{
               "body":null,
               "queryStringParameters":{
                  "mandatory1":"foo",
                  "mandatory2":"bar",
                  "optional1":"baz",
                  "extra1":"quux"
               },
               "pathParameters":null
            }"""
        )
        req = Request(event, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        (err, res) = req.get_and_check_params(['mandatory1', 'mandatory2'], ['optional1', 'optional2', 'optional3'])
        self.assertTrue(res)
        self.assertEqual(['mandatory1', 'mandatory2', 'optional1'], sorted(req.params.keys()))

    def test_check_params_mandatory(self):
        event = json.loads(
            """{
               "body":null,
               "queryStringParameters":{
                  "mandatory1":"foo",
                  "mandatory2":"bar",
                  "optional1":"baz",
                  "extra1":"quux"
               },
               "pathParameters":null
            }"""
        )
        req = Request(event, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')

        (err, res) = req.get_and_check_params(['mandatory0', 'mandatory1', 'mandatory2'],
                                              ['optional1', 'optional2', 'optional3'])
        self.assertFalse(res)
        self.assertEqual('Empty or missing mandatory parameter(s): mandatory0', str(err))

    def test_check_params_are_on_path(self):
        req = Request(self.event_params, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        (err, res) = req.get_and_check_params(['mandatory1'], [])
        self.assertTrue(res)

    def test_check_params_with_missing(self):
        req = Request(self.event_params, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        err, res = req.check_params({}, ['foo'], [])
        assert res is None
        self.assertEqual('Empty or missing mandatory parameter(s): foo', str(err))

    def test_check_params_with_multiple_missing(self):
        req = Request(self.event_params, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        err, res = req.check_params({}, ['foo', 'bar'], [])
        assert res is None
        self.assertEqual('Empty or missing mandatory parameter(s): foo, bar', str(err))

    def test_check_params_with_missing_optional(self):
        req = Request(self.event_params, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        err, res = req.check_params({}, [], ['optional'])
        assert res is not None
        assert err is None

    def test_check_params_with_empty_mandatory(self):
        req = Request(self.event_params, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        err, res = req.check_params({'foo': ''}, ['foo'], [])
        assert res is None
        self.assertEqual('Empty or missing mandatory parameter(s): foo', str(err))

    def test_check_params_ignores_extras(self):
        params = {
            'mandatory': 'foo',
            'optional': 'bar',
            'extra': 'baz',
        }
        req = Request(self.event_params, '0fa8fc8f-b04a-11e6-b8ed-6dda0ca82a80')
        err, res = req.check_params(params, ['mandatory'], ['optional'])
        assert res is not None
        assert 'extra' not in res

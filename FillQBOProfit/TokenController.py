import os
import json
import requests
import configparser

class TokenController:
    class TokenResult:
        def __init__(self):
            self.access_token = ""
            self.refresh_token = ""
            self.error = ""

    access_token = ""

    def generate_refresh_token(self):
        print("GenerateRefreshToken(): ")

        auth_Code = configparser.ConfigParser()
        auth_Code.read('config.ini')
        auth_Code = auth_Code['DEFAULT']['Auth_Code']
        auth_Basic_Code = configparser.ConfigParser()
        auth_Basic_Code.read('config.ini')
        auth_Basic_Code = auth_Basic_Code['DEFAULT']['Auth_Basic_Code']

        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

        httpRequest = requests.post(url, headers={"Authorization": "Basic " + auth_Basic_Code},
                                     data={"grant_type": "authorization_code", "code": auth_Code,
                                           "redirect_uri": "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"})

        try:
            responseString = httpRequest.text
            httpResponse = httpRequest
            responseString = httpResponse.text
            oRes = json.loads(responseString)
            if oRes["error"] is not None:
                print("Error getting token =", oRes["error"])
            else:
                print("refresh_token =", oRes["refresh_token"])
                try:
                    curDir = os.path.dirname(os.path.abspath(__file__))
                    with open(curDir + "\\refresh_token.txt", "w") as f:
                        f.write(oRes["refresh_token"])
                except Exception as e:
                    pass
        except Exception as e:
            pass

    def update_access_token(self):
        bRet = True
        curDir = os.path.dirname(os.path.abspath(__file__))
        fullFilePath = curDir + "\\refresh_token.txt"

        if not os.path.exists(fullFilePath):
            print(f"Can't find file {fullFilePath}")
            return False

        with open(fullFilePath, 'r') as file:
            refresh_token = file.readline()

        if not refresh_token:
            bRet = False
            print(f"Error: file {fullFilePath} is empty.")
        else:
            print("UpdateAccessToken() refresh_token =", refresh_token)

            url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

            auth_Basic_Code = configparser.ConfigParser()
            auth_Basic_Code.read('config.ini')
            auth_Basic_Code = auth_Basic_Code['DEFAULT']['Auth_Basic_Code']

            try:
                httpRequest = requests.post(url, headers={"Authorization": "Basic " + auth_Basic_Code},
                                             data={"grant_type": "refresh_token", "refresh_token": refresh_token})
                responseString = httpRequest.text
                httpResponse = httpRequest
                responseString = httpResponse.text

                oRes = json.loads(responseString)
                TokenController.access_token = oRes["access_token"]
                print("UpdateAccessToken() access_token =", TokenController.access_token)
            except Exception as e:
                print("UpdateAccessToken(): Exception =", e)
                return False

        return bRet

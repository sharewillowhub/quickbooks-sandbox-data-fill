import json
import requests
import requestsexceptions
import datetime
import os
import config
import Runner

class CustomerRefCl:
    def __init__(self):
        self.name = ""
        self.value = ""  # id


class ItemRefCl:
    def __init__(self):
        self.value = ""  # id


class SalesItemLineCl:
    def __init__(self):
        self.ItemRef = ItemRefCl()


class ItemLine:
    def __init__(self):
        self.DetailType = "SalesItemLineDetail"
        self.Amount = 0.0
        self.SalesItemLineDetail = SalesItemLineCl()


class Txn:
    def __init__(self):
        self.TxnDate = ""
        self.Line = []

class CustomerRefCr:
    def __init__(self):
        self.value = ""  # id

class Invoice(Txn):
    def __init__(self):
        super().__init__()
        self.CustomerRef = CustomerRefCr()


class Bill(Txn):
    def __init__(self):
        super().__init__()
        self.VendorRef = CustomerRefCl()
        self.Line = []


class BillLine:
    def __init__(self):
        self.DetailType = "AccountBasedExpenseLineDetail"
        self.Amount = 0.0
        self.AccountBasedExpenseLineDetail = AccountBasedExpenseLineDetail()


class AccountBasedExpenseLineDetail:
    def __init__(self):
        self.AccountRef = CustomerRefCl()


class TokenController:
    access_token = None

    @staticmethod
    def generate_refresh_token():
        auth_code = os.environ.get("Auth_Code")  # Assuming Auth_Code is stored in environment variables
        auth_basic_code = os.environ.get("Auth_Basic_Code")  # Assuming Auth_Basic_Code is stored in environment variables

        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        headers = {"Authorization": "Basic " + auth_basic_code}
        data = {"grant_type": "authorization_code", "code": auth_code,
                "redirect_uri": "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"}

        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        if "error" in response_data:
            print("Error getting token:", response_data["error"])
        else:
            TokenController.access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)
            print("Refresh token successfully written to file.")

    @staticmethod
    def update_access_token():
        try:
            with open("refresh_token.txt", "r") as f:
                refresh_token = f.read().strip()
        except FileNotFoundError:
            print("Refresh token file not found.")
            return False

        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        auth_basic_code = config.Auth_Basic_Code  # Assuming Auth_Basic_Code is stored in environment variables
        headers = {"Authorization": "Basic " + auth_basic_code}
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        if "error" in response_data:
            print("Error updating access token:", response_data["error"])
            return False
        else:
            TokenController.access_token = response_data["access_token"]
            print("Access token successfully updated.")
            return True

class Parser:
    @staticmethod
    def parse_entities(json_items):
        return json.loads(json_items)

class TokenResult:
    def __init__(self, access_token=None, refresh_token=None, error=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.error = error

class QueryResp:
    def __init__(self, query_response=None, time=None):
        self.QueryResponse = query_response
        self.time = time

class TokenResult:
    def __init__(self, access_token=None, refresh_token=None, error=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.error = error

class QueryRespAccount:
    def __init__(self, account=None):
        self.Account = account

class Account:
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id

class QueryRespCustomer:
    def __init__(self, customer=None):
        self.Customer = customer

class Customer:
    def __init__(self, DisplayName=None, CompanyName=None, Id=None, BillAddr=None):
        self.DisplayName = DisplayName
        self.CompanyName = CompanyName
        self.Id = Id
        self.BillAddr = BillAddr

class CustAddress:
    def __init__(self, Line1=None, City=None, CountrySubDivisionCode=None, PostalCode=None):
        self.Line1 = Line1
        self.City = City
        self.CountrySubDivisionCode = CountrySubDivisionCode
        self.PostalCode = PostalCode

class QueryRespItem:
    def __init__(self, item=None):
        self.Item = item

class Item:
    def __init__(self, Id=None, Name=None, UnitPrice=None):
        self.Id = Id
        self.Name = Name
        self.UnitPrice = UnitPrice

class QueryRespCustomerCr:
    def __init__(self, Customer=None):
        self.Customer = Customer

class QBAccessor:
    @staticmethod
    def get_accounts_test():
        #comp_url = config['appSettings']['Url']
        realm_ID = config.Realm_ID
        #config = configparser.ConfigParser()
        #tes1 = config['DEFAULT']
        #tes11 = config['DEFAULT']['Compression'] 
        #tes2 = config['forge.example']['User']
        #par = config['appSettings']['Realm_ID']

        url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realm_ID}/query?query=SELECT%20*%20FROM%20Account"
        headers = {"Authorization": f"Bearer {TokenController.access_token}"}
        try:
            response = requests.get(url, headers=headers)
            return response.ok
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def get_accounts():
        method_name = "get_accounts()"
        if not QBAccessor.get_accounts_test():
            token_controller = TokenController()
            if not token_controller.update_access_token():
                print(f"{method_name}() Failed to update keys.")
                return None

        realm_ID = config.Realm_ID
        comp_url = config.Url
        url = f"{comp_url}{realm_ID}/query?query=SELECT%20*%20FROM%20Account"
        headers = {
            "Authorization": f"Bearer {TokenController.access_token}",
            "Accept": "application/json"
        }
        try:
            response = requests.get(url, headers=headers)
            response_json = response.json()
            return response_json['QueryResponse']
        except Exception as e:
            print(f"get_accounts(): Exception = {e}")
            return None

    @staticmethod
    def get_customers():
        method_name = "get_customers()"

        if not QBAccessor.get_accounts_test():
            token_controller = TokenController()
            if not token_controller.update_access_token():
                print(f"{method_name}() Failed to update keys.")
                return None

        realm_ID = config.Realm_ID
        comp_url = config.Url

        url = f"{comp_url}{realm_ID}/query?query=SELECT%20*%20FROM%20Customer"

        headers = {
            "Authorization": f"Bearer {TokenController.access_token}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            print(response.status_code)
            return response_json['QueryResponse']
        except Exception as e:
            print(f"{datetime.now()} get_customers(): Exception = {e}")

    @staticmethod
    def get_vendors():
        method_name = "get_vendors()"

        if not QBAccessor.get_accounts_test():
            token_controller = TokenController()
            if not token_controller.update_access_token():
                print(f"{method_name}() Failed to update keys.")
                return None

        realm_ID = config.Realm_ID
        comp_url = config.Url

        url = f"{comp_url}{realm_ID}/query?query=SELECT%20*%20FROM%20Vendor"
        headers = {"Authorization": f"Bearer {TokenController.access_token}", "Accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            print(response.status_code)
            #vend_resp = Parser.parse_entities(json.dumps(response_data))
            return response_json['QueryResponse']
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_items():
        method_name = "get_items()"

        if not QBAccessor.get_accounts_test():
            token_controller = TokenController()
            if not token_controller.update_access_token():
                print(f"{method_name}() Failed to update keys.")
                return None

        realm_ID = config.Realm_ID
        comp_url = config.Url

        url = f"{comp_url}{realm_ID}/query?query=SELECT%20*%20FROM%20Item"
        headers = {"Authorization": f"Bearer {TokenController.access_token}", "Accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            print(response.status_code)
            return response_json['QueryResponse']
        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def create_invoice(invoice):
        method_name = "create_invoice()"

        if not QBAccessor.get_accounts_test():
            token_controller = TokenController()
            if not token_controller.update_access_token():
                print(f"{method_name}() Failed to update keys.")
                return None

        realm_ID = config.Realm_ID
        comp_url = config.Url

        url = f"{comp_url}{realm_ID}/invoice"
        headers = {"Authorization": f"Bearer {TokenController.access_token}", "Accept": "application/json", "Content-Type": "application/json"}

        try:
           inv_json = json.dumps(invoice, default=lambda x: x.__dict__)

           response = requests.request("POST", url, headers=headers, data=inv_json)
           print(response.status_code)
        except Exception as e:
          print(f"Error: {e}")

    @staticmethod
    def create_bill(bill):
        if not QBAccessor.get_accounts_test():
          token_controller = TokenController()
          if not token_controller.update_access_token():
            print(f"{method_name}() Failed to update keys.")
            return None

        realm_ID = config.Realm_ID
        comp_url = config.Url
        url = f"{comp_url}{realm_ID}/bill"
        headers = {"Authorization": f"Bearer {TokenController.access_token}", "Accept": "application/json", "Content-Type": "application/json"}
        try:
            bill_json = json.dumps(bill, default=lambda x: x.__dict__)
            response = requests.request("POST", url, headers=headers, data=bill_json)
            print(response.status_code)
        except Exception as e:
            print(f"Error: {e}")

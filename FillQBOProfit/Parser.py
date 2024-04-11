import json

class Parser:
    @staticmethod
    def parse_entities(json_items):
        entities_obj = json.loads(json_items)
        return entities_obj

class QueryResp:
    def __init__(self):
        self.QueryResponse = None
        self.time = None

class QueryRespAccount:
    def __init__(self):
        self.Account = []

class Account:
    def __init__(self):
        self.name = ""
        self.id = ""

class QueryRespCustomer:
    def __init__(self):
        self.Customer = []

class QueryRespVendor:
    def __init__(self):
        self.Vendor = []

class Customer:
    def __init__(self):
        self.DisplayName = ""
        self.CompanyName = ""
        self.Id = ""
        self.BillAddr = CustAddress()

class CustAddress:
    def __init__(self):
        self.Line1 = ""
        self.City = ""
        self.CountrySubDivisionCode = ""
        self.PostalCode = ""

class QueryRespItem:
    def __init__(self):
        self.Item = []

class Item:
    def __init__(self):
        self.Id = ""
        self.Name = ""
        self.UnitPrice = 0.0

class QueryRespCustomerCr:
    def __init__(self):
        self.Customer = Customer()

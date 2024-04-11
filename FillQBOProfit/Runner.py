import datetime
import json
import requests
import QBAccessor

class Runner:
    def testCreateInvoice():
        url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365045540500/invoice"

        payload = json.dumps({
          "TxnDate": "2023-04-05",
          "Line": [
            {
              "DetailType": "SalesItemLineDetail",
              "Amount": 15,
              "SalesItemLineDetail": {
                "ItemRef": {
                  "value": "22"
                }
              }
            }
          ],
          "CustomerRef": {
            "value": "89"
          }
        })
        headers = {
          'Accept': 'application/json',
          'Authorization': 'Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..9G6bteXjcBqvB7rMR5TAgA.o7yT7nt2s5b0I85QJmVaE4gQ3BAPjMjXw1FasTU3cdBhW1pHJ2HuZdP-Y9A7PDg28dCI7Os1OyLSTwjVfUi15qviefrM5mMsU8ktFyqez6DJb2wOsPxvfsQQneMm4XWIKELnIDvSvmR1VarAVGQjd_INml28tJ-X8al77kse3kmUcZeCckY2Xl0N3MtbAehQZGujRGdOae_9bsPJvQOX58Z4lQLZ_JOeEJuf9hjFCf4B3TumnWVNAr9XmYPHRWmB78ovdZLNad6sCIZawqem6cn9U2kCJqLp0oJ5s2S2iFhSXZPJbN24epDjg-FVqKfSenJ5QCfYOEtqYoj99duRZAiHHDoYr_PUZJgjpYRw25gkXMYV8Z9StiwjpkG9uDCZKLfdc872skbtHuDQewMRpT9Hgbtxtz3f-T_HBKeF4QAck7ylVKgr7U-WKM3NHrN5xXR__2t7kilUNQORfSKdKtst8XpuXaf7KBeuVOE2UxPVVzNPtYmqWH_7QbLhn1Cr28lLXGDsOiHMLdBjyaRH6MgZg1APWyjsHpyVNTP_Cy89E4j_vOgEr6Haaq2WqrF_QCg7MLhk5rOXWFi6479pRxmwxudw4bFWVNMXdpLkSPsIc69aecHbD5nBTjEcUL3RxC7kmZJJeg7duVQ57Qc7gIhZAxScBhAC_-MTXHFX6S_bauPZ_Q4P_fvhlZINXcY6Cp5i71vNlv-6ZoZ4jjJAQKCnqh4QKFT1dpUzSX-ydTk.6lnpama1VL493hOBJXBR6A',
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


    def test():
        print("Test")
        custs = QBAccessor.QBAccessor.get_customers()
        cus = QBAccessor.CustomerRefCl()
        invoice = QBAccessor.Invoice()
        customer_id = custs['Customer'][0]
        s = 2
    @staticmethod
    def run():
        minus_4_months = datetime.datetime.now() - datetime.timedelta(days=120)
        year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

        # Invoice
        customers = QBAccessor.QBAccessor.get_customers()
        customer_id = customers['Customer'][0]['Id']
        invoice = QBAccessor.Invoice()
        date = datetime.datetime.now() - datetime.timedelta(days=30)
        invoice.TxnDate = date.strftime("%Y-%m-%d")
        invoice.CustomerRef.value = customer_id

        items = QBAccessor.QBAccessor.get_items()
        item_id = items['Item'][0]['Id']
        line = QBAccessor.ItemLine()
        line.SalesItemLineDetail.ItemRef.value = item_id
        line.Amount = 15
        invoice.Line.append(line)
        #line_json = json.dumps(invoice, default=lambda x: x.__dict__)
        #print('Line --------')
        #print(line_json)

        # Bill
        vendors = QBAccessor.QBAccessor.get_vendors()
        accounts = QBAccessor.QBAccessor.get_accounts()

        bill = QBAccessor.Bill()
        bill.VendorRef.value = vendors['Vendor'][0]['Id']

        accntId = ""
        for accn in accounts['Account']:
            if "Payable" not in accn['Name'] and "Receivable" not in accn['Name']:
                accntId = accn['Id']
                break

        bill_line = QBAccessor.BillLine()
        bill_line.AccountBasedExpenseLineDetail.AccountRef.value = accntId
        bill_line.Amount = 10
        bill.Line.append(bill_line)

        current_date = year_ago
        while current_date < minus_4_months:
            invoice.TxnDate = current_date.strftime("%Y-%m-%d")
            #inv_json = json.dumps(invoice)
            #print(inv_json)
            QBAccessor.QBAccessor.create_invoice(invoice)
            bill.TxnDate = current_date.strftime("%Y-%m-%d")
            QBAccessor.QBAccessor.create_bill(bill)
            print("Created transactions with date", current_date)
            current_date += datetime.timedelta(days=7)

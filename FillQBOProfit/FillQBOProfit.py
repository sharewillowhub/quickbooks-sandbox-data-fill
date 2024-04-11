import QBAccessor
import Runner

if __name__ == "__main__":
    print("Program started.")
    QBAccessor = QBAccessor.QBAccessor
    #accns = QBAccessor.get_accounts()
    #customers = QBAccessor.get_customers()
    #invoice = Invoice()
    ##print(customers)
    #vendors = QBAccessor.get_vendors()
    #print(vendors)

    #QBAccessor.get_vendors()
    rn = Runner.Runner
    #rn.test()
    #rn.testCreateInvoice()
    Runner.Runner.run()

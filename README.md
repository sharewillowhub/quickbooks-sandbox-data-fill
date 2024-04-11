# Summary

The purpose of this repo is to backfill random data into a quickbooks sandbox account. 

## Installations steps

### Python

Install python and pip

```
pip install -r requirements.txt
```

### Example Files
You will need to move and edit the example files provided in the repo:

```
% mv FillQBOProfit/config.py{.example,}
% mv FillQBOProfit/refresh_token.txt{.example,}
```

### Quickboks Instructions
1. Go https://developer.intuit.com/app/developer/appdetail/test/keys?appId=djQuMTo6OGQzYmJlYTI3Yg:70a9a8e5-f1e2-4cbd-8d40-8b528e8dc3e4
	and check your Redirect URI should be https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl
	if there is no such record, add it clicking on "Add URI"
2. Go to https://developer.intuit.com/app/developer/playground
3. Select your app from Select app box and click "Next" https://prnt.sc/v6o90t 
4. In OAuth settings group, scopes check Accounting, OpenID, Profile, Email, Phone, Address checkboxs and click "Get Authorization Code"
5. Fill Realm ID into Realm_ID in your `config.py` file in the FillQBOProfit folder
6. Click "Get tokens" button and copy code next to "Authorization Basic:" (124-lenght string) https://prnt.sc/v6pqpe
	Paste this code into Auth_Basic_Code field in your `config.py`
7. Copy Authorization Code https://prnt.sc/v6pwca 
	and paste it into Auth_Code field in your FillQBOProfitLoss.exe.config
8. Open `refresh_token.txt` and put there refresh token instead existing text
	Your app is ready to use.
	To run it use `python FillQBOProfit.py` in Release folder.
	
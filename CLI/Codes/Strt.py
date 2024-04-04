import Grp_Server,Grp_Client,Personal_Server,Personal_Client

def grp_cht():
     print(" \n 1.New Chat. \n 2.Connect to a Chat. \n")
     a = input("Select an Option :")
     if int(a) == 1:
          Grp_Server.initialize_client()
     if int(a) == 2:
          Grp_Client.strt()
def prv_cht():
     print(" \n 1.New Chat. \n 2.Connect to a User. \n")
     a = input("Select an Option :")
     if int(a) == 1:
          Personal_Server.strt()
     if int(a) == 2:
          Personal_Client.strt()
print("                           Welcome to Safe Chat.\n \nIf you Want to start Encrypted Safe chatting Select the below Options.\n \n   1.Group Chat. \n   2.Private Chat. \n")
a = input("Select an Option :")
if int(a)==1:
    grp_cht()
if int(a)==2:
     prv_cht()
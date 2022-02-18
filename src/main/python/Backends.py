import numpy as np
import os
from Utils import save_csv,load_csv
from dateutil import parser
import datetime
DEFAULT_OUTPUT_FOLDER="/home/adwaye/Documents/account_details"





def getDateTimeFromISO8601String(s):
    d = parser.parse(s)
    return d


class ACCOUNT(object):
    def __init__(self,name,opening_balance = None,date=None):
        """

        :param name:
        :param metadata:
        """
        self._name          = name
        self._target_dest   = DEFAULT_OUTPUT_FOLDER



        self._output_folder = os.path.join(DEFAULT_OUTPUT_FOLDER,name)
        if not os.path.isdir(self._output_folder):
            os.makedirs(self._output_folder)
        fname = os.path.join(self._output_folder,'metadata.csv')
        if os.path.isfile(fname):
            self._metadata = load_csv(fileName=fname)
        else:
            self._metadata = {}
            if opening_balance is not None:
                if date is None: self._metadata['date']  = [datetime.date.today().isoformat()]
                else: self._metadata['date']  = [date.isoformat()]

                self._metadata['name']  = ["opening balance"]
                self._metadata['description'] = ["opening balance"]
                self._metadata['value'] = [opening_balance]
                self._metadata['dr']    = [1]
                self._metadata['cr']    = [0]
                save_csv(self._metadata,os.path.join(self._output_folder,'metadata.csv'))

    def credit(self,account,value,date,description=" "):
        """

        :param account: name of account to transfer money to string
        :param value:   value of amount float
        :param date:    date the transaction was made datetime.datetime
        :param description: string describing what this is for
        :return:
        """
        # assert type(date) is datetime.datetime
        target_account_path = os.path.join(self._target_dest,account)
        if not os.path.isdir(target_account_path):
            os.makedirs(target_account_path)
        if os.path.isfile(os.path.join(target_account_path,"metadata.csv")):
            target_meta = load_csv(os.path.join(target_account_path,"metadata.csv"))
            target_meta["date"]  +=[date]
            target_meta["dr"]    += [1]
            target_meta["cr"]    += [0]
            target_meta["name"]  += [self._name]
            target_meta["value"] += [value]
            target_meta["description"] += [description]
        else:
            target_meta = {}
            target_meta["date"]  =[date]
            target_meta["dr"]    = [1]
            target_meta["cr"]    = [0]
            target_meta["name"]  = [self._name]
            target_meta["value"] = [value]
            target_meta["description"] = [description]

        save_csv(target_meta,os.path.join(target_account_path,"metadata.csv"))

        if bool(self._metadata):
            self._metadata["date"]  +=[date]
            self._metadata["dr"]    += [0]
            self._metadata["cr"]    += [1]
            self._metadata["name"]  += [account]
            self._metadata["value"] += [value]
            self._metadata["description"] += [description]
        else:
            self._metadata["date"]  =[date]
            self._metadata["dr"]    = [0]
            self._metadata["cr"]    = [1]
            self._metadata["name"]  = [account]
            self._metadata["value"] = [value]
            self._metadata["description"] = [description]
        save_csv(self._metadata,os.path.join(self._output_folder,"metadata.csv"))


    def debit(self,account,value,date,description=" "):
        """

        :param account: name of account to transfer money to string
        :param value:   value of amount float
        :param date:    date the transaction was made string
        :param description: string describing what this is for
        :return:
        """
        # assert type(date) is datetime.datetime
        target_account_path = os.path.join(self._target_dest,account)
        if not os.path.isdir(target_account_path):
            os.makedirs(target_account_path)
        if os.path.isfile(os.path.join(target_account_path,"metadata.csv")):
            target_meta = load_csv(os.path.join(target_account_path,"metadata.csv"))
            target_meta["date"]  +=[date]
            target_meta["dr"]    += [0]
            target_meta["cr"]    += [1]
            target_meta["name"]  += [self._name]
            target_meta["value"] += [value]
            target_meta["description"] += [description]
        else:
            target_meta = {}
            target_meta["date"]  =[date]
            target_meta["dr"]    = [0]
            target_meta["cr"]    = [1]
            target_meta["name"]  = [self._name]
            target_meta["value"] = [value]
            target_meta["description"] = [description]

        save_csv(target_meta,os.path.join(target_account_path,"metadata.csv"))

        if bool(self._metadata):
            self._metadata["date"]  +=[date]
            self._metadata["dr"]    += [1]
            self._metadata["cr"]    += [0]
            self._metadata["name"]  += [account]
            self._metadata["value"] += [value]
            self._metadata["description"] += [description]
        else:
            self._metadata["date"]  =[date]
            self._metadata["dr"]    = [1]
            self._metadata["cr"]    = [0]
            self._metadata["name"]  = [account]
            self._metadata["value"] = [value]
            self._metadata["description"] = [description]
        save_csv(self._metadata,os.path.join(self._output_folder,"metadata.csv"))

    def view_balance(self,date):
        dates        = self._metadata["date"]
        dates_bool   = [getDateTimeFromISO8601String(f)<date for f in dates]
        debit_bools  = np.array(self._metadata["dr"],dtype=bool)
        credit_bools = np.array(self._metadata["cr"],dtype=bool)
        values       = np.array(self._metadata["value"],dtype=float)
        debit_index  = np.logical_and(debit_bools,dates_bool)
        credit_index = np.logical_and(credit_bools,dates_bool)
        all_debits   = values[debit_index]
        print(all_debits)
        all_credits  = values[credit_index]
        print(all_credits)
        balance = np.sum(all_debits)-np.sum(all_credits)
        print("balance as at "+date.isoformat()+" is {:}".format(balance))
        my_dict = { "date": date.isoformat,
                    "description": "Balance as at",
                    "value"      : balance
        }
        return my_dict



class BET(object):
    def __init__(self,account,amount,odds,event,bet_type,commission,date):
        """

        :param account:
        :param amount:
        :param odds:
        :param event:
        :param bet_type: Back-Normal, Back-Free, Lay
        :param commission:
        :param date:
        """
        self._account  = account
        self._stake    = amount
        self._bet_type = bet_type
        self._odds     = odds
        self._description = event
        self._commission = commission
        self._date       = date
        self._status     = 'Open'
        self._tracker_location = os.path.join(DEFAULT_OUTPUT_FOLDER,'bet_tracker.csv')
        self._id = None


    def load_from_tracker(self,id):

        tracker = load_csv(self._tracker_location)
        id_array = np.array(tracker['id'])
        if len(id_array)>1:

            idx = np.where(id_array == str(id))[0]
            idx= idx[0]



        else:
            idx=0
        self._account = tracker["Account"][idx]
        self._stake = float(tracker["Stake"][idx])
        self._bet_type = tracker["Type"][idx]
        self._odds     = float(tracker["Odds"][idx])
        self._description = tracker["Event"][idx]
        self._commission = float(tracker["Commission"][idx])
        self._date       =  tracker["Date"][idx]
        self._status     =  tracker["Status"][idx]
        self._id = id




    def _win(self,date=None):
        if date is None:
            date = datetime.datetime.now().isoformat()
        if self._status!='Open':
            print('bet already settled')
        else:
            account1 = ACCOUNT(name=self._account)

            if self._bet_type=="Back-Normal":
                account1.debit(account="Bets",value=self._stake+self._stake*(self._odds-1)*(
                        1-self._commission),
                               date=date,description=self._description)
            elif self._bet_type=="Back-Free":
                account1.debit(account="Bets",value=self._stake*(self._odds-1)*(1-self._commission),
                               date=date,description=self._description)

            elif self._bet_type=="Lay":
                account1.debit(account="Bets",value=self._stake +  (1 - self._commission)*self._stake,
                               date=date,description=self._description)
                exposure_value = (self._odds-2)*self._stake
                account1.credit(account="Exposure",value=exposure_value,date=date,description=self._description)
            self.settle_bet(result='Win')


    def _lose(self,date=None):
        if date is None:
            date = datetime.datetime.now().isoformat()
        if self._status!='Open':
            print('bet already settled')
        else:
            account1 = ACCOUNT(name="Bets")
            account2 = ACCOUNT(name="Exposure")
            if self._bet_type=="Back-Normal":
                account1.credit(account="Pay-outs",value=self._stake,date=date,description=self._description)
            elif self._bet_type == "Back-Free":
                account1.credit(account="Pay-outs",value=self._stake,date=date,description=self._description)
            elif self._bet_type=="Lay":
                account1.credit(account="Pay-outs",value=self._stake,date=date,description=self._description)
                exposure_value = (self._odds-2)*self._stake
                account2.credit(account="Pay-outs",value=exposure_value,date=date,description=self._description)
            self.settle_bet(result='Lose')

    def make_bet(self):
        account1 = ACCOUNT(name=self._account)
        if self._bet_type=="Back-Normal":
            account1.credit(account="Bets",value=self._stake,date=datetime.datetime.now().isoformat(timespec="minutes"),
                            description=self._description)
        elif self._bet_type=="Back-Free":
            account1.debit(account="Offers",value=self._stake,date=datetime.datetime.now().isoformat(
                timespec="minutes"),
                            description=self._description)
            account1.credit(account="Bets",value=self._stake,date=datetime.datetime.now().isoformat(timespec="minutes"),
                            description=self._description)
        elif self._bet_type=="Lay":
            account1.credit(account="Bets",value=self._stake,date=datetime.datetime.now().isoformat(timespec="minutes"),
                            description=self._description)
            exposure_value = (self._odds-2)*self._stake
            account1.credit(account="Exposure",value=exposure_value,date=datetime.datetime.now().isoformat(
                timespec="minutes"),
                            description=self._description)
        self.enter_bet_in_book()


    def enter_bet_in_book(self):
        if os.path.isfile(self._tracker_location):
            tracker = load_csv(self._tracker_location)
            id = tracker['id'][-1]
            self._id =int(id)+1
            tracker['id'] += [str(int(id)+1)]
            tracker['Date'] += [self._date]
            tracker['Account'] += [self._account]
            tracker['Stake']   += [self._stake]
            tracker['Type']    += [self._bet_type]
            tracker['Event']   += [self._description]
            tracker['Commission'] += [self._commission]
            tracker['Odds'] += [self._odds]
            tracker['Status'] += ["Open"]
        else:
            tracker = {}
            tracker['id'] = [1]
            self._id = 1
            tracker['Date'] = [self._date]
            tracker['Account'] = [self._account]
            tracker['Stake'] = [self._stake]
            tracker['Type'] = [self._bet_type]
            tracker['Event'] = [self._description]
            tracker['Commission'] = [self._commission]
            tracker['Odds'] = [self._odds]
            tracker['Status'] = ["Open"]
        save_csv(tracker,self._tracker_location)


    def settle_bet(self,result):
        """

        :param result: 'Lose' or 'Win'
        :return:
        """
        tracker = load_csv(self._tracker_location)
        id_array = np.array(tracker['id'])
        if len(id_array)>1:
            print(id_array)
            print(self._id)
            index = np.where(id_array==str(self._id))[0][0]


            tracker['Status'][index] = result

        else:

            tracker['Status'] = [result]
        save_csv(tracker,self._tracker_location)











if __name__=="__main__":
    _date0 = datetime.datetime(2020,1,31,20,1,0,0)
    _date1 = datetime.datetime(2021,1,31,20,1,0,0)
    _date_check = datetime.datetime(2021,2,1,23,1,0,0)
    _date2 = datetime.datetime(2021,2,28,20,1,0,0)

    _date3 = datetime.datetime(2022,1,31,20,1,0,0)

    account1 = ACCOUNT(name="cash",opening_balance=100,date=_date0)
    account1.debit(account="sales",value=25,date=_date1.isoformat(timespec='minutes'))
    account1.credit(account="Betfred",value=10,date=_date2.isoformat(timespec='minutes'))
    account1.credit(account="salary",value=90,date=_date3.isoformat(timespec='minutes'))


    bet1 = BET(account="Betfred",amount=10,odds=5.0,event="Liverpool vs Inter Milan",bet_type="Back-Normal",
               commission=0,date=_date2.isoformat())
    _date_settle = datetime.datetime(2021,3,12,20,1,0,0)
    bet1.make_bet()


    bet1._win()

    bet2 = BET(account="Smarkets",amount=10,odds=4.8,event="Liverpool vs Inter Milan",bet_type="Lay",
               commission=0.02,date=_date2.isoformat())

    bet2.make_bet()
    bet3 = BET(account="",amount=10,odds=5.0,event="",bet_type="",
               commission=0,date=_date2.isoformat())
    bet3.load_from_tracker(id=2)
    bet3._lose(date=_date_settle)



    account1.view_balance(date=_date_check)








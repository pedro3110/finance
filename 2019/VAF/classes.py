# discounting = ['COMPOUND', CONTINUOUS']
import numpy as np
import pandas as pd
from datetime import datetime
from scipy import optimize

class Discount:
    def __init__(self, discounting):
        self.discounting = discounting
    
    def get_discount(self, value, factor, year_fraction):
        if self.discounting == 'COMPOUND':
            return value / (1+factor)**year_fraction
        elif self.discounting == 'CONTINUOUS':
            return value * np.exp(-(factor * year_fraction))
        else:
            raise Exception('Error')

# discounting = 'CONTINUOUS'
# discount(value=10, factor=0.05, year_fraction=1)
# 9.51229424500714*np.exp(0.05*1)

# discounting = 'COMPOUND'
# discount(value=10, factor=0.05, year_fraction=0.5)
# 9.759000729485333 * (1+0.05)**0.5

class CashFlow:
    def __init__(self, dates, payments):
        if len(dates) != len(payments):
            raise Exception('Error de cashflow')
        else:
            self.dates = dates
            self.payments = payments
            self.df = pd.DataFrame(data={'Date': dates, 'Payment': payments})
class Bond:
    def __init__(self, name, base_date, cashflow: 'CashFlow'):
        if min(cashflow.dates) < base_date:
            raise Exception('Error: base date must be earlier than first cash flow')
        else:
            self.name = name
            self.base_date = base_date
            self.cashflow = cashflow
            self.maturity_date = max(self.cashflow.dates)
            self.df = self.cashflow.df
            self.df['Bond'] = self.name
            self.df['Base Date'] = self.base_date
            self.df['Maturity Date'] = self.maturity_date
            self.df['Period'] = self.df[['Base Date', 'Date']].apply(lambda row: (row[1]-row[0]).days / 365., 1)
            self.periods = self.df['Period'].tolist()
            self.payments = self.df['Payment'].tolist()
            
class ExcelReader:
    @staticmethod
    def read(today, filename):
        xl = pd.ExcelFile('Portfolio.xlsx')
        sheet_names = [name for name in xl.sheet_names if name not in ['Portfolio']]
        dfs = []
        for sheet_name in sheet_names:
            new_df = pd.read_excel(open('Portfolio.xlsx', 'rb'), sheet_name=sheet_name)[['Fecha de Pago', 'Cash Flow']]
            new_df['Bond'] = sheet_name
            new_df['Cash Flow'] = new_df['Cash Flow'].apply(lambda cf: cf.replace(',','.'))
            new_df['Cash Flow'] = pd.to_numeric(new_df['Cash Flow'])

            new_df['Price'] = -new_df.iloc[0]['Cash Flow']
            new_df['Price Date'] = new_df.iloc[0]['Fecha de Pago']
            new_df = new_df.drop(0)
            new_df['Fecha de Pago'] = pd.to_datetime(new_df['Fecha de Pago'], format="%d/%m/%Y")
            dfs.append(new_df)
        df = pd.concat(dfs, 0)
        df['Fecha de Pago'] = pd.to_datetime(df['Fecha de Pago'], format="%d/%m/%Y")

        df['Price Date'] = today
        return df
    
from datetime import date
import scipy.optimize

class BondGenerator:
    @staticmethod
    def bond_from_dataframe(df):
        name = df.iloc[0].Bond
        base_date = df.iloc[0]['Price Date']
        price = df.iloc[0]['Price']
        dates = [base_date] + df['Fecha de Pago'].tolist()
        payments = [(-1) * price] + df['Cash Flow'].tolist()
        cashflow = CashFlow(dates, payments)
        return Bond(cashflow=cashflow, name=name, base_date=base_date)
    
class YTMCalculator:
    def npv(self, rate):
        if rate <= -1.0:
            return float('inf')
        tot = sum([self.discount.get_discount(vi, rate, di) 
                    for vi, di in zip(self.payments, self.periods)])
        return tot
        
    def ytm(self):
        try:
            return scipy.optimize.newton(lambda r: self.npv(r), 0.1)
        except RuntimeError:    # Failed to converge?
            return scipy.optimize.brentq(lambda r: self.npv(r), -1.0, 1e10)
        
    def get_ytm(self, bond: 'Bond', discount: 'Discount'):
        # Asume que el dataframe viene ordenado por fecha de pago de renta ('Date')
        self.discount = discount
        self.periods = bond.periods
        self.payments = bond.payments
        try:
            return scipy.optimize.newton(lambda r: self.npv(r), 0)
        except RuntimeError:    # Failed to converge?
            return scipy.optimize.brentq(lambda r: self.npv(r), -1.0, 1e10)
        
class Curve:
    
    def _get_next_spot(self, current_yield, periods, ytms, spots):
        def npv(x):
            spots_modified = spots + [x]
            if len(spots) == 0:
                rate_now = ytms[len(spots)]
            else:
                rate_now = ytms[len(spots)] * (periods[len(spots)] - periods[len(spots)-1])

            cf = [rate_now for _ in spots] + [current_yield + rate_now]
            return current_yield - sum([cf[i] / (1 + spots_modified[i]) ** periods[i] for i in range(len(periods))])
        return npv
    
    def get_spot_curve(self, base_date, instruments, discount: 'Discount'):
        # Prueba:
        # ps    = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
        # ytms  = [0.0590,0.0650,0.0730,0.0800,0.0870,0.0950,0.01030,0.01070,0.01100,0.01130,0.01160,0.01190,0.01220,0.01250,0.01280,0.01310,0.01340,0.01370,0.01400,0.01430]
        # spots = [0.059, 0.065]
        calculator = YTMCalculator()
        
        ytms = [calculator.get_ytm(instr, discount) for instr in instruments]
        ps = [(instr.maturity_date - base_date).days / 365. for instr in instruments]
        
        spots = [calculator.get_ytm(instr, discount) for instr in instruments if len(instr.payments)==1]
        while(len(spots) < len(ytms)):
            new_val = optimize.newton(self._get_next_spot(1, ps[0:len(spots)+1], ytms[0:len(spots)+1], spots), 0.1)
            spots += [new_val]
        return spots
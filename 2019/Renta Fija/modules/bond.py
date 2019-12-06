from datetime import date
import scipy.optimize


class Actual365:
    @staticmethod
    def year_fraction_between(a,b):
        return (a-b).days / 365.
        
class Thirty360:
    @staticmethod
    def year_fraction_between(a,b):
        return (a-b).days / 360.

class Bond:
    
    def __init__(self, name, cashflow, day_count):
        self.name = name
        self.cashflow = cashflow
        self.dates, self.amounts = zip(*cashflow)
        self.day_count = day_count
        
    def maturity(self):
        return self.dates[-1]
        
    def npv(self, rate):
        if rate <= -1.0:
            return float('inf')
        d0 = self.dates[0]
        res = [ vi / (1.0 + rate)**((di - d0).days / 365.0) for vi, di in zip(self.amounts, self.dates)]
        print(res)
        return sum(res)

    def ytm(self):
        try:
            return scipy.optimize.newton(lambda r: self.npv(r), 0.0)
        except RuntimeError:    # Failed to converge?
            return scipy.optimize.brentq(lambda r: self.npv(r), -1.0, 1e10)

class BondGenerator:
    @staticmethod
    def bond_from_dataframe(df):
        return Bond(
            name=df.iloc[0]['Bond'],
            cashflow=[[df.iloc[0]['Price Date'], -df.iloc[0]['Price']]] + df[['Fecha de Pago', 'Cash Flow']].values.tolist(),
            day_count=Actual365
        )
    
#     @staticmthod
#     def zero_coupon():
#         zero_coupon = pd.DataFrame(data={
#             'Fecha de Pago': ['2020-04-18'], 'Cash Flow': [75.0], 'Bond': ['ZeroCoupon'], 'Price': [73.0], 'Price Date': ['2019-3-7']
#         })
#         zero_coupon['Fecha de Pago'] = pd.to_datetime(zero_coupon['Fecha de Pago'])
#         zero_coupon['Price Date'] = pd.to_datetime(zero_coupon['Price Date'])
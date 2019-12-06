import numpy as np
import scipy.interpolate
from datetime import timedelta

# fig, ax = plt.subplots(figsize=(20,5), ncols=2, nrows=1)
# sns.lineplot(data=z, x='maturity', y='yield', ax=ax[0])
# Anottations
# names_real = z.name.tolist()
# for c in ax[0].collections:
#     for i, of in enumerate(c.get_offsets()):
#         ax[0].annotate(names_real[i], of)

# # X-Axis Labels
# labels = ax[0].get_xticklabels()
# labels_real = z.maturity.tolist()
# for i,l in enumerate(labels):
#     if i%2 == 0 or i==len(labels)-1:
#         labels[i] = labels_real[i].strftime("%d-%m-%Y")
#     else:
#         labels[i] = ''
# ax[0].set_xticklabels(labels, rotation=30)


class Curve:
    # https://www.quantandfinancial.com/2012/08/yield-curve-bootstrapping.html
    
    def __init__(self, today, maturities, yields):
        self.today = today
        self.maturities = maturities
        self.yields = yields
    
    def interpolated_in_intervals(self, n_points):
        # Generate maturities 
        maturities_days = [(maturity - self.today).days for maturity in self.maturities]
        interpolated_maturities_numeric  = np.linspace(min(maturities_days), max(maturities_days), n_points)
        interpolated_maturities_datetime = [self.today + timedelta(days=x) for x in interpolated_maturities_numeric]
        
        # Interpolate
        y = []
        interp = scipy.interpolate.interp1d(maturities_days, self.yields, bounds_error=False, fill_value=scipy.nan)
        for i in interpolated_maturities_numeric:
            value = float(interp(i))
            if not scipy.isnan(value): # Don't include out-of-range values
                y.append(value)
        return interpolated_maturities_datetime, y
    
    def interpolated_in_specific_dates(self, specific_dates):
        # Generate maturities 
        maturities_days = [0] + [(maturity - self.today).days for maturity in self.maturities]
        yields = [0] + self.yields
        
        interpolated_maturities_numeric = [(d - self.today).days for d in specific_dates]
        
        # Interpolate
        y = []
        interp = scipy.interpolate.interp1d(maturities_days, yields, bounds_error=False, fill_value=scipy.nan)
        for i in interpolated_maturities_numeric:
            value = float(interp(i))
            if not scipy.isnan(value): # Don't include out-of-range values
                y.append(value)
        return specific_dates, y
    
class ForwardCurve:
    def __init__(self, today, maturities, yields):
        self.today = today
        self.maturities = maturities
        self.yields = yields
        
class SpotCurve(Curve):
    def __init__(self, today, maturities, yields):
        self.today = today
        self.maturities = maturities
        self.yields = yields
        self.map_maturity_yield = {self.today: 0}
        for i,_ in enumerate(maturities):
            self.map_maturity_yield[maturities[i]] = yields[i]

    def get_forward_curve(self):
        
        forward_rates = []
        periods = [self.today] + self.maturities
        for i, T in enumerate(zip(periods, periods[1:])):
            T1, T2 = T
            R1 = self.map_maturity_yield[T1]
            R2 = self.map_maturity_yield[T2]
            
            diff = (T2 - T1).days / 365.
            
            print ("#######")
            print('T1: ' + str(T1))
            print('T2: ' + str(T2))
            print('R1: ' + str(R1))
            print('R2: ' + str(R2))
            print('Days: ', (T2-T1).days)
            print('Diff: ', diff)
            
            forward_rate = (1+R2)**(1+diff)/(1+R1) - 1
            print(forward_rate)
            forward_rates.append(forward_rate)

        return ForwardCurve(self.today, self.maturities, forward_rates)

    
class YieldCurve(Curve):
    def __init__(self, today, instruments):
        self.today = today
        self.maturities = [instr.maturity() for instr in instruments]
        self.yields = [instr.ytm() for instr in instruments]
        self.names = [instr.name for instr in instruments]
        self.periods = [(instr.maturity() - self.today).days/365. for instr in instruments]

    def implied_spot_curve(self, n_points=None, specific_dates=None):
        if n_points is not None:
            interpolated_maturities, interpolated_yields = self.interpolated_in_intervals(n_points)
        elif specific_dates is not None:
            interpolated_maturities, interpolated_yields = self.interpolated_in_specific_dates(specific_dates)
        else:
            raise Exception('Wrong Parameters')
            
        maturities_years = [(maturity - self.today).days/365. for maturity in interpolated_maturities]
        spot_rates = []
        for i in range(0, len(interpolated_maturities)): #calculate i-th spot rate 
            tot = 0
            print("#######")
            for j in range(0, i): #by iterating through 0..i
                tot += interpolated_yields[i] / (1 + spot_rates[j])**maturities_years[j]
                print("# sum: ", interpolated_yields[i])
                
            print("tot = ", tot)
            print("n_days = ", (interpolated_maturities[i]-self.today).days)
            print("period = ", maturities_years[i])
            print("yield_interpolated = ", interpolated_yields[i])
            
            value = ((1+interpolated_yields[i]) / (1-tot))**(1/maturities_years[i]) - 1
            print("value = ", value)
            
            spot_rates.append(value)
        return SpotCurve(self.today, interpolated_maturities, spot_rates)
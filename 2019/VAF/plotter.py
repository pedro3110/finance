import pandas as pd
import seaborn as sns


class Plotter:
    
    @classmethod
    def dataframe_price_evolution(cls, T, n_obs, paths_sample):
        df = pd.DataFrame(data=paths_sample).T
        df_melt = pd.melt(df.reset_index(), id_vars='index',value_vars=list(range(0,10)))

        df_melt = df_melt.rename(columns={'index': 'time', 'variable': 'Simulation', 'value': 'Price'})
        df_melt['time'] = df_melt['time'] * T / n_obs
        return df_melt
    
    @classmethod
    def make_plot(cls, ax, df_melt, T):
        sns.tsplot(df_melt, time='time', unit = "Simulation", condition='Simulation', value='Price', ax=ax)
        ax.set_title('100 Shocks, 10 Simulations of brownian motion: S(t+1)=S(t) +S(t)[u * dt + sigma * dz(t)], dz(t) ~ N(0,sqrt(dt))')
        ax.set_xlim((0, T))
        ax.set_ylim((60,200))
        return ax
import tensorflow as tf
import numpy as np


class Pricer:
    
    @staticmethod
    def plain_vanilla_closed_formula_with_2nd_greeks(enable_greeks = True):
        # Reset previous graph
        tf.reset_default_graph()
        
        # Build the static computational graph
        S = tf.placeholder(tf.float32, name="S")
        K = tf.placeholder(tf.float32, name="K")
        dt = tf.placeholder(tf.float32, name="dt")
        sigma = tf.placeholder(tf.float32, name="sigma")
        r = tf.placeholder(tf.float32, name="r")
        
        # Closed Formula
        # Nonte: need connected gradients to get 2nd order greeks (https://www.tensorflow.org/api_docs/python/tf/gradients)
        Phi = tf.distributions.Normal(0.,1.).cdf
        d_1 = (tf.log(S / K) + (r+sigma**2/2)*dt) / (sigma*tf.sqrt(dt))
        d_2 = d_1 - sigma*tf.sqrt(dt)
        npv =  S*Phi(d_1) - K*tf.exp(-r*dt)*Phi(d_2)
        
        # Identifiers
        tf.identity(d_1, name="d_1")
        tf.identity(d_2, name="d_2")
        tf.identity(npv, name="NPV")
        
        target_calc = [npv]
        if enable_greeks:
            greeks = tf.gradients(npv, [S, sigma, r, K, dt])
            dS_2ndOrder = tf.gradients(greeks[0], [S, sigma, r, K, dt])
            dsigma_2ndOrder = tf.gradients(greeks[1], [S, sigma, r, K, dt])
            dr_2ndOrder = tf.gradients(greeks[2], [S, sigma, r, K, dt]) 
            dK_2ndOrder = tf.gradients(greeks[3], [S, sigma, r, K, dt]) 
            dT_2ndOrder = tf.gradients(greeks[4], [S, sigma, r, K, dt])
            target_calc += [greeks, dS_2ndOrder, dsigma_2ndOrder, dr_2ndOrder, dK_2ndOrder, dT_2ndOrder]

        def execute_graph(S_0, strike, time_to_expiry, implied_vol, riskfree_rate):
            with tf.Session() as sess:
                res = sess.run(target_calc, 
                               {
                                   S: S_0,
                                   K : strike,
                                   r : riskfree_rate,
                                   sigma: implied_vol,
                                   dt: time_to_expiry
                               })
            return res
        return execute_graph
    
    @classmethod
    def make_path_simulator(cls):
        # Reset previous graph
        tf.reset_default_graph()
        
        S = tf.placeholder(tf.float32, name="S")
        K = tf.placeholder(tf.float32, name="K")
        dt = tf.placeholder(tf.float32, name="dt")
        T = tf.placeholder(tf.float32, name="T")
        sigma = tf.placeholder(tf.float32, name="sigma")
        r = tf.placeholder(tf.float32, name="r")
        dw = tf.placeholder(tf.float32, name="dw")
        
        S_T = S * tf.cumprod(tf.exp((r-sigma**2/2)*dt+sigma*tf.sqrt(dt)*dw), axis=1, name="S_T")
        
        def paths(S_0, strike, time_to_expiry, implied_vol, riskfree_rate, seed, n_sims, n_obs):
            if seed != 0:
                np.random.seed(seed)
            stdnorm_random_variates = np.random.randn(n_sims, n_obs)
            with tf.Session() as sess:
                timedelta = time_to_expiry / stdnorm_random_variates.shape[1]
                res = sess.run(S_T, 
                               {
                                   S: S_0,
                                   K : strike,
                                   r : riskfree_rate,
                                   sigma: implied_vol,
                                   dt : timedelta,
                                   T: time_to_expiry,
                                   dw : stdnorm_random_variates
                             })
                return res
        return paths
    
    @classmethod
    def plain_vanilla_with_path(cls, enable_greeks = True):
        # Reset previous graph
        tf.reset_default_graph()
        
        S = tf.placeholder(tf.float32, name="S")
        K = tf.placeholder(tf.float32, name="K")
        dt = tf.placeholder(tf.float32, name="dt")
        T = tf.placeholder(tf.float32, name="T")
        sigma = tf.placeholder(tf.float32, name="sigma")
        r = tf.placeholder(tf.float32, name="r")
        dw = tf.placeholder(tf.float32, name="dw")
        
        # Trick: 1. initialize matrix with random shocks; 2. apply cumulative product function on each row 3. result: 1 column
        S_T = S * tf.cumprod(tf.exp((r-sigma**2/2)*dt+sigma*tf.sqrt(dt)*dw), axis=1, name="S_T")
        
        # S_T is column array; S_T[:,-1] is row array
        payout = tf.maximum(S_T[:,-1] - K, 0, name="Payout")
        
        # reduce_mean: calculate mean of payouts (S_t[:,-1] contains the last 'column' of the price evolution simulation)
        npv = tf.exp(-r*T) * tf.reduce_mean(payout, name="NPV")
        target_calc = [npv]
        if enable_greeks:
            greeks = tf.gradients(npv, [S, sigma, r, K, T])
            target_calc += [greeks]
            
            # Note: to calculate 2nd order derivatives, connections between variables must be declared explicitly in graph
            #       when simulating, it is not possible to do this
            # dS_2ndOrder = tf.gradients(greeks[0], [sigma, r])
            # target_calc += [greeks, dS_2ndOrder]
            
        def pricer(S_0, strike, time_to_expiry, implied_vol, riskfree_rate, seed, n_sims, n_obs):
            # seed: get same results in repeated executions
            if seed != 0:
                np.random.seed(seed)
                
            # n_sims = number of rows; n_obs = number of columns  
            stdnorm_random_variates = np.random.randn(n_sims, n_obs)
            with tf.Session() as sess:
                # time_to_expiry is in years
                timedelta = time_to_expiry / stdnorm_random_variates.shape[1]
                res = sess.run(target_calc, 
                               {
                                   S: S_0,
                                   K : strike,
                                   r : riskfree_rate,
                                   sigma: implied_vol,
                                   dt : timedelta,
                                   T: time_to_expiry,
                                   dw : stdnorm_random_variates
                             })
                return res
        return pricer
    
    @classmethod
    def analytical_downOut_tf_pricer(cls, enable_greeks = True):
        # Reset previous graph
        tf.reset_default_graph()
        
        S = tf.placeholder(tf.float32)
        K = tf.placeholder(tf.float32)
        dt = tf.placeholder(tf.float32)
        sigma = tf.placeholder(tf.float32)
        r = tf.placeholder(tf.float32)
        B = tf.placeholder(tf.float32)
        Phi = tf.distributions.Normal(0.,1.).cdf
        d_1 = (tf.log(S / K) + (r+sigma**2/2)*dt) / (sigma*tf.sqrt(dt))
        d_2 = d_1 - sigma*tf.sqrt(dt)
        bs_npv =  S*Phi(d_1) - K*tf.exp(-r*dt)*Phi(d_2)
        d_1a = (tf.log(B**2 / (S*K)) + (r+sigma**2/2)*dt) / (sigma*tf.sqrt(dt))
        d_2a = d_1a - sigma*tf.sqrt(dt)
        reflection = (S/B)**(1-r/sigma**2) * ((B**2/S)*Phi(d_1a) - K*tf.exp(-r*dt)*Phi(d_2a))
        npv = bs_npv - reflection
        
        target_calc = [npv]
        if enable_greeks:
            greeks = tf.gradients(npv, [S, sigma, r, K, dt, B])
            # Calculate mixed 2nd order greeks for S (esp. gamma, vanna) and sigma (esp. volga)
            dS_2ndOrder = tf.gradients(greeks[0], [S, sigma, r, K, dt, B]) 
            #dsigma_2ndOrder = tf.gradients(greeks[1], [S, sigma, r, K, dt, B]) 
            # Function to feed in the input and calculate the computational graph
            target_calc += [greeks, dS_2ndOrder]
            
        def price(S_0, strike, time_to_expiry, implied_vol, riskfree_rate, barrier):
            """
            Returns the npv, delta, vega and gamma
            """
            with tf.Session() as sess:

                res = sess.run(target_calc, 
                               {
                                   S: S_0,
                                   K : strike,
                                   r : riskfree_rate,
                                   sigma: implied_vol,
                                   dt: time_to_expiry,
                                   B : barrier})
            if enable_greeks:
                return np.array([res[0], res[1][0], res[1][1], res[2][0]])
            else:
                return res
        return price

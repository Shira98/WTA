import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl


def Normalize(x,maximum): #min=0.0 max=100.0
  return float((x-0.0)/(maximum-0.0))

def fuzzy(c,l): #Maps crisp to fuzzy sets.
  #3 I/P fuzzy sets: Low, Med, High.
  
  link=Normalize(l,50.0)
  content=Normalize(c,10.0)
  
  #6 O/P fuzzy sets: Very_low, Low, Med, Good, Very_Good, Excellent.
 
  fuzzy_set=[None,None] #[class of ContentScore, class of LinkScore from output sets]
  #output_fuzzy_sets=["very low","low","med","good","very good","excellent"]
  #input__fuzzy_sets=["low","med","high"]
  
  
  #Input and output ranges:
  content_score = ctrl.Antecedent(np.arange(0,1,0.001), 'content_score')
  link_score = ctrl.Antecedent(np.arange(0,1,0.001), 'link_score')
  relevant_score= ctrl.Consequent(np.arange(0,1,0.001), 'relevant_score')
  #print(content_limit)
    
  
  #Membership functions: Maps values to [0,1]
  
  content_score['low'] = fuzz.trapmf(content_score.universe, [0.01, 0.0825, 0.2475, 0.375])
  content_score['med'] = fuzz.trapmf(content_score.universe, [.32, .425, .577, .68]) 
  content_score['high'] = fuzz.trapmf(content_score.universe, [.63, .7425, .9075, 1.00]) 
  
  link_score['low'] = fuzz.trapmf(link_score.universe, [0.01, 0.0825, 0.2475, 0.375])
  link_score['med'] = fuzz.trapmf(link_score.universe, [.32, .425, .577, .68])
  link_score['high'] = fuzz.trapmf(link_score.universe, [.63, .7425, .9075, 1.00])
  
  #content_score.view()
  #link_score.view()
  #0.1667 - 6 parts; 0.041675 - 4 parts of 0.1667, 0.007-fallback
  relevant_score['very low'] = fuzz.trapmf(relevant_score.universe, [0.01, .04167, .125, .1674]) #.08335 0.125 
  relevant_score['low'] = fuzz.trapmf(relevant_score.universe, [.1667, .20837, .29171, .3341])   #0.25004 0.291715 
  relevant_score['med'] = fuzz.trapmf(relevant_score.universe, [.3334, .37505, .45839, .5008])   #.416714 .458389 
  relevant_score['good'] = fuzz.trapmf(relevant_score.universe, [.5001, .54178, .6255, .6675])   #.58345 .6251525
  relevant_score['very good'] = fuzz.trapmf(relevant_score.universe, [.6668, .70848, .791825, .8342]) #.75015 .791825
  relevant_score['excellent'] = fuzz.trapmf(relevant_score.universe, [.8335, .87517, .958525, 1.00])  #.91685 
  
  #relevant_score.view()

  #Define the fuzzy relationship between input and output variables:
  rule1 = ctrl.Rule(link_score['low'] & content_score['low'],relevant_score['very low'])
  rule2 = ctrl.Rule(link_score['low'] & content_score['med'],relevant_score['med'])
  rule3 = ctrl.Rule(link_score['low'] & content_score['high'],relevant_score['very good'])
  rule4 = ctrl.Rule(link_score['med'] & content_score['low'],relevant_score['low'])
  rule5 = ctrl.Rule(link_score['med'] & content_score['med'],relevant_score['good'])
  rule6 = ctrl.Rule(link_score['med'] & content_score['high'],relevant_score['very good'])
  rule7 = ctrl.Rule(link_score['high'] & content_score['low'],relevant_score['med'])
  rule8 = ctrl.Rule(link_score['high'] & content_score['med'],relevant_score['very good'])
  rule9 = ctrl.Rule(link_score['high'] & content_score['high'],relevant_score['excellent'])
  
  #Building the interference system:
  relevance_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9])
  #relevance_ctrl.view()
  
  relevance = ctrl.ControlSystemSimulation(relevance_ctrl)
  
  #Pass inputs to the system:
  relevance.input['content_score'] = content
  relevance.input['link_score'] = link
  
  #Run the fuzzy system: Computes based on the rules and MFs and defuzzifies.
  relevance.compute()

  #Viewing the Consequent again after computation shows the calculated system:
  relevant_score.view(sim=relevance)
  
  #return the relevant score of the element:
  return relevance.output['relevant_score']



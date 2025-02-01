# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 20:11:52 2024

@author: fawaz
"""

#%%
import numpy as np
import pandas as pd
import scipy as sp
import pandas as pd
#from google.colab import drive
#drive.mount('drive')
print("Cell Done")
#%%
class antenna_array:
  def __init__(self,m,n,dx,dy,f,alpha_max,antenna_array_number):
    self.m = m
    self.n = n
    self.dx = dx
    self.dy = dy
    self.f = f
    self.alpha_max = alpha_max
    self.antenna_array_number = antenna_array_number
    self.f = 5.8*(10**9)
    self.c = sp.constants.physical_constants["speed of light in vacuum"][0]
    self.k = (2*(np.pi)*(self.f))/(self.c)

    self.alpha_matrix = np.zeros((self.m,self.n))
    for m in range(self.m):
      for n in range(self.n):
        alpha = np.random.uniform(0,self.alpha_max)
        self.alpha_matrix[m][n] = alpha

    self.gamma_matrix = np.zeros((self.m,self.n))
    for m in range(self.m):
      for n in range(self.n):
        gamma = np.random.uniform(0,2*(np.pi))
        self.gamma_matrix[m][n] = gamma

    self.L_matrix = np.zeros((self.m,self.n))
    for m in range(self.m):
      for n in range(self.n):
        L = np.random.uniform(0,2*(np.pi))
        self.L_matrix[m][n] = L


  def calculate_phase_angle(self,e_theta_phi,phi,theta,r,alpha,gamma,phi_mn,L_mn,k,m,n,dx,dy):
    total_phase_angle = -k*r-phi_mn-L_mn+ k*((np.sin(theta)*np.cos(phi)*(m)*dx+np.sin(theta)*np.sin(phi)*(n)*dy)+(np.sin(theta)*np.cos(phi)*alpha*np.cos(gamma))+(np.sin(theta)*np.sin(phi)*alpha*np.sin(gamma)))
    total_phase_angle = (total_phase_angle)%(2*np.pi)
    return total_phase_angle

  def return_phase_angle(self,theta_phi_r_array):
    phase_data = {}
    e_theta_phi = 1
    phi_mn = 0
    total_phase_angle_data = {}
    total_phase_angle_data_df = {}
    for m in range(self.m):
      for n in range(self.n):

        total_phase_angle_data[str(m)+','+str(n)] = []
        for item in theta_phi_r_array:
          alpha = self.alpha_matrix[m][n]
          gamma = self.gamma_matrix[m][n]
          L_mn = self.L_matrix[m][n]
          total_phase_angle = np.degrees(self.calculate_phase_angle(e_theta_phi,np.radians(item[0]),np.radians(item[1]),item[2],alpha,gamma,phi_mn,L_mn,self.k,self.m,self.n,self.dx,self.dy))
          data_tuple = (item[0],item[1],total_phase_angle)
          total_phase_angle_data[str(m)+','+str(n)].append(data_tuple)
        print("total_phase_angle_data is: ",total_phase_angle_data)
        total_phase_angle_data_df[str(m)+','+str(n)] = pd.DataFrame(total_phase_angle_data[str(m)+','+str(n)],columns=('Phi[deg]','Theta[deg]','cang_deg(rEL3X)[deg]'))

    return total_phase_angle_data_df
    #return {'0,0':1,'0,1':1,'1,0':1,'1,1':1}

print("Cell Done")

#%% DRIVER CODE
c = sp.constants.physical_constants["speed of light in vacuum"][0]
f = 5.8*(10**9)
pi = np.pi
k = (2*pi*f)/c
r = 5
m=2
n=2
dx = 0.026
dy = 0.026
alpha_max = 0.004

total_arrays = 300

phi_min = -180
phi_max = 180
theta_min = 0
theta_max = 75
theta_phi_r_array = []

for theta in range(theta_min,theta_max+1):
  for phi in range(phi_min,phi_max+1):
    theta_phi_r_array.append([phi,theta,r])


file_counter = 1
for array in range(total_arrays):
  print("array Number is: ",array)
  antn_array = antenna_array(m,n,dx,dy,f,alpha_max,1)
  diction = antn_array.return_phase_angle(theta_phi_r_array)
  del antn_array
  # pdb.set_trace()
  #print(diction.keys())
  #print(diction)
  for m_ in range(m):
    for n_ in range(n):
      #print(diction[str(m)+','+str(n)])
      csv = diction[str(m_)+','+str(n_)]


      if file_counter<10:
          file_name = 'FileExports'+'/rEL3XPhase_'+'000'+str(file_counter)+'.csv'
      else:
          if file_counter<100:
              file_name = 'FileExports'+'/rEL3XPhase_'+'00'+str(file_counter)+'.csv'
          else:
              if file_counter<1000:
                  file_name = 'FileExports'+'/rEL3XPhase_'+'0'+str(file_counter)+'.csv'
              else:
                  file_name = 'FileExports'+'/rEL3XPhase_'+str(file_counter)+'.csv'

      csv.to_csv(file_name,index=False)
      file_counter+=1






print("Cell Done")
#%%
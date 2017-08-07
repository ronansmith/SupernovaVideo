import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('sn2017ahndata.csv', delimiter = ',', dtype = object)

filters = ['V', 'B', 'ip', 'gp', 'rp']
filter_counter = np.zeros(len(filters))
data_array = np.empty((int(np.shape(data)[0]), int(np.shape(data)[1]),len(filters)), dtype = object)

print(filters)
print(filter_counter)
print(data_array)

print(np.shape(data_array))

for i in range(len(filters)):
    j = 0
    for j in range(np.shape(data)[0]):
        if filters[i] == data[j,1]:
            if data[j,2][0] == 'K':
                data_array[filter_counter[i],:,i] = data[j,:]
                filter_counter[i] +=1            
        j +=1
    i +=1
    
print(data_array)

colors = ['red','blue','yellow','green','pink']
plt.figure()
for z in range(len(filters)):
    plt.scatter(data_array[:,0,z].astype(np.float) - 57788, data_array[:,4,z], color = colors[z], label = filters[z] + ' Band')
    z +=1
plt.legend(loc = 0, ncol = 3)
plt.show()

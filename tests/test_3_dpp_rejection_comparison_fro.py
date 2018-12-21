# This is a test for basic functions of this package:
## * Calculating the k-leverage scores 
## * Calculating the p_eff(theta) function
## * Plots of k-leverage scores and cumulative k-leverage scores




import sys
#sys.path.append('../')
sys.path.insert(0, '..')
from CSSPy.dataset_tools import *
#from CSSPy.visualization_tools import *
from CSSPy.derandomized_projection_dpp_sampler import *
from CSSPy.derandomized_volume_sampler import *
from CSSPy.volume_sampler import *
from CSSPy.optimized_projection_dpp_sampler import *
from CSSPy.projection_dpp_sampler import *
from CSSPy.uniform_sampler import *
from CSSPy.evaluation_functions import *
from CSSPy.experiments_tools import *
from CSSPy.k_means import *
from CSSPy.visualization_tools import *

import numpy as np
#import matplotlib.pyplot as plt
import timeit
import pandas as pd
from matplotlib import pyplot as plt
# This is a test for subsampling functions:
## * Projection DPPs
## * Volume sampling
## * Uniform sampling

# Import two datasets
dataset_name = "Basehock"
dataset_file = dataset_name+str("_X")
clustering_labels_file = dataset_name +str("_Y")
t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')
X_df = pd.read_csv('datasets/'+dataset_file+'.csv', sep=",", header=None)

#X_df = pd.read_csv('datasets/arcene_train.data', header=None, delimiter=' ', skip_blank_lines=True)
Y_df = pd.read_csv('datasets/'+clustering_labels_file+'.csv', sep=" ", header=None)

X_matrix = X_df.values


print(np.shape(X_matrix))
d = np.shape(X_matrix)[1]
N = np.shape(X_matrix)[0] -1


_,D,V = np.linalg.svd(X_matrix)

#U,D,V = svds(X_matrix, 61 , return_singular_vectors='true')


#k_means_test = k_means_using_column_subset(2,U[:,0:2])
#print("kmeans")
#print(k_means_test)
#print(evaluate_k_means_using_jaccard(list(Y_matrix[:,0]),list(k_means_test)))
#print(evaluate_k_means_using_jaccard(list(Y_matrix_2[:,0]),list(k_means_test)))

#print("finish kmeans")
k = 20
t_2 = timeit.default_timer()
#print(t_2-t_1)

V_k_ = calculate_right_eigenvectors_k_svd(X_matrix,k)
t_3 = timeit.default_timer()
print(t_3-t_2)
V_k = V_k_ #V[0:k,:]
#np.asarray(list(reversed(np.sort(lv_scores_vector))))


rank_X = np.shape(D)[0]
#print("classic bound for spe norm")
#print(np.sqrt((d-k)*k))
#print("new bound for spe norm")
#from  sys  import  path

#for d in sys.path:
#    print(d)

exp_number = 50
boosting_batch = 1

klv_test_1 = np.asarray(list(reversed(np.sort((np.diag(np.dot(np.transpose(V_k),V_k)))))))


plot_leverage_scores(klv_test_1,dataset_name,k)

plot_cumul_leverage_scores(klv_test_1,dataset_name,k)

#plt.boxplot([error_spe_list_uniform_sampling,error_spe_list_volume_sampling,error_spe_list_optimized_projection_DPP,error_spe_list_optimized_projection_DPP_with_rejection,error_spe_list_pivoted_qr], showfliers=False)
#plt.boxplot([error_spe_list_uniform_sampling,error_spe_list_volume_sampling,error_spe_list_optimized_projection_DPP,error_spe_list_optimized_projection_DPP_with_rejection,error_spe_list_pivoted_qr], showfliers=False)
#plt.boxplot([error_spe_list_uniform_sampling,error_spe_list_lvscores_sampling,error_spe_list_volume_sampling,error_spe_list_optimized_projection_DPP], showfliers=False)
  
#plt.boxplot([error_spe_list_uniform_sampling,error_spe_list_volume_sampling,error_spe_list_optimized_projection_DPP,error_spe_list_projection_DPP,error_spe_list_largest_lvs_sampling,error_spe_list_pivoted_qr_sampling,error_spe_list_derandomized_volume_sampling,error_spe_list_double_phase_sampling], showfliers=False)


def random_error_list_to_min_error_list(error_list):
    l_test = len(error_list)
    min_value_random_list = min(error_list)
    new_list = [min_value_random_list]*l_test
    return min_value_random_list


boosting_error_spe_aggregated_list = []


boosting_error_spe_volume_sampling_list = []
boosting_error_spe_projection_dpp_list = []
boosting_error_spe_effective_projection_dpp_list_1 = []
boosting_error_spe_effective_projection_dpp_list_2 = []
boosting_error_spe_effective_projection_dpp_list_3 = []
boosting_error_spe_effective_projection_dpp_list_4 = []

boosting_error_spe_largest_lvs_list = []

boosting_error_spe_double_phase_list = []


error_spe_aggregated_list = []
print("here we start")
for T_B in list(range(boosting_batch)):
    print ("Boosting step \n")
    print(T_B)
    print("\n")
    error_spe_aggregated_list = []
    ##plot_singular_values("matrix",X_matrix,dataset_name,k)
    ##plot_leverage_scores("vector",klv_test_1,dataset_name,k)
    ##plot_cumulative_leverage_scores("vector",klv_test_1,dataset_name,k)
    ##error_spe_list_derandomized_projection_dpp_sampling = launch_exp_derandomization_projection_dpp(X_matrix,dataset_name,k,exp_number) 

    error_spe_list_projection_DPP = launch_exp_projection_dpp(X_matrix,dataset_name,k,exp_number,"spectral")    
    error_spe_list_effective_projection_DPP_1 = launch_exp_effective_projection_dpp(X_matrix,dataset_name,k,exp_number,1.5,"spectral")    
    error_spe_list_effective_projection_DPP_2 = launch_exp_effective_projection_dpp(X_matrix,dataset_name,k,exp_number,2,"spectral")    
    error_spe_list_effective_projection_DPP_3 = launch_exp_effective_projection_dpp(X_matrix,dataset_name,k,exp_number,3,"spectral")    
    error_spe_list_effective_projection_DPP_4 = launch_exp_effective_projection_dpp(X_matrix,dataset_name,k,exp_number,5,"spectral")    

    error_spe_list_double_phase_sampling = launch_exp_double_phase_sampler(X_matrix,dataset_name,k,exp_number,"spectral") 

    error_spe_list_largest_lvs_sampling = launch_exp_largest_leveragescores_sampling(X_matrix,dataset_name,k,exp_number,"spectral") 
    
    error_spe_list_volume_sampling = launch_exp_volume_sampling(X_matrix,Y_matrix,dataset_name,k,exp_number,"spectral")    


    min_error_spe_list_volume_sampling = random_error_list_to_min_error_list(error_spe_list_volume_sampling)
    min_error_spe_list_projection_DPP = random_error_list_to_min_error_list(error_spe_list_projection_DPP)
    min_error_spe_list_effective_projection_DPP_1 = random_error_list_to_min_error_list(error_spe_list_effective_projection_DPP_1)
    min_error_spe_list_effective_projection_DPP_2 = random_error_list_to_min_error_list(error_spe_list_effective_projection_DPP_2)    
    min_error_spe_list_effective_projection_DPP_3 = random_error_list_to_min_error_list(error_spe_list_effective_projection_DPP_3)
    min_error_spe_list_effective_projection_DPP_4 = random_error_list_to_min_error_list(error_spe_list_effective_projection_DPP_4)
    min_error_spe_list_double_phase_sampling = random_error_list_to_min_error_list(error_spe_list_double_phase_sampling)

    
    min_error_spe_list_largest_lvs_sampling = random_error_list_to_min_error_list(error_spe_list_largest_lvs_sampling)

    #boosting_error_spe_aggregated_list.append(min_error_spe_list_uniform_sampling)
    boosting_error_spe_volume_sampling_list.append(min_error_spe_list_volume_sampling)
    boosting_error_spe_projection_dpp_list.append(min_error_spe_list_projection_DPP)
    boosting_error_spe_largest_lvs_list.append(min_error_spe_list_largest_lvs_sampling)
    boosting_error_spe_double_phase_list.append(min_error_spe_list_double_phase_sampling)
    boosting_error_spe_effective_projection_dpp_list_1.append(error_spe_list_effective_projection_DPP_1)
    boosting_error_spe_effective_projection_dpp_list_2.append(error_spe_list_effective_projection_DPP_2)
    boosting_error_spe_effective_projection_dpp_list_3.append(error_spe_list_effective_projection_DPP_3)
    boosting_error_spe_effective_projection_dpp_list_4.append(error_spe_list_effective_projection_DPP_4)
                
    #error_spe_aggregated_list.append(error_spe_list_uniform_sampling)
    error_spe_aggregated_list.append(error_spe_list_volume_sampling)
    error_spe_aggregated_list.append(error_spe_list_projection_DPP)
    error_spe_aggregated_list.append(error_spe_list_effective_projection_DPP_1)
    error_spe_aggregated_list.append(error_spe_list_effective_projection_DPP_2)
    error_spe_aggregated_list.append(error_spe_list_effective_projection_DPP_3)
    error_spe_aggregated_list.append(error_spe_list_effective_projection_DPP_4)
    error_spe_aggregated_list.append(error_spe_list_largest_lvs_sampling)
    error_spe_aggregated_list.append(error_spe_list_double_phase_sampling)


boosting_error_spe_aggregated_list.append(boosting_error_spe_volume_sampling_list)
boosting_error_spe_aggregated_list.append(boosting_error_spe_projection_dpp_list)
boosting_error_spe_aggregated_list.append(boosting_error_spe_effective_projection_dpp_list_1)
boosting_error_spe_aggregated_list.append(boosting_error_spe_effective_projection_dpp_list_2)
boosting_error_spe_aggregated_list.append(boosting_error_spe_effective_projection_dpp_list_3)
boosting_error_spe_aggregated_list.append(boosting_error_spe_effective_projection_dpp_list_4)
boosting_error_spe_aggregated_list.append(boosting_error_spe_largest_lvs_list)
boosting_error_spe_aggregated_list.append(boosting_error_spe_double_phase_list)



plot_leverage_scores(klv_test_1,dataset_name,k)

plot_cumul_leverage_scores(klv_test_1,dataset_name,k)

plt.figure(figsize=(24, 6)) 
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
ax = plt.subplot(111) 
#plt.setp(bp['means'], color='red')
box1 =plt.boxplot(error_spe_aggregated_list, showfliers=False)
plt.setp(box1['medians'], color='red', linewidth=3)

#plt.boxplot([error_spe_list_uniform_sampling,error_spe_list_volume_sampling,error_spe_list_optimized_projection_DPP], showfliers=False)

plt.ylabel(r'$\mathrm{\|\| X- \pi_{C} X \|\| _{2}}$', fontsize=16)
 
#plt.legend(bbox_to_anchor=(1.04,1), loc="bottomleft", inset=.02, ["Volume Sampling","Projection DPP"])
#plt.legend("bottomleft", inset=.02, c("Volume Sampling","Projection DPP"), fill=topo.colors(3), horiz=TRUE, cex=0.8)
#plt.gca().xaxis.set_ticklabels(["Uniform Sampling","LVScores Sampling","Volume Sampling","Projection DPP"])

#plt.gca().xaxis.set_ticklabels(["Uniform Sampling","Volume Sampling","Optimized Projection DPP","Projection DPP","Largest lvs","Pivoted QR","derandomized_volume_sampling","Double Phase"])

plt.gca().xaxis.set_ticklabels(["Volume S.","Projection DPP","E Projection DPP 1","E Projection DPP 2","E Projection DPP 3","E Projection DPP 4","Largest lvs","Double Phase"])

#figfile_name= dataset_name+"_allalgos_"+str(exp_number)+"samples_k_"+str(k)+".pdf"
#plt.savefig(figfile_name)

plt.show()
#
#
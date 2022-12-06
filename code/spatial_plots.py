""" This file will generate the spatial plots of stimulus and response on the foot

"""

# import relavant packages
import footsim as fs
import holoviews as hv
import pickle as pk
from footsim.plotting import plot, figsave

# read in processed data
f = open('/Users/lukecleland/Desktop/Figure 7 stuff/additional/step_data.pk','rb')
dictionary = pk.load(f)
f.close()

# define variables based on dictionary keys
s_one = dictionary['Normal']['Step 1']['Stimulus']
r_one = dictionary['Normal']['Step 1']['Response']
s_two = dictionary['Normal']['Step 2']['Stimulus']
r_two = dictionary['Normal']['Step 2']['Response']
s_three = dictionary['Normal']['Step 3']['Stimulus']
r_three = dictionary['Normal']['Step 3']['Response']
s_jogging = dictionary['Jogging']['Stimulus']
r_jogging = dictionary['Jogging']['Response']

# define output path
path = '../figures/'

## JOGGING
hvobj_jogging = plot() * plot(s_jogging,spatial=True,bin=25) + plot() * plot(r_jogging,spatial=True,bin=25,scaling_factor=.75)

output_path = path + 'jogging '

figsave(hvobj_jogging[1][67],output_path + 'response bin 67',fmt='png', dpi=100)
figsave(hvobj_jogging[1][77],output_path + 'response bin 77',fmt='png', dpi=100)
figsave(hvobj_jogging[1][87],output_path + 'response bin 87',fmt='png', dpi=100)

figsave(hvobj_jogging[0][66],output_path + 'stimulation bin 67',fmt='png', dpi=100)
figsave(hvobj_jogging[0][76],output_path + 'stimulation bin 77',fmt='png', dpi=100)
figsave(hvobj_jogging[0][86],output_path + 'stimulation bin 87',fmt='png', dpi=100)



## NORMAL 1

hvobj_normal_one = plot() * plot(s_one,spatial=True,bin=25) + plot() * plot(r_one,spatial=True,bin=25,scaling_factor=.75)

output_path = path + 'normal 1 '

figsave(hvobj_normal_one[1][67],output_path + 'response bin 67',fmt='png', dpi=100)
figsave(hvobj_normal_one[1][77],output_path + 'response bin 77',fmt='png', dpi=100)
figsave(hvobj_normal_one[1][87],output_path + 'response bin 87',fmt='png', dpi=100)

figsave(hvobj_normal_one[0][66],output_path + 'stimulation bin 67',fmt='png', dpi=100)
figsave(hvobj_normal_one[0][76],output_path + 'stimulation bin 77',fmt='png', dpi=100)
figsave(hvobj_normal_one[0][86],output_path + 'stimulation bin 87',fmt='png', dpi=100)


## NORMAL 2

hvobj_normal_two = plot() * plot(s_two,spatial=True,bin=25) + plot() * plot(r_two,spatial=True,bin=25,scaling_factor=.75)

output_path = path + 'normal 2 '

figsave(hvobj_normal_two[1][67],output_path + 'response bin 67',fmt='png', dpi=100)
figsave(hvobj_normal_two[1][77],output_path + 'response bin 77',fmt='png', dpi=100)
figsave(hvobj_normal_two[1][87],output_path + 'response bin 87',fmt='png', dpi=100)

figsave(hvobj_normal_two[0][66],output_path + 'stimulation bin 67',fmt='png', dpi=100)
figsave(hvobj_normal_two[0][76],output_path + 'stimulation bin 77',fmt='png', dpi=100)
figsave(hvobj_normal_two[0][86],output_path + 'stimulation bin 87',fmt='png', dpi=100)


## NORMAL 3
hvobj_normal_three = plot() * plot(s_three,spatial=True,bin=25) + plot() * plot(r_three,spatial=True,bin=25,scaling_factor=.75)

output_path = path + 'normal 3 '

figsave(hvobj_normal_three[1][67],output_path + 'response bin 67',fmt='png', dpi=100)
figsave(hvobj_normal_three[1][77],output_path + 'response bin 77',fmt='png', dpi=100)
figsave(hvobj_normal_three[1][87],output_path + 'response bin 87',fmt='png', dpi=100)

figsave(hvobj_normal_three[0][66],output_path + 'stimulation bin 67',fmt='png', dpi=100)
figsave(hvobj_normal_three[0][76],output_path + 'stimulation bin 77',fmt='png', dpi=100)
figsave(hvobj_normal_three[0][86],output_path + 'stimulation bin 87',fmt='png', dpi=100)
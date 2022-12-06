# import relevant packages
import footsim as fs
from insole.insole import *
from footsim.plotting import plot,figsave
import holoviews as hv
import pickle as pk
import bz2
import _pickle as cPickle
import matplotlib.ticker as mtick
from functions import *

# read in processed data
f = open('../processed_data/response_dict.pkl','rb')
response_dict = pk.load(f)
f.close()

# import afferent population
a = response_dict['a']


# generate dictionary containing foot regions grouped to 4 coarse regions of the foot
regions_dict = {'heel': ['HR', 'HL'],
               'arch': ['AMe', 'AMi', 'ALa'],
               'mets': ['MLa','MMe','MMi'],
               'toes': ['T1', 'T2_t','T3_t','T4_t','T5_t']}

# define output path
output_path = '../figures/'




# ## Normal walking
# load in participant data
normal_data = bz2.BZ2File('/Users/lukecleland/Documents/PhD/Research projects/Project insole/project_insole/preprocessed_data/PPT_013/trial07/left/left data.pbz2', 'rb')
normal_data = cPickle.load(normal_data)

# extract raw data
raw_data = normal_data['Raw data']
under_threshold, step_start, index_differences, total_pressure = check4steps(raw_data)

# identify stomp in pressure data
stomp = int(stomp_detection_pressure(normal_data['Total pressure']))

# identify turns
segmentaion_file_path = '/Users/lukecleland/Documents/PhD/Research projects/Project insole/project_insole/raw_data/IMU/Raw data/PPT_013/trial07/Segmentation times.csv'
gryo_data_filename = '/Users/lukecleland/Documents/PhD/Research projects/Project insole/project_insole/raw_data/IMU/Raw data/PPT_013/trial07/left_foot_accel.csv'
turn_idxs = find_turning_idxs(segmentaion_file_path, gryo_data_filename)
turn_idxs = (turn_idxs) + stomp

# normalize to 100 timepoints
all_steps, total_step_frame = average_after_exclusions(raw_data, 'left', step_start, under_threshold, index_differences, turn_idxs)
all_steps_new, total_step_frame_new = normalize_step_length_given_longest(all_steps, total_step_frame)

# to generate a slightly different step
for_step_three = total_step_frame_new
for_step_three_all = all_steps_new

# remove steps that are now zero following removal of turns
remove = []
for q in range(total_step_frame_new.shape[0]):
    if np.sum(total_step_frame_new[q, :, :, :]) == 0.0:
        remove.append(q)
total_step_frame_new = np.delete(total_step_frame_new, remove,
                             axis=0)



# # including turns

all_steps_turns, total_step_frame_turns = average_to_single_step(raw_data, 'left', step_start, under_threshold, index_differences)
all_steps_turns_new, total_step_frame_turns_new = normalize_step_length_given_longest(all_steps_turns, total_step_frame_turns)



### Get steps
step_one = np.moveaxis(total_step_frame_new[10], 0, 2)
step_two = np.moveaxis(total_step_frame_new[-3], 0, 2)
step_three = np.moveaxis(total_step_frame_turns_new[12], 0, 2)


# #### Step 1

path = output_path + "normal_walking_step_one"

# concat 2 steps together
step_one_add_end = np.zeros((step_one.shape[0], step_one.shape[1], 2))
step_one = np.append(step_one_add_end, step_one, axis=2)
step_one_ = np.append(step_one, np.zeros((step_one.shape[0], step_one.shape[1], 50)), axis=2)
step_one = np.append(step_one_, step_one, axis=2)

# smooth the pressure profile
s_one, r_one, total_one = one_step_total_pressure_response_all_frames_smooth(step_one, a, frames=100, output_path=path)

# plot step with population response across whole foot
path = output_path + "normal_walking_step_one_single_panel"
revised_plots(total_one, r_one, a, path, hz_lim=8, pres_lim=100000)


# generate response
s_one, regions_one, reshaped_data_one, idxs_one, D_one = map2footsim(step_one)
r_one = a.response(s_one)


# #### Big toe
path = output_path + "normal_walking_step_one_single_panel_"
region_plots(r_one, a, s_one, reshaped_data_one, regions_one, path, 'T1', hz_lim=8, pres_lim=6000)


# #### Middle metatarsal
path = output_path + "normal_walking_step_one_single_panel_"
region_plots(r_one, a, s_one, reshaped_data_one, regions_one, path, 'MMi', hz_lim=12, pres_lim=60000)


# #### Lateral arch
path = output_path + "normal_walking_step_one_single_panel_"
region_plots(r_one, a, s_one, reshaped_data_one, regions_one, path, 'ALa', hz_lim=6, pres_lim=8000)


# ####Heel
path = output_path + "normal_walking_step_one_single_panel_"
region_plots(r_one, a, s_one, reshaped_data_one, regions_one, path, 'heel', hz_lim=12, pres_lim=30000)


### REPEAT FOR STEP 2
# #### Step 2
path = output_path + "normal_walking_step_two"

# repeat for step 2
step_two_add_end = np.zeros((step_two.shape[0], step_two.shape[1], 2))
step_two = np.append(step_two_add_end, step_two, axis=2)
step_two_ = np.append(step_two, np.zeros((step_two.shape[0], step_two.shape[1], 50)), axis=2)
step_two = np.append(step_two_, step_two, axis=2)


s_two, r_two, total_two = one_step_total_pressure_response_all_frames_smooth(step_two, a, frames=100, output_path=path)

s_two, regions_two, reshaped_data_two, idxs_two, D_two = map2footsim(step_two)
r_two = a.response(s_two)

path = output_path + "normal_walking_step_two_single_panel"
revised_plots(total_two, r_two, a, path, hz_lim=8, pres_lim=100000)


# #### Big toe
path = output_path + "normal_walking_step_two_single_panel_"
#region_plots(step_two, r_two, a, 'T1', path, 6, 300)
region_plots(r_two, a, s_two, reshaped_data_two, regions_two, path, 'T1', hz_lim=8, pres_lim=6000)


# #### Middle metatarsal
path = output_path + "normal_walking_step_two_single_panel_"
region_plots(r_two, a, s_two, reshaped_data_two, regions_two, path, 'MMi', hz_lim=12, pres_lim=60000)


# #### Lateral arch
path = output_path + "normal_walking_step_two_single_panel_"
region_plots(step_two, r_two, a, 'ALa', path, 6, 10000)
region_plots(r_two, a, s_two, reshaped_data_two, regions_two, path, 'ALa', hz_lim=6, pres_lim=8000)


# #### Heel
path = output_path + "normal_walking_step_two_single_panel_"
region_plots(r_two, a, s_two, reshaped_data_two, regions_two, path, 'heel', hz_lim=12, pres_lim=30000)


### REPEAT FOR STEP 3
# # Normal step 3
path = output_path + "normal_walking_step_three"

step_three_add_end = np.zeros((step_three.shape[0], step_three.shape[1], 2))
step_three = np.append(step_three_add_end, step_three, axis=2)
step_three_ = np.append(step_three, np.zeros((step_three.shape[0], step_three.shape[1], 50)), axis=2)
step_three = np.append(step_three_, step_three, axis=2)

s_three, r_three, total_three = one_step_total_pressure_response_all_frames_smooth(step_three, a, frames=100, output_path=path)

s_three, regions_three, reshaped_data_three, idxs_three, D_three = map2footsim(step_three)
r_three = a.response(s_three)

path = output_path + "normal_walking_step_three_single_panel"
revised_plots(total_three, r_three, a, path, hz_lim=8, pres_lim=100000)


# ### Big toe
path = output_path + "normal_walking_step_three_single_panel_"
region_plots(r_three, a, s_three, reshaped_data_three, regions_three, path, 'T1', hz_lim=8, pres_lim=6000)


# ### Middle metatarsal
path = output_path + "normal_walking_step_three_single_panel_"
region_plots(r_three, a, s_three, reshaped_data_three, regions_three, path, 'MMi', hz_lim=12, pres_lim=60000)


# ### Lateral arch
path = output_path + "normal_walking_step_three_single_panel_"
region_plots(r_three, a, s_three, reshaped_data_three, regions_three, path, 'ALa', hz_lim=6, pres_lim=8000)


# ### Heel
path = output_path + "normal_walking_step_three_single_panel_"
region_plots(r_three, a, s_three, reshaped_data_three, regions_three, path, 'heel', hz_lim=12, pres_lim=30000)


# ## REPEAT FOR A SINGLE STEP DURING JOGGING

running_data = bz2.BZ2File('/Users/lukecleland/Documents/PhD/Research projects/Project insole/project_insole/preprocessed_data/PPT_013/trial15/left/left data.pbz2', 'rb')
running_data = cPickle.load(running_data)

running_raw_data = running_data['Raw data']
running_under_threshold, running_step_start, running_index_differences, running_total_pressure = check4steps(running_raw_data)

running_stomp = int(stomp_detection_pressure(running_data['Total pressure']))

running_segmentaion_file_path = '/Users/lukecleland/Documents/PhD/Research projects/Project insole/Data analysis/IMU data analysis/Raw data/PPT_013/trial15/Segmentation times.csv'
running_gryo_data_filename = '/Users/lukecleland/Documents/PhD/Research projects/Project insole/Data analysis/IMU data analysis/Raw data/PPT_013/trial15/left_foot_accel.csv'
running_turn_idxs = find_turning_idxs(running_segmentaion_file_path, running_gryo_data_filename)
running_turn_idxs = (running_turn_idxs) + running_stomp

running_all_steps, running_total_step_frame = average_after_exclusions(running_raw_data, \
                                    'left', running_step_start, running_under_threshold, \
                                                                       running_index_differences, running_turn_idxs)


running_all_steps = np.delete(running_all_steps, running_remove,
                             axis=0)

running_all_steps_new, running_total_step_frame_new = normalize_step_length_given_longest(running_all_steps, running_total_step_frame)

# remove steps that are now zero
running_remove = []
for q in range(running_total_step_frame_new.shape[0]):
    if np.sum(running_total_step_frame_new[q, :, :, :]) == 0.0:
        running_remove.append(q)
running_total_step_frame_new = np.delete(running_total_step_frame_new, running_remove,
                             axis=0)

running_step_one = np.moveaxis(running_total_step_frame_new[3], 0, 2)


path = output_path + "jogging_step_one"


running_step_one_add_end = np.zeros((running_step_one.shape[0], running_step_one.shape[1], 2))
running_step_one = np.append(running_step_one_add_end, running_step_one, axis=2)
running_step_one_ = np.append(running_step_one, np.zeros((running_step_one.shape[0], running_step_one.shape[1], 50)), axis=2)
running_step_one = np.append(running_step_one_, running_step_one, axis=2)

s_jogging, r_jogging, total_jogging = one_step_total_pressure_response_all_frames_smooth(running_step_one, a, frames=100, output_path=path)

s_jogging, regions_jogging, reshaped_data_jogging, idxs_jogging, D_jogging = map2footsim(running_step_one)
r_jogging = a.response(s_jogging)


path = output_path + "jogging_step_one_single_panel"
revised_plots(total_jogging, r_jogging, a, path, hz_lim=8, pres_lim=100000)


# #### Big toe
path = output_path + "jogging_step_one_single_panel_"
region_plots(r_jogging, a, s_jogging, reshaped_data_jogging, regions_jogging, path, 'T1', hz_lim=8, pres_lim=6000)


# #### Middle metatarsal
path = output_path + "jogging_step_one_single_panel_"
region_plots(r_jogging, a, s_jogging, reshaped_data_jogging, regions_jogging, path, 'MMi', hz_lim=12, pres_lim=60000)


# #### Lateral arch
path = output_path + "jogging_step_one_single_panel_"
region_plots(r_jogging, a, s_jogging, reshaped_data_jogging, regions_jogging, path, 'ALa', hz_lim=6, pres_lim=8000)


# #### Heel
path = output_path + "jogging_step_one_single_panel_"
region_plots(r_jogging, a, s_jogging, reshaped_data_jogging, regions_jogging, path, 'heel', hz_lim=12, pres_lim=30000)




# save dictionary will raw data, FootSim stimulus and response objects per step
dictionary = {'Normal': {'Step 1': {'Pressure': step_one,
                                    'Stimulus': s_one,
                                    'Response': r_one,
                                   'Reshaped': reshaped_data_one,
                                   'Regions': regions_one},
                         'Step 2': {'Pressure': step_two,
                                    'Stimulus': s_two,
                                    'Response': r_two,
                                   'Reshaped': reshaped_data_two,
                                   'Regions': regions_one},
                         'Step 3': {'Pressure': step_three,
                                    'Stimulus': s_three,
                                    'Response': r_three,
                                   'Reshaped': reshaped_data_three,
                                   'Regions': regions_one}},
             'Jogging' : {'Pressure': running_step_one,
                          'Stimulus': s_jogging,
                          'Response': r_jogging,
                                   'Reshaped': reshaped_data_jogging,
                                   'Regions': regions_one},
             'a': a}

pk.dump(dictionary, open("../processed_data/step_data.pk", "wb"))





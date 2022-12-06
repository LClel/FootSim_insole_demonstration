def stomp_detection_pressure(total_pressure):
    """ Identifies the point in time that the foot was stomped - first peak in the data.
    The is used to sync the pressure insole data to the IMU data.

    :param total_pressure:
    :param args:
    :return:
    """

    peaks, _ = find_peaks(total_pressure, height=5000, distance=100)

    return peaks[0]


def find_turning_idxs(segmentaion_file_path, gryo_data_filename):
    """

    :param segmentaion_file_path:
    :param gryo_data_filename:
    :return:
    """

    # read in segementation times
    segmentation_times = np.asarray(pd.read_csv(segmentaion_file_path, header=None)).T[0]

    IMU_data = np.asarray(pd.read_csv(gryo_data_filename)).T

    IMU_stomp = read_left_foot_accel_csv(gryo_data_filename)

    segmentation_times = segmentation_times - IMU_stomp

    # find maximum difference in turn segmentation times
    differences = []
    for i in range(int(len(segmentation_times) / 2)):
        differences.append(segmentation_times[(i * 2) + 1] - segmentation_times[i * 2])

    turn_idxs = np.zeros(((int(len(segmentation_times) / 2)), np.max(differences)))
    for i in range(int(len(segmentation_times) / 2)):
        idxs = np.arange(segmentation_times[i * 2], [segmentation_times[(i * 2) + 1]])

        turn_idxs[i, :len(idxs)] = idxs

    return turn_idxs


def total_pressure_response_all_frames_smooth(D, a, frames, output_path):
    """

    :param D:
    :param a:
    :param frames:
    :param output_path:
    :return:
    """
    # calculate stimulus and indentation
    s, regions, reshaped_data, idxs, D = map2footsim(D)

    r = a.response(s)

    under_threshold, step_start, index_differences, total_pressure = check4steps(D, frames=frames)

    # plot total pressure per frame with afferent responses

    x = list(range(D.shape[2]))
    total_Spline = scipy.interpolate.make_interp_spline(x, total_pressure)
    X_ = np.linspace(min(x), max(x), D.shape[2] * 5)
    total_ = total_Spline(X_)
    total_[total_ < 0] = 0

    FA1 = np.mean(r[a['FA1']].psth(25), axis=0)
    FA2 = np.mean(r[a['FA2']].psth(25), axis=0)
    SA1 = np.mean(r[a['SA1']].psth(25), axis=0)
    SA2 = np.mean(r[a['SA2']].psth(25), axis=0)

    x_ = list(range(len(FA1)))
    FA1_Spline = scipy.interpolate.make_interp_spline(x_, FA1)
    X_ = np.linspace(min(x_), max(x_), len(FA1) * 5)
    FA1_ = FA1_Spline(X_)
    FA1_[FA1_ < 0] = 0

    FA2_Spline = scipy.interpolate.make_interp_spline(x_, FA2)
    X_ = np.linspace(min(x_), max(x_), len(FA2) * 5)
    FA2_ = FA2_Spline(X_)
    FA2_[FA2_ < 0] = 0

    SA1_Spline = scipy.interpolate.make_interp_spline(x_, SA1)
    X_ = np.linspace(min(x_), max(x_), len(SA1) * 5)
    SA1_ = SA1_Spline(X_)
    SA1_[SA1_ < 0] = 0

    SA2_Spline = scipy.interpolate.make_interp_spline(x_, SA2)
    X_ = np.linspace(min(x_), max(x_), len(SA2) * 5)
    SA2_ = SA2_Spline(X_)
    SA2_[SA2_ < 0] = 0

    plt.figure(figsize=(15, 10), dpi=600)

    plt.subplot(2, 1, 1)
    plt.plot(total_)
    plt.title('Total pressure', fontsize=18)  # , fontweight="bold")
    plt.ylabel('Pressure (kPa)', fontsize=18)  # ,fontweight="bold")
    plt.xticks([])
    plt.yticks(fontsize=12)
    # plt.xlim(0,D.shape[2])
    plt.xlim(0, len(total_))
    plt.ylim(0, 35000)
    # plt.ylim(-1, 50)

    # plt.figure()
    ax = plt.subplot(2, 1, 2)
    plt.plot(SA1_[int(505 * .6):], color=fs.constants.affcol['SA1'], label='SA1')
    plt.plot(FA1_[int(505 * .6):], color=fs.constants.affcol['FA1'], label='FA1')
    plt.plot(FA2_[int(505 * .6):], color=fs.constants.affcol['FA2'], label='FA2')
    plt.plot(SA2_[int(505 * .6):], color=fs.constants.affcol['SA2'], label='SA2')
    plt.title('Tactile population responses', fontsize=18)  # , fontweight="bold")
    plt.ylabel('Firing rate (Hz)', fontsize=18)  # , fontweight="bold")
    plt.xlabel('Step progress (%)', fontsize=18)  # , fontweight="bold")
    # plt.xticks([])
    plt.yticks(fontsize=12)
    plt.xlim(0, len(FA1_))
    plt.ylim(0, 6.)
    # print(len(FA1_))
    # print(len(SA1_))
    # print(len(FA2_))
    # print(len(SA2_))

    # plt.axvspan(307.5,410,color='lightgrey')
    # plt.axvspan(1435,1537.5,color='lightgrey')
    # plt.axvspan(2665,2767,color='lightgrey')

    # locs, labels = plt.xticks()
    # diff = 4100
    # print(diff)
    # quarter = np.min(locs) + diff * .25
    # half = np.min(locs) + diff * .5
    # three_quarter = np.min(locs) + diff * .75

    # ticks = [quarter, half, three_quarter]
    # plt.xticks(ticks, labels=[25, 50, 75], fontsize=12)

    plt.legend(fontsize=12, loc='upper right')
    # plt.savefig(output_path + "/Pressure and response all frames all afferents.png", format='png', dpi=600)

    return s, r, total_


def revised_plots(total_, r, a, output_path, **args):
    hz_lim = args.get('hz_lim', 15)
    pres_lim = args.get('pres_lim', 75000)

    FA1 = np.mean(r[a['FA1']].psth(25), axis=0)
    FA2 = np.mean(r[a['FA2']].psth(25), axis=0)
    SA1 = np.mean(r[a['SA1']].psth(25), axis=0)
    SA2 = np.mean(r[a['SA2']].psth(25), axis=0)

    x_ = list(range(len(FA1)))
    FA1_Spline = scipy.interpolate.make_interp_spline(x_, FA1)
    X_ = np.linspace(min(x_), max(x_), len(FA1) * 5)
    FA1_ = FA1_Spline(X_)
    FA1_[FA1_ < 0] = 0

    FA2_Spline = scipy.interpolate.make_interp_spline(x_, FA2)
    X_ = np.linspace(min(x_), max(x_), len(FA2) * 5)
    FA2_ = FA2_Spline(X_)
    FA2_[FA2_ < 0] = 0

    SA1_Spline = scipy.interpolate.make_interp_spline(x_, SA1)
    X_ = np.linspace(min(x_), max(x_), len(SA1) * 5)
    SA1_ = SA1_Spline(X_)
    SA1_[SA1_ < 0] = 0

    SA2_Spline = scipy.interpolate.make_interp_spline(x_, SA2)
    X_ = np.linspace(min(x_), max(x_), len(SA2) * 5)
    SA2_ = SA2_Spline(X_)
    SA2_[SA2_ < 0] = 0

    fig = plt.figure(figsize=(8, 4), dpi=600)
    ax = fig.add_subplot(111, label="1")
    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    ax2.plot(FA1_, color=fs.constants.affcol['FA1'], label='FA1')
    ax2.plot(FA2_, color=fs.constants.affcol['FA2'], label='FA2')
    ax2.plot(SA1_, color=fs.constants.affcol['SA1'], label='SA1')
    ax2.plot(SA2_, color=fs.constants.affcol['SA2'], label='SA2')
    ax2.set_xlabel("Step progress (%)", color="black")
    ax2.set_ylabel("Firing rate (Hz)", color="black")
    ax2.tick_params(axis='x', colors="black")
    ax2.tick_params(axis='y', colors="black")
    ax2.set_xlim(len(FA1_) * .59, len(FA1_) * .99)
    ax2.set_ylim(0, hz_lim)

    ax.axvspan(835.841584, 848.3168316, color='pink')

    ax.axvspan(960.5940594, 973.063069, color='cyan')

    ax.axvspan(1085.346354, 1097.82178217, color='lightgreen')

    locs = ax.get_xticks()
    print(locs)
    diff = 508.0
    print(diff)
    quarter = np.min(locs) + diff * .25
    half = np.min(locs) + diff * .5
    three_quarter = np.min(locs) + diff * .75

    ticks = [quarter, half, three_quarter]
    ax.set_xticks(ticks)
    ax.set_xticklabels(['25', '50', '75'])

    ax.plot(total_, color="black")
    ax.xaxis.tick_top()
    ax.yaxis.tick_right()
    # ax.set_xlabel('x label 2', color="C1") 
    ax.set_ylabel('Total pressure', color="black")
    ax.xaxis.set_label_position('top')
    ax.yaxis.set_label_position('right')
    ax.tick_params(axis='x', colors="black")
    ax.set_xticks([])
    ax.tick_params(axis='y', colors="black")
    ax.set_xlim(len(total_) * .59, len(total_) * .99)
    ax.set_ylim(0, pres_lim)

    plt.savefig(output_path + ".png", format='png', dpi=100)


def region_plots(r, a, s, reshaped_data, regions, output_path, region_to_plot, **args):
    """ Region called is either:
    T1: great toe
    MMi: Middle metatarsal
    MMe: medial metatarsal
    ALa: lateral arch
    AMe: medial arch
    Any other input for region will be taken as the heel
    """

    hz_lim = args.get('hz_lim', 15)
    pres_lim = args.get('pres_lim', 40000)

    foot = 'left'
    participant = ''
    av_pressure_per_region, contact_percentage_per_region, total_pressure_per_region = average_pressure_per_region(
        reshaped_data, regions, foot, participant)
    pressure_per_region = total_pressure_per_region

    if region_to_plot == 'T1':
        FA1 = np.mean(r[a['T1']['FA1']].psth(25), axis=0)
        FA2 = np.mean(r[a['T1']['FA2']].psth(25), axis=0)
        SA1 = np.mean(r[a['T1']['SA1']].psth(25), axis=0)
        SA2 = np.mean(r[a['T1']['SA2']].psth(25), axis=0)

        total_pressure = pressure_per_region['T1'].T

    elif region_to_plot == 'MMi':
        FA1 = np.mean(r[a['MMi']['FA1']].psth(25), axis=0)
        FA2 = np.mean(r[a['MMi']['FA2']].psth(25), axis=0)
        SA1 = np.mean(r[a['MMi']['SA1']].psth(25), axis=0)
        SA2 = np.mean(r[a['MMi']['SA2']].psth(25), axis=0)

        total_pressure = pressure_per_region['MMi'].T

    elif region_to_plot == 'MMe':
        FA1 = np.mean(r[a['MMe']['FA1']].psth(25), axis=0)
        FA2 = np.mean(r[a['MMe']['FA2']].psth(25), axis=0)
        SA1 = np.mean(r[a['MMe']['SA1']].psth(25), axis=0)
        SA2 = np.mean(r[a['MMe']['SA2']].psth(25), axis=0)

        total_pressure = pressure_per_region['MMe'].T


    elif region_to_plot == 'ALa':
        FA1 = np.mean(r[a['ALa']['FA1']].psth(25), axis=0)
        FA2 = np.mean(r[a['ALa']['FA2']].psth(25), axis=0)
        SA1 = np.mean(r[a['ALa']['SA1']].psth(25), axis=0)
        SA2 = np.mean(r[a['ALa']['SA2']].psth(25), axis=0)

        total_pressure = pressure_per_region['ALa'].T

    elif region_to_plot == 'AMe':
        FA1 = np.mean(r[a['AMe']['FA1']].psth(25), axis=0)
        FA2 = np.mean(r[a['AMe']['FA2']].psth(25), axis=0)
        SA1 = np.mean(r[a['AMe']['SA1']].psth(25), axis=0)
        SA2 = np.mean(r[a['AMe']['SA2']].psth(25), axis=0)

        total_pressure = pressure_per_region['AMe'].T


    else:
        HL_FA1 = np.mean(r[a['HL']['FA1']].psth(25), axis=0)
        HL_FA2 = np.mean(r[a['HL']['FA2']].psth(25), axis=0)
        HL_SA1 = np.mean(r[a['HL']['SA1']].psth(25), axis=0)
        HL_SA2 = np.mean(r[a['HL']['SA2']].psth(25), axis=0)

        HR_FA1 = np.mean(r[a['HR']['FA1']].psth(25), axis=0)
        HR_FA2 = np.mean(r[a['HR']['FA2']].psth(25), axis=0)
        HR_SA1 = np.mean(r[a['HR']['SA1']].psth(25), axis=0)
        HR_SA2 = np.mean(r[a['HR']['SA2']].psth(25), axis=0)

        FA1 = (HL_FA1 + HR_FA1) / 2
        FA2 = (HL_FA2 + HR_FA2) / 2
        SA1 = (HL_SA1 + HR_SA1) / 2
        SA2 = (HL_SA2 + HR_SA2) / 2

        pressure_HL = pressure_per_region['HL']
        pressure_HR = pressure_per_region['HR']
        total_pressure = np.sum(pressure_HL + pressure_HR, axis=0)

    x = list(range(len(total_pressure)))
    total_Spline = scipy.interpolate.make_interp_spline(x, total_pressure)
    X_ = np.linspace(min(x), max(x), len(total_pressure) * 5)
    total_ = total_Spline(X_)
    total_[total_ < 0] = 0

    x_ = list(range(len(FA1)))
    FA1_Spline = scipy.interpolate.make_interp_spline(x_, FA1)
    X_ = np.linspace(min(x_), max(x_), len(FA1) * 5)
    FA1_ = FA1_Spline(X_)
    FA1_[FA1_ < 0] = 0

    FA2_Spline = scipy.interpolate.make_interp_spline(x_, FA2)
    X_ = np.linspace(min(x_), max(x_), len(FA2) * 5)
    FA2_ = FA2_Spline(X_)
    FA2_[FA2_ < 0] = 0

    SA1_Spline = scipy.interpolate.make_interp_spline(x_, SA1)
    X_ = np.linspace(min(x_), max(x_), len(SA1) * 5)
    SA1_ = SA1_Spline(X_)
    SA1_[SA1_ < 0] = 0

    SA2_Spline = scipy.interpolate.make_interp_spline(x_, SA2)
    X_ = np.linspace(min(x_), max(x_), len(SA2) * 5)
    SA2_ = SA2_Spline(X_)
    SA2_[SA2_ < 0] = 0

    fig = plt.figure(figsize=(8, 4), dpi=600)
    ax = fig.add_subplot(111, label="1")
    ax2 = fig.add_subplot(111, label="2", frame_on=False)

    ax2.plot(FA1_, color=fs.constants.affcol['FA1'], label='FA1')
    ax2.plot(FA2_, color=fs.constants.affcol['FA2'], label='FA2')
    ax2.plot(SA1_, color=fs.constants.affcol['SA1'], label='SA1')
    ax2.plot(SA2_, color=fs.constants.affcol['SA2'], label='SA2')
    ax2.set_xlabel("Step progress (%)", color="black")
    ax2.set_ylabel("Firing rate (Hz)", color="black")
    ax2.tick_params(axis='x', colors="black")
    ax2.tick_params(axis='y', colors="black")
    ax2.set_xlim(len(FA1_) * .59, len(FA1_) * .99)
    ax2.set_ylim(0, hz_lim)

    ax.axvspan(835.841584, 848.3168316, color='pink')

    ax.axvspan(960.5940594, 973.063069, color='cyan')

    ax.axvspan(1085.346354, 1097.82178217, color='lightgreen')

    locs = ax.get_xticks()
    print(locs)
    diff = 508.0
    print(diff)
    quarter = np.min(locs) + diff * .25
    half = np.min(locs) + diff * .5
    three_quarter = np.min(locs) + diff * .75

    ticks = [quarter, half, three_quarter]
    ax.set_xticks(ticks)
    ax.set_xticklabels(['25', '50', '75'])

    ax.plot(total_, color="black")
    ax.xaxis.tick_top()
    ax.yaxis.tick_right()
    # ax.set_xlabel('x label 2', color="C1") 
    ax.set_ylabel('Total pressure', color="black")
    ax.xaxis.set_label_position('top')
    ax.yaxis.set_label_position('right')
    ax.tick_params(axis='x', colors="black")
    ax.set_xticks([])
    ax.tick_params(axis='y', colors="black")
    ax.set_xlim(len(total_) * .59, len(total_) * .99)
    ax.set_ylim(0, pres_lim)

    plt.savefig(output_path + region_to_plot + ".png", format='png', dpi=100)
    
    
def one_step_total_pressure_response_all_frames_smooth(D, a, frames, output_path):
    """

    :param D:
    :param a:
    :param frames:
    :param output_path:
    :return:
    """
    # calculate stimulus and indentation
    s, regions, reshaped_data, idxs, D = map2footsim(D)

    r = a.response(s)

    under_threshold, step_start, index_differences, total_pressure = check4steps(D, frames=frames)

    # plot total pressure per frame with afferent responses

    x = list(range(D.shape[2]))
    total_Spline = scipy.interpolate.make_interp_spline(x, total_pressure)
    X_ = np.linspace(min(x), max(x), D.shape[2]*5)
    total_ = total_Spline(X_)
    total_[total_ < 0] = 0

    return s, r, total_
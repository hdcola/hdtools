import sys
import re

def calc_time_diff(time1_str, time2_str):  # Not used in this code!
    '''Function: Calculate the numerical difference of two timestamps.
    This function is used to obtain the '[duration]' based on [start_time]
    and [end_time] for cutting a media with the following FFmpeg command:
    $ ffmpeg -i in.mpn -ss [start] -t [duration] out.mpn
    Parameters:
        time1_str <str> - The previous timestamp 'hh:mm:ss'.
        time2_str <str> - The latest timestamp 'hh:mm:ss'.
    Return:
        diff_str <str> - The numerical difference of two timestamps 'hh:mm:ss'.
    '''
    # Split timestamp to hh, mm, and ss.
    time1_list = re.split('[:]', time1_str)  # <list> with 3 elements (hh, mm, ss).
    time2_list = re.split('[:]', time2_str)  # <list> with 3 elements (hh, mm, ss).

    # Convert <str> to <int> for calculation (+, *).
    time1_s = int(time1_list[0]) * 3600 + int(time1_list[1]) * 60 + int(time1_list[2])
    time2_s = int(time2_list[0]) * 3600 + int(time2_list[1]) * 60 + int(time2_list[2])

    # Calculate hh, mm, and ss of timestamp difference.
    diff = time2_s - time1_s  # Total timestamp difference (seconds).
    diff_h = int(diff / 3600)
    diff_m = int((diff % 3600) / 60)
    diff_s = int(diff % 60)

    # Concatenate hh, mm, and ss of timestamp difference.
    diff_str = str(diff_h).zfill(2) + ':' + str(diff_m).zfill(2) + ':' + str(diff_s).zfill(2)

    return diff_str

print(calc_time_diff(sys.argv[1],sys.argv[2]))

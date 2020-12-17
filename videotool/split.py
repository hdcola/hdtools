#!/usr/bin/env python3
import sys

def help():
    return """
请使用三个参数来运行本程序：
split.py  <moviename>  <movetime> <split_number>

moviename: 视频文件路径，需要是ffmpeg支持的格式
movetime: 视频时长，ffmpeg会用这个时长来计算如何切几段
split_name: 切为几段

示例：
split.py movie.mkv 3:20:10 3

将 movie.mkv的时长 3:20:10 切为3段。
    """

def movie_time_to_int(movie_time):
    # 将类似于 1:00:01 的时间，变换为 int的秒数
    h,m,s = movie_time.split(":")
    return int(h)*3600+int(m)*60+int(s)

def int_to_movie_time(int_time):
    # 将int秒变换为 1:00:01 的string时间
    h = int(int_time / 3600)
    m = int( (int_time % 3600) / 60 )
    s = int (int_time % 60)
    return f"{h}:{m}:{s}"

def split_time(movie_time,n):
    # 将movie_time切为n段，输入 30 返回 [0,10,10,10]
    s = [0]
    t = 0
    for i in range(n):
        if i == n-1:
            t = movie_time
        else:
            t += int(movie_time/n)
        s.append(t)
    return s

if len(sys.argv) != 4:
    print(help())
    sys.exit(1)

pyfile, movie_file, movie_time, split_number = sys.argv

int_movie_time = movie_time_to_int(movie_time)
movie_split = split_time( int_movie_time,int(split_number) )
print(f"总时长：{int_movie_time} 秒 切{split_number}段")
print(f"分段时间为：{ movie_split }\n请执行以下命令：\n\n")

# ffmpeg -ss 00:00:00 -i 林中漫步.超清中英双字.mp4  -c copy -t 1:00:0 part1.mp4

sfile_name = movie_file.split(".")[0]

for i in range( len(movie_split) - 1 ):
    print( f"ffmpeg -ss { int_to_movie_time(movie_split[i]) } -i {movie_file} -c copy -t {movie_split[i+1] - movie_split[i]} {sfile_name}.{i+1}.mp4" )

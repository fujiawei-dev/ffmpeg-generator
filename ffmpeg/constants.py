'''
Date: 2021.02-24 14:58:57
LastEditors: Rustle Karl
LastEditTime: 2021.05.04 23:36:56
'''
import sys

LINUX = sys.platform == 'linux'
WINDOWS = sys.platform == 'win32'

# Video Source
VIDEO_SOURCES = {
    'allrgb', 'allyuv', 'color', 'haldclutsrc', 'nullsrc',
    'pal75bars', 'pal100bars', 'rgbtestsrc', 'smptebars',
    'smptehdbars', 'testsrc', 'testsrc2', 'yuvtestsrc'
}

# CUDA Encoders
H264_NVENC = 'h264_nvenc'
HEVC_NVENC = 'hevc_nvenc'
CUDA_ENCODERS = {H264_NVENC, HEVC_NVENC}

# CUDA Decoders
H264_CUVID = 'h264_cuvid'
HEVC_CUVID = 'hevc_cuvid'
MJPEG_CUVID = 'mjpeg_cuvid'
MPEG1_CUVID = 'mpeg1_cuvid'
MPEG2_CUVID = 'mpeg2_cuvid'
MPEG4_CUVID = 'mpeg4_cuvid'
VC1_CUVID = 'vc1_cuvid'
VP8_CUVID = 'vp8_cuvid'
VP9_CUVID = 'vp9_cuvid'

# Expression
REAL_TIME = '%{localtime:%Y-%m-%d %H-%M-%S}'

# Format
COPY = 'copy'
RAW_VIDEO = 'rawvideo'
S16LE = 's16le'

# Pixel Format
RGB24 = 'rgb24'
PCM_S16LE = 'pcm_s16le'

# PTS
PTS_STARTPTS = 'PTS-STARTPTS'

# Input/Output
PIPE = 'pipe:'

# Resolution
HD = HD720 = '1280x720'
FHD = HD1080 = '1920x1080'
QHD = HD2K = HD1440 = '2560x1440'
UHD = HD4K = HD2160 = '3840x2160'

# Image Formats
IMAGE_FORMATS = {'.bmp', '.gif', '.heif', '.jpeg', '.jpg', '.png', '.raw', '.tiff'}

JSON_FORMAT = 'json'

'''
Date: 2021.03.07 21:50:15
LastEditors: Rustle Karl
LastEditTime: 2021.03.07 21:55:27
'''


class XFade(object):
    """Apply cross fade from one input video stream to another input video stream.
        The cross fade is applied for specified duration.

    https://ffmpeg.org/ffmpeg-filters.html#xfade
    """
    Circleclose = "circleclose"
    Circlecrop = "circlecrop"
    Circleopen = "circleopen"
    Custom = "custom"
    Diagbl = "diagbl"
    Diagbr = "diagbr"
    Diagtl = "diagtl"
    Diagtr = "diagtr"
    Dissolve = "dissolve"
    Distance = "distance"
    Fade = "fade"
    Fadeblack = "fadeblack"
    Fadegrays = "fadegrays"
    Fadewhite = "fadewhite"
    Hblur = "hblur"
    Hlslice = "hlslice"
    Horzopen = "horzopen"
    Hrslice = "hrslice"
    Pixelize = "pixelize"
    Radial = "radial"
    Rectcrop = "rectcrop"
    Slidedown = "slidedown"
    Slideleft = "slideleft"
    Slideright = "slideright"
    Slideup = "slideup"
    Smoothdown = "smoothdown"
    Smoothleft = "smoothleft"
    Smoothright = "smoothright"
    Smoothup = "smoothup"
    Squeezeh = "squeezeh"
    Squeezev = "squeezev"
    Vdslice = "vdslice"
    Vertclose = "vertclose"
    Vertopen = "vertopen"
    Vuslice = "vuslice"
    Wipebl = "wipebl"
    Wipebr = "wipebr"
    Wipedown = "wipedown"
    Wipeleft = "wipeleft"
    Wiperight = "wiperight"
    Wipetl = "wipetl"
    Wipetr = "wipetr"
    Wipeup = "wipeup"
    Horzclose = "horzclose"


All = [v for k, v in vars(XFade).items() if not k.endswith("__")]

if __name__ == '__main__':
    print(All)

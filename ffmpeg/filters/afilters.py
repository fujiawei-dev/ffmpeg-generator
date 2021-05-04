'''
Date: 2021.02-28 22:29:00
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 13:31:49
'''
from ..nodes import FilterableStream, Stream, filterable
from .avfilters import filter

__all__ = []

"""Audio Filters

https://ffmpeg.org/ffmpeg-filters.html#Audio-Filters
"""


@filterable()
def acompressor(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acompressor"""
    return filter(stream, acompressor.__name__, *args, **kwargs)


@filterable()
def acontrast(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acontrast"""
    return filter(stream, acontrast.__name__, *args, **kwargs)


@filterable()
def acopy(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acopy"""
    return filter(stream, acopy.__name__, *args, **kwargs)


@filterable()
def acrossfade(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acrossfade"""
    return filter(stream, acrossfade.__name__, *args, **kwargs)


@filterable()
def acrossover(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acrossover"""
    return filter(stream, acrossover.__name__, *args, **kwargs)


@filterable()
def acrusher(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acrusher"""
    return filter(stream, acrusher.__name__, *args, **kwargs)


@filterable()
def acue(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#acue"""
    return filter(stream, acue.__name__, *args, **kwargs)


@filterable()
def adeclick(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#adeclick"""
    return filter(stream, adeclick.__name__, *args, **kwargs)


@filterable()
def adeclip(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#adeclip"""
    return filter(stream, adeclip.__name__, *args, **kwargs)


@filterable()
def adelay(stream: Stream, delays: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#adelay"""
    return filter(stream, adelay.__name__, delays=delays)


@filterable()
def adenorm(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#adenorm"""
    return filter(stream, adenorm.__name__, *args, **kwargs)


@filterable()
def aintegral(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aintegral"""
    return filter(stream, aintegral.__name__, *args, **kwargs)


@filterable()
def aecho(stream: Stream, in_gain: int = None, out_gain: int = None,
          delays: str = None, decays: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aecho"""
    return filter(stream, aecho.__name__, in_gain=in_gain, out_gain=out_gain, delays=delays, decays=decays)


@filterable()
def aemphasis(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aemphasis"""
    return filter(stream, aemphasis.__name__, *args, **kwargs)


@filterable()
def aeval(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aeval"""
    return filter(stream, aeval.__name__, *args, **kwargs)


@filterable()
def aexciter(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aexciter"""
    return filter(stream, aexciter.__name__, *args, **kwargs)


@filterable()
def afade(stream: Stream, fadein: bool = False, fadeout: bool = False,
          start_sample: int = None, nb_samples: int = None, start_time: int = None,
          duration: int = None, curve: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afade"""
    afade_type = "in" if (fadein and not fadeout) else "out"
    return filter(stream, afade.__name__, t=afade_type, ss=start_sample, ns=nb_samples, st=start_time, d=duration,
                  curve=curve)


@filterable()
def afftdn(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afftdn"""
    return filter(stream, afftdn.__name__, *args, **kwargs)


@filterable()
def afftfilt(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afftfilt"""
    return filter(stream, afftfilt.__name__, *args, **kwargs)


@filterable()
def afir(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afir"""
    return filter(stream, afir.__name__, *args, **kwargs)


@filterable()
def aformat(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aformat"""
    return filter(stream, aformat.__name__, *args, **kwargs)


@filterable()
def afreqshift(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afreqshift"""
    return filter(stream, afreqshift.__name__, *args, **kwargs)


@filterable()
def agate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#agate"""
    return filter(stream, agate.__name__, *args, **kwargs)


@filterable()
def aiir(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aiir"""
    return filter(stream, aiir.__name__, *args, **kwargs)


@filterable()
def alimiter(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#alimiter"""
    return filter(stream, alimiter.__name__, *args, **kwargs)


@filterable()
def allpass(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#allpass"""
    return filter(stream, allpass.__name__, *args, **kwargs)


@filterable()
def aloop(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aloop"""
    return filter(stream, aloop.__name__, *args, **kwargs)


@filterable()
def amerge(stream: Stream, inputs: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#amerge"""
    return filter(stream, amerge.__name__, inputs=inputs)


@filterable()
def amix(stream: Stream, inputs: int = None, duration: str = None,
         dropout_transition: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#amix"""
    return filter(stream, amix.__name__, inputs=inputs, duration=duration, dropout_transition=dropout_transition)


@filterable()
def amultiply(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#amultiply"""
    return filter(stream, amultiply.__name__, *args, **kwargs)


@filterable()
def anequalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anequalizer"""
    return filter(stream, anequalizer.__name__, *args, **kwargs)


@filterable()
def anlmdn(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anlmdn"""
    return filter(stream, anlmdn.__name__, *args, **kwargs)


@filterable()
def anlms(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anlms"""
    return filter(stream, anlms.__name__, *args, **kwargs)


@filterable()
def anull(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anull"""
    return filter(stream, anull.__name__, *args, **kwargs)


@filterable()
def apad(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#apad"""
    return filter(stream, apad.__name__, *args, **kwargs)


@filterable()
def aphaser(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aphaser"""
    return filter(stream, aphaser.__name__, *args, **kwargs)


@filterable()
def aphaseshift(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aphaseshift"""
    return filter(stream, aphaseshift.__name__, *args, **kwargs)


@filterable()
def apulsator(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#apulsator"""
    return filter(stream, apulsator.__name__, *args, **kwargs)


@filterable()
def aresample(stream: Stream, inputs: int = None, duration: str = None,
              dropout_transition: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aresample"""
    return filter(stream, aresample.__name__, inputs=inputs, duration=duration, dropout_transition=dropout_transition)


@filterable()
def areverse(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#areverse"""
    return filter(stream, areverse.__name__, *args, **kwargs)


@filterable()
def arnndn(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#arnndn"""
    return filter(stream, arnndn.__name__, *args, **kwargs)


@filterable()
def asetnsamples(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asetnsamples"""
    return filter(stream, asetnsamples.__name__, *args, **kwargs)


@filterable()
def asetrate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asetrate"""
    return filter(stream, asetrate.__name__, *args, **kwargs)


@filterable()
def ashowinfo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ashowinfo"""
    return filter(stream, ashowinfo.__name__, *args, **kwargs)


@filterable()
def asoftclip(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asoftclip"""
    return filter(stream, asoftclip.__name__, *args, **kwargs)


@filterable()
def asr(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asr"""
    return filter(stream, asr.__name__, *args, **kwargs)


@filterable()
def astats(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#astats"""
    return filter(stream, astats.__name__, *args, **kwargs)


@filterable()
def asubboost(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asubboost"""
    return filter(stream, asubboost.__name__, *args, **kwargs)


@filterable()
def asubcut(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asubcut"""
    return filter(stream, asubcut.__name__, *args, **kwargs)


@filterable()
def asupercut(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asupercut"""
    return filter(stream, asupercut.__name__, *args, **kwargs)


@filterable()
def asuperpass(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asuperpass"""
    return filter(stream, asuperpass.__name__, *args, **kwargs)


@filterable()
def asuperstop(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asuperstop"""
    return filter(stream, asuperstop.__name__, *args, **kwargs)


@filterable()
def atempo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#atempo"""
    return filter(stream, atempo.__name__, *args, **kwargs)


@filterable()
def atrim(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#atrim"""
    return filter(stream, atrim.__name__, *args, **kwargs)


@filterable()
def axcorrelate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#axcorrelate"""
    return filter(stream, axcorrelate.__name__, *args, **kwargs)


@filterable()
def bandpass(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bandpass"""
    return filter(stream, bandpass.__name__, *args, **kwargs)


@filterable()
def bandreject(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bandreject"""
    return filter(stream, bandreject.__name__, *args, **kwargs)


@filterable()
def lowshelf(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lowshelf"""
    return filter(stream, lowshelf.__name__, *args, **kwargs)


@filterable()
def biquad(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#biquad"""
    return filter(stream, biquad.__name__, *args, **kwargs)


@filterable()
def bs2b(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bs2b"""
    return filter(stream, bs2b.__name__, *args, **kwargs)


@filterable()
def channelmap(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#channelmap"""
    return filter(stream, channelmap.__name__, *args, **kwargs)


@filterable()
def channelsplit(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#channelsplit"""
    return filter(stream, channelsplit.__name__, *args, **kwargs)


@filterable()
def chorus(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#chorus"""
    return filter(stream, chorus.__name__, *args, **kwargs)


@filterable()
def compand(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#compand"""
    return filter(stream, compand.__name__, *args, **kwargs)


@filterable()
def compensationdelay(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#compensationdelay"""
    return filter(stream, compensationdelay.__name__, *args, **kwargs)


@filterable()
def crossfeed(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#crossfeed"""
    return filter(stream, crossfeed.__name__, *args, **kwargs)


@filterable()
def crystalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#crystalizer"""
    return filter(stream, crystalizer.__name__, *args, **kwargs)


@filterable()
def dcshift(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dcshift"""
    return filter(stream, dcshift.__name__, *args, **kwargs)


@filterable()
def deesser(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deesser"""
    return filter(stream, deesser.__name__, *args, **kwargs)


@filterable()
def drmeter(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#drmeter"""
    return filter(stream, drmeter.__name__, *args, **kwargs)


@filterable()
def dynaudnorm(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dynaudnorm"""
    return filter(stream, dynaudnorm.__name__, *args, **kwargs)


@filterable()
def earwax(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#earwax"""
    return filter(stream, earwax.__name__, *args, **kwargs)


@filterable()
def equalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#equalizer"""
    return filter(stream, equalizer.__name__, *args, **kwargs)


@filterable()
def extrastereo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#extrastereo"""
    return filter(stream, extrastereo.__name__, *args, **kwargs)


@filterable()
def firequalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#firequalizer"""
    return filter(stream, firequalizer.__name__, *args, **kwargs)


@filterable()
def flanger(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#flanger"""
    return filter(stream, flanger.__name__, *args, **kwargs)


@filterable()
def haas(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#haas"""
    return filter(stream, haas.__name__, *args, **kwargs)


@filterable()
def hdcd(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hdcd"""
    return filter(stream, hdcd.__name__, *args, **kwargs)


@filterable()
def headphone(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#headphone"""
    return filter(stream, headphone.__name__, *args, **kwargs)


@filterable()
def highpass(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#highpass"""
    return filter(stream, highpass.__name__, *args, **kwargs)


@filterable()
def join(*streams: Stream, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#join"""
    return filter(streams, join.__name__, min_inputs=2, **kwargs)


@filterable()
def ladspa(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ladspa"""
    return filter(stream, ladspa.__name__, *args, **kwargs)


@filterable()
def loudnorm(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#loudnorm"""
    return filter(stream, loudnorm.__name__, *args, **kwargs)


@filterable()
def lowpass(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lowpass"""
    return filter(stream, lowpass.__name__, *args, **kwargs)


@filterable()
def lv2(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lv2"""
    return filter(stream, lv2.__name__, *args, **kwargs)


@filterable()
def mcompand(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mcompand"""
    return filter(stream, mcompand.__name__, *args, **kwargs)


@filterable()
def pan(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pan"""
    return filter(stream, pan.__name__, *args, **kwargs)


@filterable()
def replaygain(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#replaygain"""
    return filter(stream, replaygain.__name__, *args, **kwargs)


@filterable()
def resample(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#resample"""
    return filter(stream, resample.__name__, *args, **kwargs)


@filterable()
def rubberband(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#rubberband"""
    return filter(stream, rubberband.__name__, *args, **kwargs)


@filterable()
def sidechaincompress(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sidechaincompress"""
    return filter(stream, sidechaincompress.__name__, *args, **kwargs)


@filterable()
def sidechaingate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sidechaingate"""
    return filter(stream, sidechaingate.__name__, *args, **kwargs)


@filterable()
def silencedetect(stream: Stream, noise: float, duration: float = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#silencedetect"""
    return filter(stream, silencedetect.__name__, n=f"{noise}dB", d=duration)


@filterable()
def silenceremove(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#silenceremove"""
    return filter(stream, silenceremove.__name__, *args, **kwargs)


@filterable()
def sofalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sofalizer"""
    return filter(stream, sofalizer.__name__, *args, **kwargs)


@filterable()
def speechnorm(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#speechnorm"""
    return filter(stream, speechnorm.__name__, *args, **kwargs)


@filterable()
def stereotools(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#stereotools"""
    return filter(stream, stereotools.__name__, *args, **kwargs)


@filterable()
def stereowiden(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#stereowiden"""
    return filter(stream, stereowiden.__name__, *args, **kwargs)


@filterable()
def superequalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#superequalizer"""
    return filter(stream, superequalizer.__name__, *args, **kwargs)


@filterable()
def surround(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#surround"""
    return filter(stream, surround.__name__, *args, **kwargs)


@filterable()
def highshelf(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#highshelf"""
    return filter(stream, highshelf.__name__, *args, **kwargs)


@filterable()
def tremolo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tremolo"""
    return filter(stream, tremolo.__name__, *args, **kwargs)


@filterable()
def vibrato(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vibrato"""
    return filter(stream, vibrato.__name__, *args, **kwargs)


@filterable()
def volume(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#volume"""
    return filter(stream, volume.__name__, *args, **kwargs)


@filterable()
def volumedetect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#volumedetect"""
    return filter(stream, volumedetect.__name__, *args, **kwargs)


"""Audio Sources

https://ffmpeg.org/ffmpeg-filters.html#Audio-Sources
"""


@filterable()
def abuffer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#abuffer"""
    return filter(stream, abuffer.__name__, *args, **kwargs)


@filterable()
def aevalsrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aevalsrc"""
    return filter(stream, aevalsrc.__name__, *args, **kwargs)


@filterable()
def afirsrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afirsrc"""
    return filter(stream, afirsrc.__name__, *args, **kwargs)


@filterable()
def anullsrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anullsrc"""
    return filter(stream, anullsrc.__name__, *args, **kwargs)


@filterable()
def flite(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#flite"""
    return filter(stream, flite.__name__, *args, **kwargs)


@filterable()
def anoisesrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anoisesrc"""
    return filter(stream, anoisesrc.__name__, *args, **kwargs)


@filterable()
def hilbert(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hilbert"""
    return filter(stream, hilbert.__name__, *args, **kwargs)


@filterable()
def sinc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sinc"""
    return filter(stream, sinc.__name__, *args, **kwargs)


@filterable()
def sine(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sine"""
    return filter(stream, sine.__name__, *args, **kwargs)


"""Audio Sinks

https://ffmpeg.org/ffmpeg-filters.html#Audio-Sinks
"""


@filterable()
def abuffersink(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#abuffersink"""
    return filter(stream, abuffersink.__name__, *args, **kwargs)


@filterable()
def anullsink(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#anullsink"""
    return filter(stream, anullsink.__name__, *args, **kwargs)

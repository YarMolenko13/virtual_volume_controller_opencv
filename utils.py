import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


def count_distance(coord1, coord2):
    oX = abs(coord1[0] - coord2[0])
    oY = abs(coord1[1] - coord2[1])
    g = math.sqrt(oX ** 2 + oY ** 2)
    return g


def set_volume(value):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        vol_range = volume.GetVolumeRange()
        min_vol = vol_range[0]
        max_vol = vol_range[1]
        if value < 30:
            volume.SetMasterVolumeLevel(min_vol, None)
        elif value >= 30 and value < 400:
            # Volume -65 - 0
            vol = np.interp(value, [30, 400], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)
        else:
            volume.SetMasterVolumeLevel(max_vol, None)
    except Exception:
        print(Exception)

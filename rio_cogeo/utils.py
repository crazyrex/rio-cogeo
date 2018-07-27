"""rio_cogeo.utils: Utility functions."""

import math

from rasterio.enums import MaskFlags
from rasterio.warp import calculate_default_transform


def _meters_per_pixel(zoom, lat):
    return (math.cos(lat * math.pi / 180.0) * 2 * math.pi * 6378137) / (256 * 2 ** zoom)


def get_max_zoom(src, snap=0.5, max_z=23):
    """Calculate raster max zoom level."""
    dst_affine, w, h = calculate_default_transform(
        src.crs, "epsg:3857", src.width, src.height, *src.bounds
    )

    res_max = max(abs(dst_affine[0]), abs(dst_affine[4]))

    tgt_z = max_z
    mpp = 0.0

    # loop through the pyramid to file the closest z level
    for z in range(1, max_z):
        mpp = _meters_per_pixel(z, 0)

        if (mpp - ((mpp / 2) * snap)) < res_max:
            tgt_z = z
            break

    return tgt_z


def has_alpha_band(src):
    """Check if a source has an alpha band."""
    for flags in src.mask_flag_enums:
        if MaskFlags.alpha in flags:
            return True
    return False
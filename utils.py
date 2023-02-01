import math

def dbm_to_vpp(dbm: int, Z: int = 50) -> float:
    """ Convert Vpp to dBm
    """
    vpp: float = 2 * math.sqrt(
        (2 * Z) / 1000
    ) * math.pow(
        10, (dbm / 20)
    )
    
    return round(vpp, 3)

import math


class NearestDistance:
    """
    Burada OOP prensiplerine uygun haversine hesaplama işlemleri yazılmıştır.
    """

    def __init__(self, lat1: float, lon1: float, lat2: float, lon2: float) -> None:

        # Dünya yarıçapı (km)
        self.earth_radius = 6371

        # Derece -> Radyan dönüşümü
        self.phi1 = math.radians(lat1)
        self.phi2 = math.radians(lat2)
        self.dphi = math.radians(lat2 - lat1)
        self.dlambda = math.radians(lon2 - lon1)

    def haversine_distance(self) -> float:
        # Haversine formülü
        a = (
            math.sin(self.dphi / 2) ** 2
            + math.cos(self.phi1)
            * math.cos(self.phi2)
            * math.sin(self.dlambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        # KM cinsinden döner
        return self.earth_radius * c

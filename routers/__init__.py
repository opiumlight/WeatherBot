from routers.start import start_router
from routers.geoposition import geo_router
from routers.weather import weather_router
from routers.notifications import notifications_router
routers_list = [start_router, geo_router, weather_router, notifications_router]

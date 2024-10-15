from rest_framework import routers

from blog.views import ArticleViewset

__all__ = ["router_urls"]


router = routers.SimpleRouter()
router.register(r"article", ArticleViewset, basename="articles")
router_urls = router.urls

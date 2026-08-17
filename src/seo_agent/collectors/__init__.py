"""Credential-free delta collector adapters."""

from seo_agent.collectors.bitrix24 import Bitrix24Collector
from seo_agent.collectors.ga4 import GA4Collector
from seo_agent.collectors.google_search_console import GoogleSearchConsoleCollector
from seo_agent.collectors.yandex_metrica import YandexMetricaCollector
from seo_agent.collectors.yandex_webmaster import YandexWebmasterCollector

__all__ = [
    "Bitrix24Collector",
    "GA4Collector",
    "GoogleSearchConsoleCollector",
    "YandexMetricaCollector",
    "YandexWebmasterCollector",
]

# Attribution

Channels are limited to `organic_google`, `organic_yandex`, `paid_google`,
`paid_yandex`, `direct`, `referral`, `email`, `messenger`, `call`, `partner`, and
`unknown`. The resolver uses explicit UTM paid signals first, then an explicit
search-engine source, then explicit medium/source mappings. A non-evidenced guess
is forbidden: missing or conflicting evidence stays `unknown` with low confidence.

The raw source fields remain intact. The normalized output records channel,
evidence and confidence so mappings can be audited and improved.

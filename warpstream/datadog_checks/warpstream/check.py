from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout

from datadog_checks.base import AgentCheck, ConfigurationError


class WarpstreamCheck(AgentCheck):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'warpstream'

    def __init__(self, name, init_config, instances):
        super(WarpstreamCheck, self).__init__(name, init_config, instances)

        self._url = self.instance.get('url', '')
        self._tags = self.instance.get('tags', [])
        # The Agent only makes one attempt to instantiate each AgentCheck so any errors occurring
        # in `__init__` are logged just once, making it difficult to spot. Therefore, we emit
        # potential configuration errors as part of the check run phase.
        # The configuration is only parsed once if it succeed, otherwise it's retried.
        self.check_initializations.append(self._parse_config)

    def _parse_config(self):
        if not self._url:
            raise ConfigurationError('Missing configuration: url')

    def check(self, _):
        tags = ['url:{}'.format(self._url)] + self._tags

        url_warpstream_agent = self._url + "/api/v1/status"

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/
        try:
            response = self.http.get(url_warpstream_agent)
            response.raise_for_status()

        except Timeout:
            self.gauge('can_connect', 0, tags=tags)
            raise

        except (HTTPError, InvalidURL, ConnectionError):
            self.gauge('can_connect', 0, tags=tags)
            raise

        except ValueError:
            self.gauge('can_connect', 0, tags=tags)
            raise

        self.gauge('can_connect', 1, tags=tags)

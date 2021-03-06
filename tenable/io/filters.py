from .base import TIOEndpoint

class FiltersAPI(TIOEndpoint):
    _cache = dict()

    def _normalize(self, filterset):
        '''
        Converts the filters into an easily parsable dictionary
        '''
        filters = dict()
        for item in filterset:
            f = {
                'operators': item['operators'],
                'choices': None,
                'pattern': None,
            }

            # If there is a list of choices available, then we need to parse
            # them out and only pull back the usable values as a list
            if 'list' in item['control']:
                # There is a lack of consistancy here.  In some cases the "list"
                # is a list of dictionary items, and in other cases the "list"
                # is a list of string values.
                if isinstance(item['control']['list'][0], dict):
                    key = 'value' if 'value' in item['control']['list'][0] else 'id'
                    f['choices'] = [i[key] for i in item['control']['list']]
                elif isinstance(item['control']['list'], list):
                    f['choices'] = item['control']['list']
            if 'regex' in item['control']:
                f['pattern'] = item['control']['regex']
            filters[item['name']] = f
        return filters

    def _use_cache(self, name, path, normalize=True):
        '''
        Leverages the filter cache and will return the results as expected.
        '''
        if name not in self._cache:
            self._cache[name] = self._api.get(path).json()['filters']

        if normalize:
            return self._normalize(self._cache[name])
        else:
            return self._cache[name]

    def agents_filters(self, normalize=True):
        '''
        `filters: agents-filters <https://cloud.tenable.com/api#/resources/filters/agents-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._use_cache('agents', 'filters/scans/agents', normalize)

    def workbench_vuln_filters(self, normalize=True):
        '''
        `workbenches: vulnerabilities-filters <https://cloud.tenable.com/api#/resources/workbenches/vulnerabilities-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._use_cache('vulns', 'filters/workbenches/vulnerabilities', normalize)

    def workbench_asset_filters(self, normalize=True):
        '''
        `workbenches: assets-filters <https://cloud.tenable.com/api#/resources/workbenches/assets-filters>`_

        Returns:
            dict: Filter resource dictionary
        '''
        return self._use_cache('asset', 'filters/workbenches/assets', normalize)

    def scan_filters(self, normalize=True):
        '''
        Returns:
            dict: Filter resource dictionary
        '''
        return self._use_cache('scan', 'filters/scans/reports', normalize)

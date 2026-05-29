# flake8: noqa
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ms_agent.tools.search.search_base import (BaseResult, SearchRequest,
                                               SearchResponse, SearchResult)


class TavilySearchRequest(SearchRequest):
    """
    A class representing a search request to Tavily.
    """

    def __init__(self,
                 query: str,
                 num_results: Optional[int] = 5,
                 search_depth: Optional[str] = 'advanced',
                 topic: Optional[str] = 'general',
                 include_domains: Optional[List[str]] = None,
                 exclude_domains: Optional[List[str]] = None,
                 **kwargs: Any):
        """
        Initialize TavilySearchRequest with search parameters.

        Args:
            query: The search query string
            num_results: Number of results to return, default is 5
            search_depth: Search depth ('basic' or 'advanced'), default is 'advanced'
            topic: Topic category ('general', 'news', 'finance'), default is 'general'
            include_domains: List of domains to restrict search to
            exclude_domains: List of domains to exclude from search
        """
        super().__init__(query=query, num_results=num_results, **kwargs)
        self.search_depth = search_depth
        self.topic = topic
        self.include_domains = include_domains
        self.exclude_domains = exclude_domains

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the request parameters to a dictionary.

        Returns:
            Dict[str, Any]: The parameters as a dictionary
        """
        d = {
            'query': self.query,
            'max_results': self.num_results,
            'search_depth': self.search_depth,
            'topic': self.topic,
        }
        if self.include_domains:
            d['include_domains'] = self.include_domains
        if self.exclude_domains:
            d['exclude_domains'] = self.exclude_domains
        return d


class TavilySearchResult(SearchResult):
    """Tavily search result implementation."""

    def __init__(self,
                 query: str,
                 arguments: Dict[str, Any] = None,
                 response: Any = None):
        super().__init__(query=query, arguments=arguments, response=response)
        self.response = self._process_results() if response else None

    def _process_results(self) -> SearchResponse:
        """Process raw Tavily response into standardized SearchResponse."""
        if not self.response:
            return SearchResponse(results=[])

        raw_results = self.response.get('results', [])
        results = []
        for r in raw_results:
            results.append(BaseResult(
                url=r.get('url', ''),
                id=r.get('url', ''),
                title=r.get('title', ''),
                summary=r.get('content', ''),
                markdown=r.get('raw_content'),
            ))

        return SearchResponse(results=results)

    def to_list(self) -> List[Dict[str, Any]]:
        """Convert the search results to a list of dictionaries."""
        if not self.response or not self.response.results:
            print('***Warning: No search results found.')
            return []

        if not self.query:
            print('***Warning: No query provided for search results.')
            return []

        res_list: List[Dict[str, Any]] = []
        for res in self.response.results:
            res_list.append({
                'url': res.url,
                'id': res.id,
                'title': res.title,
                'highlights': res.highlights,
                'highlight_scores': res.highlight_scores,
                'summary': res.summary,
                'markdown': res.markdown,
            })

        return res_list

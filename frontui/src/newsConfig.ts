import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "news"
});

export const news_config = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
  hasA11yNotifications: true,
  searchQuery: {
    search_fields: {
      title: {
        weight: 5
      },
      text: {}
    },
    result_fields: {
      title: {
        snippet: {
          size: 100,
          fallback: true
        }
      },
      text: {
        snippet: {
          size: 100,
          fallback: true
        }
      },
      url: {},
      screenshot: {},
      time: {}
    },
    disjunctiveFacets: ["title.keyword"],
    facets: {
      "title.keyword": { type: "value", size: 10 },
    }
  },
  autocompleteQuery: {
    results: {
      resultsPerPage: 5,
      result_fields: {
        title: {
          snippet: {
            size: 100,
            fallback: true
          }
        }
      }
    },
    suggestions: {
      types: {
        documents: {
          fields: ["suggest"]
        }
      },
      size: 4
    }
  }
};
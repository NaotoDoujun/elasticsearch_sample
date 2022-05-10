import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import AppSearchAPIConnector from '@elastic/search-ui-app-search-connector';
import moment from "moment";

const WIKIPEDIA_CONNECTOR = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "wikipedia"
});

export const WIKIPEDIA_CONFIG = {
  debug: true,
  alwaysSearchOnInitialLoad: false,
  apiConnector: WIKIPEDIA_CONNECTOR,
  hasA11yNotifications: true,
  searchQuery: {
    search_fields: {
      title: {},
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
      }
    },
    disjunctiveFacets: [
      "acres"
    ],
    facets: {
      acres: {
        type: "range",
        ranges: [
          { from: -1, name: "Any" },
          { from: 0, to: 1000, name: "Small" },
          { from: 1001, to: 100000, name: "Medium" },
          { from: 100001, name: "Large" }
        ]
      }
    }
  }
};

const NATIONAL_PARKS_CONNECTOR = new AppSearchAPIConnector({
  searchKey: 'search-nyxkw1fuqex9qjhfvatbqfmw',
  engineName: 'national-parks',
  endpointBase: 'https://search-ui-sandbox.ent.us-central1.gcp.cloud.es.io'
});

export const NATIONAL_PARKS_CONFIG = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: NATIONAL_PARKS_CONNECTOR,
  hasA11yNotifications: true,
  searchQuery: {
    result_fields: {
      visitors: { raw: {} },
      world_heritage_site: { raw: {} },
      location: { raw: {} },
      acres: { raw: {} },
      square_km: { raw: {} },
      title: {
        snippet: {
          size: 100,
          fallback: true
        }
      },
      nps_link: { raw: {} },
      states: { raw: {} },
      date_established: { raw: {} },
      image_url: { raw: {} },
      description: {
        snippet: {
          size: 100,
          fallback: true
        }
      }
    },
    disjunctiveFacets: ["acres", "states", "date_established", "location"],
    facets: {
      world_heritage_site: { type: "value" },
      states: { type: "value", size: 30 },
      acres: {
        type: "range",
        ranges: [
          { from: -1, name: "Any" },
          { from: 0, to: 1000, name: "Small" },
          { from: 1001, to: 100000, name: "Medium" },
          { from: 100001, name: "Large" }
        ]
      },
      date_established: {
        type: "range",
        ranges: [
          {
            from: moment().subtract(50, "years").toISOString(),
            name: "Within the last 50 years"
          },
          {
            from: moment().subtract(100, "years").toISOString(),
            to: moment().subtract(50, "years").toISOString(),
            name: "50 - 100 years ago"
          },
          {
            to: moment().subtract(100, "years").toISOString(),
            name: "More than 100 years ago"
          }
        ]
      },
      visitors: {
        type: "range",
        ranges: [
          { from: 0, to: 10000, name: "0 - 10000" },
          { from: 10001, to: 100000, name: "10001 - 100000" },
          { from: 100001, to: 500000, name: "100001 - 500000" },
          { from: 500001, to: 1000000, name: "500001 - 1000000" },
          { from: 1000001, to: 5000000, name: "1000001 - 5000000" },
          { from: 5000001, to: 10000000, name: "5000001 - 10000000" },
          { from: 10000001, name: "10000001+" }
        ]
      }
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
        },
        nps_link: {
          raw: {}
        }
      }
    },
    suggestions: {
      types: {
        documents: {
          fields: ["title"]
        }
      },
      size: 4
    }
  }
};
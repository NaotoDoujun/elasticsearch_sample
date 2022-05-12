import { Results, ErrorBoundary, Paging } from '@elastic/react-search-ui';

function SearchResults() {
  return (
    <ErrorBoundary>
      <Results titleField="title" shouldTrackClickThrough={true} />
      <Paging />
    </ErrorBoundary>
  )
}

export { SearchResults }
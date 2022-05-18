import { Results, ErrorBoundary, PagingInfo, Paging } from '@elastic/react-search-ui';

function SearchResults() {
  return (
    <ErrorBoundary>
      <PagingInfo />
      <Results titleField="title" />
      <Paging />
    </ErrorBoundary>
  )
}

export { SearchResults }
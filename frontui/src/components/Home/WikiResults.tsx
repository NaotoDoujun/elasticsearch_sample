import { Results, ErrorBoundary, PagingInfo, Paging } from '@elastic/react-search-ui';

function WikiResults() {
  return (
    <ErrorBoundary>
      <PagingInfo />
      <Results titleField="title" />
      <Paging />
    </ErrorBoundary>
  )
}

export { WikiResults }